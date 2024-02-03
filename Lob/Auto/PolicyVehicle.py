from addict import Dict
from Utils.WriteJson import write_json

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def extract_vehicle_data(PublicID, Vehicle, Drivers):
    
    policy_vehicle_data = Dict({})

    policy_vehicle_data.PublicID = PublicID
    policy_vehicle_data.VehPublicID = Vehicle.PublicID
    policy_vehicle_data.VehType = Vehicle.VehicleType
    policy_vehicle_data.VehicleNumber = Vehicle.VehicleNumber
    policy_vehicle_data.Vin = Vehicle.Vin
    policy_vehicle_data.ModelYear = Vehicle.Year
    policy_vehicle_data.EngineCC = ""
    policy_vehicle_data.TerritoryCode = Vehicle.GarageLocation.TerritoryCode.Code
    policy_vehicle_data.PostalCode = Vehicle.GarageLocation.PostalCode
    policy_vehicle_data.County = Vehicle.GarageLocation.County
    policy_vehicle_data.City = Vehicle.GarageLocation.City
    policy_vehicle_data.Class = ""
    policy_vehicle_data.AnnualMileage = Vehicle.AnnualMileage

    VehicleDriverID = ""
    for VehDrv in range(len(Vehicle.Drivers)):
        if Vehicle.Drivers[VehDrv].PublicID == Vehicle.PrimaryDriver.PublicID:
            VehicleDriverID = Vehicle.Drivers[VehDrv].PolicyDriver.PublicID

    policy_vehicle_data.YouthfulOperator = ""

    policy_vehicle_data.DriverAge = Drivers[0].Age
    policy_vehicle_data.Gender = Drivers[0].Gender
    policy_vehicle_data.MaritalStatus = Drivers[0].MaritalStatus
    policy_vehicle_data.LicenseDate = ""
    policy_vehicle_data.PercentageDriven = ""

    for Driver in range(len(Drivers)):
        if Drivers[Driver].PublicID == VehicleDriverID:
            policy_vehicle_data.DriverAge = Drivers[Driver].Age
            policy_vehicle_data.Gender = Drivers[Driver].Gender
            policy_vehicle_data.MaritalStatus = Drivers[Driver].MaritalStatus
            policy_vehicle_data.LicenseDate = ""
            for VehDriver in range(len(Drivers[Driver].VehicleDrivers)):
                if Drivers[Driver].VehicleDrivers[VehDriver] == Vehicle.PublicID:
                    policy_vehicle_data.PercentageDriven = Drivers[Driver].VehicleDrivers[VehDriver].PercentageDriven
    
    policy_vehicle_data.NumOperatorOnVehicle = len(Vehicle.Drivers)

    policy_vehicle_data.NumMajorConvictions = ""
    policy_vehicle_data.NumMinorConvictions = ""
    policy_vehicle_data.NumAtFaultAccidentBI = ""
    policy_vehicle_data.NumAtFaultAccidentPD = ""
    policy_vehicle_data.LicenseDateAddDriver1 = ""
    policy_vehicle_data.PercentageDrivenAddDriver1 = ""
    policy_vehicle_data.EligibilityPointsAddDriver1 = ""
    policy_vehicle_data.NumAtFaultAccidentBIAddDriver1 = ""
    policy_vehicle_data.NumAtFaultAccidentPDAddDriver1 = ""
    policy_vehicle_data.LicenseDateAddDriver2 = ""
    policy_vehicle_data.PercentageDrivenAddDriver2 = ""
    policy_vehicle_data.EligibilityPointsAddDriver2 = ""
    policy_vehicle_data.NumAtFaultAccidentBIAddDriver2 = ""
    policy_vehicle_data.NumAtFaultAccidentPDAddDriver2 = ""

    for VehCov in range(len(Vehicle.Coverages)):
        match Vehicle.Coverages[VehCov].PatternCode:
            case "PACollisionCov":
                for VehCovTerm in range(len(Vehicle.Coverages[VehCov].CovTerms)):
                    match Vehicle.Coverages[VehCov].CovTerms[VehCovTerm].PatternCode:
                        case "PACollDeductible":
                            policy_vehicle_data.CollisionDeductibleAmt = Vehicle.Coverages[VehCov].CovTerms[VehCovTerm].ValueAsString
            case "PAComprehensiveCov":
                for VehCovTerm in range(len(Vehicle.Coverages[VehCov].CovTerms)):
                    match Vehicle.Coverages[VehCov].CovTerms[VehCovTerm].PatternCode:
                        case "PACompDeductible":
                            policy_vehicle_data.ComprehensiveDeductibleAmt = Vehicle.Coverages[VehCov].CovTerms[VehCovTerm].ValueAsString
            case "PARentalCov":
                for VehCovTerm in range(len(Vehicle.Coverages[VehCov].CovTerms)):
                    match Vehicle.Coverages[VehCov].CovTerms[VehCovTerm].PatternCode:
                        case "PARental":
                            policy_vehicle_data.TowingRentalLimit = Vehicle.Coverages[VehCov].CovTerms[VehCovTerm].ValueAsString

    VehModifiers = []
    for Modifier in range(len(Vehicle.PAVehicleModifiers)):
        VehModifiers.append(Vehicle.PAVehicleModifiers[Modifier].PatternCode)
    policy_vehicle_data.VehicleModifiers = VehModifiers

    out_path = "C:\ProjectAlphaExtract\Output\PolicyVehicle.txt"
    write_json(out_path, policy_vehicle_data)
