from datetime import date, datetime

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from scipy.interpolate import UnivariateSpline


# read data
back_data = pd.read_csv("Back.csv")
biceps_data = pd.read_csv("Biceps.csv")
chest_data = pd.read_csv("Chest.csv")
daily_data = pd.read_csv("Daily.csv")
legs_data = pd.read_csv("Legs.csv")
shoulders_data = pd.read_csv("Shoulders.csv")
triceps_data = pd.read_csv("Triceps.csv")

# merge data into one
all_data = pd.merge(back_data, biceps_data, on="Date", how="outer")
all_data = pd.merge(all_data, chest_data, on="Date", how="outer")
all_data = pd.merge(all_data, daily_data, on="Date", how="outer")
all_data = pd.merge(all_data, legs_data, on="Date", how="outer")
all_data = pd.merge(all_data, shoulders_data, on="Date", how="outer")
all_data = pd.merge(all_data, triceps_data, on="Date", how="outer")

all_data = all_data.fillna(0)
all_data.set_index("Date")

# format date as datetime and sort in chronological order
all_data["Date"] = all_data["Date"].apply(lambda row: datetime.strptime(row, "%d/%m/%Y"))
all_data.sort_values(by="Date", inplace=True)

# data currently array of values in each cell. Average data in each cell to get number for further use
def average_values(row, delimiter):
    row = str(row)
    try:
        values = float(row)
        return values
    except ValueError:
        values = row.split(delimiter)
        values = [float(value) for value in values]
        return sum(values)/len(values)

for column in all_data.columns[1:]:
    if column == "Woodchoppers":
        all_data[column] = all_data[column].apply(lambda row: average_values(row, " "))
    else:
        all_data[column] = all_data[column].apply(lambda row: average_values(row, "."))


for column in all_data.columns[1:]:
    all_data[column].replace(to_replace=0, method="ffill", inplace=True)

print(all_data.head())

# interpolation
x = np.linspace(0, 1, len(all_data["Date"]))

# just initialising estimates DF, then filling up in for loop below
estimates = pd.DataFrame(all_data["Date"])
for column in all_data.columns[1:]:
    interp_fn = UnivariateSpline(x, all_data[column], k=5)
    estimates[column] = interp_fn(x)


# visualisation
back_exercises = back_data.columns[1:]
bicep_exercises = biceps_data.columns[1:]
chest_exercises = chest_data.columns[1:]
daily_exercises = daily_data.columns[1:]
leg_exercises = legs_data.columns[1:]
shoulder_exercises = shoulders_data.columns[1:]
tricep_exercises = triceps_data.columns[1:]

columns_to_plot = shoulder_exercises

for column in columns_to_plot:
    sns.scatterplot(data=all_data, x="Date", y=column)
    sns.lineplot(data=estimates, x="Date", y=column)
plt.legend(columns_to_plot)
plt.show()

