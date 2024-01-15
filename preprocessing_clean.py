import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file path", required=True)
parser.add_argument("-o", "--output", help="output folder path", required=False, default=".")

if __name__ == "__main__":
    args = parser.parse_args()
    data = pd.read_csv(args.input)

    apparatus_dictionary = {"VT1": "VT", "VT2": "VT"}
    for i,entry in data.iterrows():
        a = entry.Apparatus.upper()
        if a in apparatus_dictionary.keys():
            data.loc[i,"Apparatus"] = apparatus_dictionary[a]
        else:
            data.loc[i, "Apparatus"] = a
        data.loc[i, "FirstName"] = entry.FirstName.upper()
        data.loc[i, "LastName"] = entry.LastName.upper()
    data.drop(columns=["D_Score", "E_Score", "Penalty"], inplace=True)

    male = data.loc[:,data.Gender == "m"]
    female = data.loc[:,data.Gender == "f"]

    male.to_csv(os.path.join(f"{args.output}", "cleaned_mens_data.csv"))
    female.to_csv(os.path.join(f"{args.output}", "cleaned_womens_data.csv"))
