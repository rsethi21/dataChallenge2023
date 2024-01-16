# dataChallenge2023

## Requirements
- You must find a may to install these packages (either in a virtual environment, conda environment, or locally
- Python:
	- pandas
	- tqdm
	- argparse
	- scikit-learn
- R:
	- dplyr

## Scripts
- ./scripts/preprocessing_clean.py: cleans up irregularities in data
- ./scripts/preprocessing_engineering.py: adds three new engineered columns
	- ROF: rate of change which captures the change in the gymnasts' scores over time in a specific apparatus; this captures trends in gymnast performances in specific apparatuses (over the 12 different competition between 2/2022-10/2023)) and will be useful in determining performance in 2024
	- Average Rank in Apparatus: this captures the average performance of gymnast in the specific apparatus; this captures how well a gymnast does in specific events and will be useful in determining performance in 2024
	- Days till Paris: this captures how many days away from the paris 2024 olympics are from the competition date in the data; this captures how performance of a gymnast could change over time
- ./scripts/preprocessing_scale.py: scales data between 0, 1 and -1, 1 to ensure columns don't overpower each other
- ./scripts/model_n_predict.R: this script creates a linear model that takes in the gymnast name, location of event, days till paris olympics, country, ROF, Average Rank in Apparatus, apparatus, and round to predict the gymnast's score; we train this on the data provided, evaluate its performance and viability, and deploy to predict score for gymnasts
- ./scripts/FormingTeams.R: this script takes he data from model_n_predict and finds the best team based off of the predictions. The team is created by ranking the top athletes in each apparatus and finds a team that is excellent in as many events as possible.
## How to Run
```
- Generally:
python3 ./scripts/preprocessing_clean.py -i input/path -o output/path
- Example:
python3 ./scripts/preprocessing_clean.py -i ./input_data/data_2022_2023.csv -o ./output_data/
```
```
- Generally:
python3 ./scripts/preprocessing_engineering.py -m male/input/path -f female/input/path -o output/path
- Example:
python3 ./scripts/preprocessing_engineering.py -m ./output_data/cleaned_mens_data.csv -f ./output_data/cleaned_womens_data.csv -o ./output_data/
```
```
- Generally:
python3 ./scripts/preprocessing_scale.py -m male/input/path -f female/input/path -c column/names/space/delimited -o output/path
- Example:
python3 ./scripts/preprocessing_scale.py -m ./output_data/processed_male_data.csv -f ./output_data/processed_female_data.csv -c Score days_till_paris average_apparatus_rank rate_of_change -o ./output_data
```
```
- Generally:
Rscript ./scripts/model_n_predict.R path/to/male/or/female/data path/to/list/of/male/or/female/usa/names path/to/list/of/male/or/female/apparatus path/to/rounds/list output/path
- Example:
	- Female Data:
	Rscript ./scripts/model_n_predict.R ./output_data/scaled_female_data.csv ./input_data/usa_female_namelist.csv ./input_data/women_apparatus.csv ./input_data/rounds.csv ./output_data/female_predictions.csv
	- Male Data:
	Rscript ./scripts/model_n_predict.R ./output_data/scaled_male_data.csv ./input_data/usa_male_namelist.csv ./input_data/men_apparatus.csv ./input_data/rounds.csv ./output_data/male_predictions.csv
```
```
- Generally:
Rscript FormingTeams.R path/to/male/data path/to/female/data
- Example:
Rscript FormingTeams.R ./output_data/male_predictions.csv ./output_data/female_predictions.csv
```
