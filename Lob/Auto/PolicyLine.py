from addict import Dict
from datetime import date
from Utils.WriteJson import write_json

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def extract_policy_line_data(policy_data):
    
    policy_line_dict = Dict({})
    policy_data_dict = Dict(policy_data)

    policy_line_dict.PublicID = policy_data_dict.PublicID
    policy_line_dict.BasedOnPublicID = ""
    policy_line_dict.PolicyNumber = policy_data_dict.PolicyNumber
    policy_line_dict.ProcessDate = date.today().strftime("%Y-%m-%d")
    policy_line_dict.AccountDate = policy_data_dict.chargeAccountDate["$date"].split("T")[0]
    policy_line_dict.PeriodStart = policy_data_dict.PeriodStart["$date"].split("T")[0]
    policy_line_dict.PeriodEnd = policy_data_dict.PeriodEnd["$date"].split("T")[0]
    policy_line_dict.EditEffectiveDate = policy_data_dict.EditEffectiveDate["$date"].split("T")[0]
    policy_line_dict.BaseState = policy_data_dict.BaseState
    policy_line_dict.UWCompany = policy_data_dict.UWCompany.Code
    policy_line_dict.TermType = policy_data_dict.TermType_CD
    policy_line_dict.JobType = policy_data_dict.Lines[0].JobType
    policy_line_dict.TransactionPremium = policy_data_dict.TransactionPremiumRPT
    policy_line_dict.FirstInsuredYear = ""
    policy_line_dict.CreditScore = ""
    policy_line_dict.ScoreCardHAL = ""
    policy_line_dict.PolicyForm = ""
    policy_line_dict.SingleLimitPolicyInd = ""
    policy_line_dict.FinancialResp = ""
    policy_line_dict.HighestRatedCar = ""
    policy_line_dict.NumOperatorOnPolicy = len(policy_data_dict.Lines[0].PolicyDrivers)

    if policy_data_dict.Lines[0].PALineCoverages:
        for LineCov in range(len(policy_data_dict.Lines[0].PALineCoverages)):
            match policy_data_dict.Lines[0].PALineCoverages[LineCov].PatternCode:
                case "PALiabilityCov":
                    policy_line_dict.BIPDLimitCd = "1"
                    for LiabCov in range(len(policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms)):
                        match policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[LiabCov].PatternCode:
                            case "PALiability":
                                if len(policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[LiabCov].ValueAsString.split("/")) == 2:
                                    policy_line_dict.BILimitAmtPerClaim = policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[LiabCov].ValueAsString.split("/")[0]
                                    policy_line_dict.BILimitAmtPerOccr = policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[LiabCov].ValueAsString.split("/")[1]
                                else:
                                    policy_line_dict.BILimitAmtPerClaim = ""
                                    policy_line_dict.BILimitAmtPerOccr = policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[LiabCov].ValueAsString
                                policy_line_dict.BIDeductibleAmtPerClaim = ""
                                policy_line_dict.BIDeductibleAmtPerOccur = ""
                            case "PAPDLiability":
                                policy_line_dict.BIPDLimitCd = '2'
                                policy_line_dict.PDLimitAmt = policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[LiabCov].ValueAsString.replace("K",'')
                                policy_line_dict.PDDeductibleAmt = ""
                case "PAMedPayCov":
                    for MedCov in range(len(policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms)):
                        if policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[MedCov].PatternCode == "PAMedLimit":
                            policy_line_dict.MedLimitAmt = policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[MedCov].ValueAsString
                            policy_line_dict.MedDeductibleAmt = ""
                case "PAUMBICov":
                    for UMBICov in range(len(policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms)):
                        if policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[UMBICov].PatternCode == "PAUMBILimit":
                            if len(policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[UMBICov].ValueAsString.split("/")) == 2:
                                policy_line_dict.UMBILimitAmtPerClaim = policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[UMBICov].ValueAsString.split("/")[0]
                                policy_line_dict.UMBILimitAmtPerOccur = policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[UMBICov].ValueAsString.split("/")[1]
                            else:
                                policy_line_dict.UMBILimitAmtPerClaim = ""
                                policy_line_dict.UMBILimitAmtPerOccur = policy_data_dict.Lines[0].PALineCoverages[LineCov].CovTerms[UMBICov].ValueAsString
                            policy_line_dict.UMBIDeductibleAmtPerClaim = ""
                            policy_line_dict.UMBIDeductibleAmtPerOccur = ""

    policy_line_dict.UMBILimitCd = ""
    policy_line_dict.UMBIDeductibleAmtPerClaim = ""
    policy_line_dict.UMBIDeductibleAmtPerOccur = ""
    policy_line_dict.UMPDLimitAmt = ""
    policy_line_dict.UMPDDeductibleAmt = ""
    policy_line_dict.UDMBILimitCd = ""
    policy_line_dict.UDMBILimitAmtPerClaim = ""
    policy_line_dict.UDMBILimitAmtPerOccur = ""
    policy_line_dict.UDMBIDeductibleAmtPerClaim = ""
    policy_line_dict.UDMBIDeductibleAmtPerOccur = ""
    policy_line_dict.UDMPDLimitAmt = ""
    policy_line_dict.UDMPDDeductibleAmt = ""
    policy_line_dict.PIPLimitAmt = ""
    policy_line_dict.PIPDeductibleAmt = ""
    policy_line_dict.PIPCopayAmt = ""
    policy_line_dict.PolicyLineDiscounts = ""

    LineModifiers = []
    for Modifier in range(len(policy_data_dict.Lines[0].PAModifiers)):
        LineModifiers.append(policy_data_dict.Lines[0].PAModifiers[Modifier].PatternCode)
    policy_line_dict.PolicyPAModifiers = LineModifiers

    out_path = "C:\ProjectAlphaExtract\Output\PolicyLine.txt"
    write_json(out_path, policy_line_dict)
