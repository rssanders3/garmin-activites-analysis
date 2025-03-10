# garmin-activites-analysis
A Project that can be used to export data from Garmin and Analyze the historical data

# Setup

## Python & Venv
This is a Python Project, and would require Python to be installed locally along with Virtual Env

## Credentials and Configs
Create a `.env` file locally. You can use the `.env.sample` file that exists as a template and then update the file as needed:
```
cp .env.sample .env
```
Then update `.env` file

# Execution

This project consists of two steps for Execution. 
Step 1 extracts the Garmin data as a CSV file for the user credentials given in the `.env` file
Step 2 is a notebook that loads the CSV data as a Pandas Data Frame and allows you to review it

## Step 1: Exporting Data to Local
After setting up the Python Virtual Environment and updating the `.env` file, run the `1-garmin-activites-export.py` file. This will extract all data from Garmin for the user defined in the `.env` file and extract the data to the `data/` directory. 
Note: Data will be saved in the format `garmin_activities_YYYY_MM_DD_HH_MM_SS.csv`

## Step 2: Analyzing Data
After extracting the data, you can then use the `2-garmin-activites-analysis.ipynb` Python Notebook to perform your analysis on the data that was ectracted. 
The first cell loads all requried imports
The second cell loads the data into a Pandas Dataframe (note: by default if you dont cahgne anything, the notebook will load the latest data file in the `data/` directory, but if you want to process a specific/past data file, you can manually set a value to the `FILE_TO_LOAD` variable)
At the moment the rest of the cells are setup to list the amount of time by week you are at a specific heart rate zone. But you can enhance this and adjust to answer the specific question you have.

