import pandas as pd
import argparse
import os
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file path", required=True)
parser.add_argument("-o", "--output", help="output folder path", required=False, default=".")

if __name__ == "__main__":
    args = parser.parse_args()
    data = pd.read_csv(args.input)

    apparatus_dictionary = {"VT1": "VT", "VT2": "VT"}
    for i,entry in tqdm(data.iterrows(), total=len(data.index), desc="Cleaning Apparatus and Name Columns"):
        a = str(entry.Apparatus).upper()
        if a in apparatus_dictionary.keys():
            data.loc[i,"Apparatus"] = apparatus_dictionary[a]
        else:
            data.loc[i, "Apparatus"] = a
        data.loc[i, "FirstName"] = str(entry.FirstName).upper()
        data.loc[i, "LastName"] = str(entry.LastName).upper()
    data.drop(columns=["D_Score", "E_Score", "Penalty"], inplace=True)

    print("Saving mens and womens gymnastics data separately...")
    male = data.loc[data[data.Gender == "m"].index, :]
    female = data.loc[data[data.Gender == "w"].index, :]

    male.to_csv(os.path.join(args.output, "cleaned_mens_data.csv"))
    female.to_csv(os.path.join(args.output, "cleaned_womens_data.csv"))
