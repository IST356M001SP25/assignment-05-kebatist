
#TODO Write your extraction code here
'''
- For each file you extract save it in `.csv` format with a header to the `cache` folder. The basic process is to read the file, add lineage, then write as a `.csv` to the `cache` folder. 
- Extract the states with codes google sheet. Save as `cache/states.csv`
- Extract the survey google sheet, and engineer a `year` column from the `Timestamp` using the `extract_year_mdy` function in `pandaslib.py`. Then save as `cache/survey.csv`
- For each unique year in the surveys: extract the cost of living for that year from the website, engineer a `year` column for that year, then save as `cache/col_{year}.csv` for example for `2024` it would be `cache/col_2024.csv`
'''
# This code is used to extract the data from the csv files and clean it.
import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl

# Read the data from the google sheet
surveys = pd.read_csv("https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv")
# print(url.head())

# Save the data to a csv file
surveys['year'] = surveys['Timestamp'].apply(pl.extract_year_mdy)
# Save the data to a csv file
surveys.to_csv('cache/survey.csv', index=False)

#extract unqiue years from the survey data
multiple_years = surveys['year'].unique()

# Iterate over each year to fetch and save cost of living data
for mutiple_year in multiple_years:
    # Retrieve cost of living data for the given year
    col_url = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={mutiple_year}&displayColumn=0")
    col_url = col_url[1]

    # Add a 'year' column to the dataset
    col_url['year'] = mutiple_year
    # Save the cost of living data to the cache directory
    col_url.to_csv(f'cache/col_{mutiple_year}.csv', index=False)

    # extract states from the csv
    link="https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"
    state_data = pd.read_csv(link)
    # save csv to cache folder as "states.csv"
    state_data.to_csv ('cache/states.csv', index=False)

'''
# Load survey data from Google Sheets
survey_link = 'https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv'
survey_data = pd.read_csv(survey_link)

# Create a 'year' column using the extract_year_mdy function
survey_data['year'] = survey_data['Timestamp'].apply(lambda timestamp: pl.extract_year_mdy(timestamp))

# Save the processed survey data to the cache directory
survey_data.to_csv('cache/survey.csv', index=False)

# Identify unique years in the survey data
distinct_years = survey_data['year'].dropna().unique()

# Iterate over each year to fetch and save cost of living data
for distinct_year in distinct_years:
    # Retrieve cost of living data for the given year
    cost_of_living_data = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={distinct_year}&displayColumn=0")[1]
    
    # Add a 'year' column to the dataset
    cost_of_living_data['year'] = distinct_year
    
    # Save the cost of living data to the cache directory
    cost_of_living_data.to_csv(f'cache/col_{distinct_year}.csv', index=False)
    '''

'''This code is used to extract the data from the csv files and clean it.
for i in range(1, 4):
    # read the data from the csv file
    df = pd.read_csv(f'data/part-{i}.csv', sep=',', header=None)
    # rename the columns
    df.columns = ['timestamp', 'country', 'currency', 'amount']
    # clean the currency column
    df['amount'] = df['amount'].apply(pl.clean_currency)
    # clean the country column
    df['country'] = df['country'].apply(pl.clean_country_usa)
    # extract the year from the timestamp column
    df['year'] = df['timestamp'].apply(pl.extract_year_mdy)
    # drop the timestamp column
    df.drop(columns=['timestamp'], inplace=True)
    # save the cleaned data to a new csv file
    df.to_csv(f'data/cleaned_part-{i}.csv', index=False)
    # print the cleaned data
    print(f'cleaned_part-{i}.csv')
    print(df.head())
    print()
'''


