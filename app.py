import os
from addict import Dict
from Lob.Auto.PolicyLine import extract_policy_line_data
from Lob.Auto.PolicyPremium import extract_premium_data
from Lob.Auto.PolicyVehicle import extract_vehicle_data
from Utils.ReadJson import read_json

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def extract_input_policy_transaction():

    path = "C:\ProjectAlphaExtract\Input"
    files = os.listdir(path)
    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            file_path = os.path.join(path, file)
            policy_data = read_json(file_path)
            extract_policy_line_data(policy_data)
            extract_policy_vehicle_data(policy_data)

def extract_policy_vehicle_data(policy_data):
    
    policy_data_dict = Dict(policy_data)

    FirstCarOnPolicy = policy_data_dict.Lines[0].Vehicles[0].VehicleNumber

    for Veh in range(len(policy_data_dict.Lines[0].Vehicles)):
        if policy_data_dict.Lines[0].Vehicles[Veh].VehicleNumber < FirstCarOnPolicy:
            FirstCarOnPolicy = policy_data_dict.Lines[0].Vehicles[Veh].VehicleNumber

    for Veh in range(len(policy_data_dict.Lines[0].Vehicles)):
        extract_vehicle_data(policy_data_dict.PublicID, policy_data_dict.Lines[0].Vehicles[Veh], policy_data_dict.Lines[0].PolicyDrivers)
        extract_premium_data(policy_data_dict.PublicID, policy_data_dict.Lines[0].Vehicles[Veh], policy_data_dict.Lines[0].PACosts, FirstCarOnPolicy)
    
if __name__ == "__main__":
    
    extract_input_policy_transaction()

