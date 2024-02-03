from addict import Dict
from Utils.WriteJson import write_json

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def extract_premium_data(PublicID, Vehicle, LinePACosts, FirstCarOnPolicy):
    
    policy_premium_data = Dict({})

    policy_premium_data.PublicID = PublicID
    policy_premium_data.VehPublicID = Vehicle.PublicID
    policy_premium_data.VehicleNumber = Vehicle.VehicleNumber
    policy_premium_data.Vin = Vehicle.Vin

    for VehCov in range(len(Vehicle.Coverages)):
        match Vehicle.Coverages[VehCov].PatternCode:
            case "PACollisionCov":
                policy_premium_data.CollisonPremium = Vehicle.Coverages[VehCov].Costs[0].ActualAmount
            case "PAComprehensiveCov":
                policy_premium_data.ComprehensivePremium = Vehicle.Coverages[VehCov].Costs[0].ActualAmount
            case "PARentalCov":
                policy_premium_data.RentalPremium = Vehicle.Coverages[VehCov].Costs[0].ActualAmount

    for LineCost in range(len(Vehicle.Costs)):
        for LinePACost in range(len(LinePACosts)):
            if Vehicle.Costs[LineCost].PersonalAutoCov.PublicID == LinePACosts[LinePACost].PersonalAutoCov.PublicID:
                match LinePACosts[LinePACost].PersonalAutoCov.type:
                    case "PALiabilityCov":
                        if Vehicle.Costs[LineCost].CostType == "BI":
                            policy_premium_data.BodilyInjuryPremium = Vehicle.Costs[LineCost].ActualAmount
                        elif Vehicle.Costs[LineCost].CostType == "PD":
                            policy_premium_data.PropertyDamagePremium = Vehicle.Costs[LineCost].ActualAmount
                    case "PAMedPayCov":
                        policy_premium_data.MedicalPremium = Vehicle.Costs[LineCost].ActualAmount
            
            if Vehicle.VehicleNumber == FirstCarOnPolicy:
                match LinePACosts[LinePACost].PersonalAutoLineCov.type:
                    case "PAUMBICov":
                        policy_premium_data.UnisuredBIPremium = LinePACosts[LinePACost].ActualAmount

    out_path = "C:\ProjectAlphaExtract\Output\PolicyPremium.txt"
    write_json(out_path, policy_premium_data)


