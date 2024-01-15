import argparse
import os
import pandas as pd
from tqdm import tqdm
import statistics
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--male", help="input path to male dataframe", required=True)
parser.add_argument("-f", "--female", help="input path to female dataframe", required=True)

def days_engineered(data):
  month_dictionary = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
  years = []
  months = []
  rough_dates = []
  for entry in data.loc[:,"Date"]:
    year = entry[-4:]
    month = entry.split(" ")[1]
    years.append(year)
    months.append(month_dictionary[month[0:3]])
    rough_date = datetime.date(int(year), int(month_dictionary[month[0:3]]), 1)
    rough_dates.append((datetime.date(2024, 7, 1) - rough_date).days)
  data["years"] = years
  data["months"] = months
  data["days_till_paris"] = rough_dates
  data.drop(columns=["Date"], inplace=True)

def convert_names(data):
  names = []
  for i, entry in data.iterrows():
    try:
      names.append(f"{entry.FirstName.upper()} {entry.LastName.upper()}")
    except:
      names.append(f"{entry.FirstName} {entry.LastName}")
  data["names"] = names
  data.drop(columns=["FirstName", "LastName", "Gender"], inplace=True)

def create_datetime_separated(data):
  list_of_dataframes = []
  years = ["2022", "2023"]
  months = [2, 3, 4, 5, 6, 7, 8, 9, 10]
  for year in years:
    for month in months:
      time_temp_data = data[(data["years"] == year) & (data["months"] == month)].reset_index(inplace=False)
      time_temp_data.drop(columns=["years", "months"])
      if len(time_temp_data) != 0:
        list_of_dataframes.append(time_temp_data)
  data.drop(columns=["years", "months"], inplace=True)
  return list_of_dataframes

def rof_engineered(times, data):
  time_dictionary = {}
  for time in tqdm(times):
    for i, entry in time.iterrows():
      apparatus = entry.Apparatus
      last = entry.names
      key = f"{apparatus}_{last}"
      if key not in time_dictionary.keys():
        time_dictionary[key] = [(entry.days_till_paris, entry.Score)]
      else:
        time_dictionary[key].append((entry.days_till_paris, entry.Score))
  data["rate_of_change"] = [None for _ in range(len(data.index))]
  for key, value in tqdm(time_dictionary.items()):
    apparatus, name = key.split("_")
    try:
        arof = (value[-1][1] - value[0][1]) / abs(value[-1][0] - value[0][0])
    except:
        arof = 0
    entries = data[(data.Apparatus == apparatus)&(data.names == name)].index
    for i in entries:
      data.loc[i,"rate_of_change"] = arof

def average_ranks(data):
    rank_dictionary = {}
    for i, entry in data.iterrows():
      apparatus = entry.Apparatus
      last = entry.names
      key = f"{apparatus}_{last}"
      if key not in rank_dictionary.keys():
        rank_dictionary[key] = [entry.Rank]
      else:
        rank_dictionary[key].append(entry.Rank)
    data["average_apparatus_rank"] = [0 for _ in range(len(data.index))]
    for key, value in tqdm(rank_dictionary.items()):
        apparatus, name = key.split("_")
        average = sum(value)/len(value)
        entries = data[(data.Apparatus == apparatus)&(data.names == name)].index
        for i in entries:
            data.loc[i,"average_apparatus_rank"] = average
    data["average_apparatus_rank"].fillna(0, inplace=True)

if __name__ == "__main__":
    args = parser.parse_args()
    male_data = pd.read_csv(args.male)
    female_data = pd.read_csv(args.female)
    
    days_engineered(female_data)
    convert_names(female_data)
    time_list = create_datetime_separated(female_data)
    rof_engineered(time_list, female_data)
    average_ranks(female_data)

    days_engineered(male_data)
    convert_names(male_data)
    time_list = create_datetime_separated(male_data)
    rof_engineered(time_list, male_data)
    average_ranks(male_data)
    
    male_data.to_csv("processed_male_data.csv")
    female_data.to_csv("processed_female_data.csv")
