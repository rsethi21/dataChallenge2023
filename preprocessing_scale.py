import pandas as pd
import argparse
from sklearn.preprocessing import MaxAbsScaler
import pickle
import os

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--male", help="path to input csv male", required=True)
parser.add_argument("-f", "--female", help="path to input csv female", required=True)
parser.add_argument("-c", "--columns", help="columns to scale", nargs="*", required=False, default=None)
parser.add_argument("-o", "--output", help="path to output folder", required=False, default=".")

def scale_columns(data, columns, scaler=None):
    if scaler == None:
        scaler = MaxAbsScaler()
    transformed = scaler.fit_transform(data.loc[:,columns])
    transformed = pd.DataFrame(transformed, columns=columns)
    for col in columns:
        data.loc[:,col] = transformed.loc[:,col]
    return scaler


if __name__ == "__main__":
    
    args = parser.parse_args()
    print("Opening Male and Female Data...")
    male_data = pd.read_csv(args.male)
    female_data = pd.read_csv(args.female)
    
    print("Scaling columns...")
    if args.columns != None:
        male_scaler = scale_columns(male_data, args.columns)
        female_scaler = scale_columns(female_data, args.columns)
        with open(os.path.join(args.output, "male_scaler.pkl"), "wb") as male_scaler_file:
            pickle.dump(male_scaler, male_scaler_file)
        with open(os.path.join(args.output, "female_scaler.pkl"), "wb") as female_scaler_file:
            pickle.dump(female_scaler, female_scaler_file)
    
    print("Saving data...")
    male_data.to_csv(os.path.join(args.output, "scaled_male_data.csv"))
    female_data.to_csv(os.path.join(args.output, "scaled_female_data.csv"))
