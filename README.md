# dataChallenge2023

## Requirements
You must find a may to install these packages (either in a virtual environment, conda environment, or locally
Python:
- pandas
- tqdm
- argparse
- scikit-learn
R:
- dpylr

## Scripts
./scripts/preprocessing_clean.py: cleans up irregularities in data
./scripts/preprocessing_engineering.py: adds three new engineered columns
	- ROF: rate of change which captures the change in the gymnasts' scores over time in a specific apparatus; this captures trends in gymnast performances in specific apparatuses (over the 12 different competition between 2/2022-10/2023)) and will be useful in determining performance in 2024
	- Average Rank in Apparatus: this captures the average performance of gymnast in the specific apparatus; this captures how well a gymnast does in specific events and will be useful in determining performance in 2024
./scripts/preprocessing_scale.py: scales data between 0, 1 and -1, 1 to ensure columns don't overpower each other
./scripts/model_n_predict.R: this script creates a linear model that takes in the gymnast name, location of event, days till paris olympics, country, ROF, Average Rank in Apparatus, apparatus, and round to predict the gymnast's score; we train this on the data provided, evaluate its performance and viability, and deploy to predict score for gymnasts
## How to Run
```

```

```
```

```
```

```
```
