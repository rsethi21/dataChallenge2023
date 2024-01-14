import pandas as pd
import argparse
from sklearn.preprocessing import MaxAbsScaler
from sklearn.model_selection import train_test_split
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--male", help="path to input csv male", required=True)
parser.add_argument("-f", "--female", help="path to input csv female", required=True)
parser.add_argument("-c", "--columns", help="columns to scale", nargs="*", required=False, default=None)
# parser.add_argument("-s", "--split", help="train split out of 100", required=False, type=int, default=80)

def scale_columns(data, columns, scaler=None):
    if scaler == None:
        scaler = MaxAbsScaler()
    transformed = scaler.fit_transform(data.loc[:,columns])
    transformed = pd.DataFrame(transformed, columns=columns)
    for col in columns:
        data.loc[:,col] = transformed.loc[:,col]
    return scaler

def separate(data):
    '''
    competition_list = data.Competition.unique()
    X_train, X_test = train_test_split(competition_list, train_size=percent_train/100.0, random_state=2024)
    train_indices = [i for i, entry in data.iterrows() if entry.Competition in X_train]
    test_indices = [i for i, entry in data.iterrows() if entry.Competition in X_test]
    return data.loc[train_indices,:].reset_index(inplace=False), data.loc[test_indices,:].reset_index(inplace=False)
    '''
    competition_to_use = "2022 U.S. Classic"
    Country = "USA"
    Round = "AAfinal"
    test_indices = list(data[(data.Competition==competition_to_use) & (data.Country==Country) & (data.Round==Round)].index)
    train_indices = [i for i in data.index if i not in test_indices]
    return data.loc[train_indices,:], data.loc[test_indices,:]

if __name__ == "__main__":
    
    args = parser.parse_args()
    male_data = pd.read_csv(args.male)
    female_data = pd.read_csv(args.female)
    
    if args.columns != None:
        male_scaler = scale_columns(male_data, args.columns)
        female_scaler = scale_columns(female_data, args.columns)
        with open("male_scaler.pkl", "wb") as male_scaler_file:
            pickle.dump(male_scaler, male_scaler_file)
        with open("female_scaler.pkl", "wb") as female_scaler_file:
            pickle.dump(female_scaler, female_scaler_file)

    train_male, test_male = separate(male_data)
    train_female, test_female = separate(female_data)

    train_male.to_csv("./train_male_data.csv", index=True)
    test_male.to_csv("./test_male_data.csv", index=True)
    train_female.to_csv("./train_female_data.csv", index=True)
    test_female.to_csv("./test_female_data.csv", index=True)
