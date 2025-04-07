'''
The bulk of the work is done in the transform process. Here we read our data from the cache back into pandas. From there we will clean the data, engineer new columns, join datasets together, etc all on route to producing a dataset from which we can create the reports. In the final transformation step, we write the reports back to the cache. 
'''

import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

## Load from cache

# Load survey data
survey_data = pd.read_csv('cache/survey.csv')

# Load states data
states_data = pd.read_csv('cache/states.csv')

# Load cost of living (col) data for each year
cols = []
for year in survey_data['year'].unique():
    col = pd.read_csv(f'cache/col_{year}.csv')
    cols.append(col)

# Combine all col data into one DataFrame
col_data = pd.concat(cols, ignore_index=True)
# Clean the country column
survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

# Merge survey data with states data to get state abbreviations
survey_states_combined = survey_data.merge(
    states_data,
    left_on="If you're in the U.S., what state do you work in?",
    right_on='State',
    how='inner'
)

# Create a full city column by combining city, state, and country
survey_states_combined['_full_city'] = (
    survey_states_combined['What city do you work in?'] + ', ' +
    survey_states_combined['Abbreviation'] + ', ' +
    survey_states_combined['_country']
)
# Ensure the 'City' column exists in col_data
if 'City' not in col_data.columns:
    raise KeyError(f"'City' column is missing in col_data. Available columns: {col_data.columns}")

# Merge survey data with cost of living data
combined = survey_states_combined.merge(
    col_data,
    left_on=['year', '_full_city'],
    right_on=['year', 'City'],
    how='inner'
)

# Clean the salary column
combined["_annual_salary_cleaned"] = combined[
    "What is your annual salary? (You'll indicate the currency in a later question. "
    "If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"
].apply(pl.clean_currency)

# Adjust salary based on the cost of living index
combined['_annual_salary_adjusted'] = combined.apply(
    lambda row: row["_annual_salary_cleaned"] * (100 / row['Cost of Living Index']),
    axis=1
)
# Save the combined dataset to a CSV file
combined.to_csv('cache/survey_dataset.csv', index=False)

# Create pivot tables for analysis
annual_salary_adjusted_by_location_and_age = combined.pivot_table(
    index='_full_city',
    columns='How old are you?',
    values='_annual_salary_adjusted',
    aggfunc='mean'
)
annual_salary_adjusted_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

annual_salary_adjusted_by_location_and_education = combined.pivot_table(
    index='_full_city',
    columns='What is your highest level of education completed?',
    values='_annual_salary_adjusted',
    aggfunc='mean'
)
annual_salary_adjusted_by_location_and_education.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')

# Display the education pivot table in Streamlit
st.write(annual_salary_adjusted_by_location_and_education)
'''
# load survey data from cache
survey_data = pd.read_csv('cache/survey.csv')

# load the states data from cache
states_data = pd.read_csv('cache/states.csv')

# load list of col data from cache
cols = []
for year in survey_data['year'].unique():
    col = pd.read_csv(f'cache/col_{year}.csv')
    cols.append(col)

# Transform survey data
survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)
survey_data = survey_data.merge(states_data, left_on="If you're in the U.S., what state do you work in?", right_on='State')
survey_data['_full_city'] = survey_data['What city do you work in?'] + ', ' + survey_data['Abbreviation'] + ', ' + survey_data['_country']

# Merge and adjust salary
col_data = pd.concat(cols)
combined = survey_data.merge(col_data, left_on=['year', '_full_city'], right_on=['year', 'City'])
combined['_salary_adj'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency) * (100 / combined['Cost of Living Index'])

# Save outputs
combined.to_csv('cache/survey_dataset.csv', index=False)
combined.pivot_table(index='_full_city', columns='How old are you?', values='_salary_adj', aggfunc='mean').to_csv('cache/salary_by_location_and_age.csv')
education_pivot = combined.pivot_table(index='_full_city', columns='What is your highest level of education completed?', values='_salary_adj', aggfunc='mean')
education_pivot.to_csv('cache/salary_by_location_and_education.csv')
st.write(education_pivot)

# Load data
survey = pd.read_csv('cache/survey.csv')
states = pd.read_csv('cache/states.csv')
col_data = pd.concat([pd.read_csv(f'cache/col_{y}.csv') for y in survey['year'].unique()])

# Transform survey data
survey['_country'] = survey['What country do you work in?'].apply(pl.clean_country_usa)
survey = survey.merge(states, left_on="If you're in the U.S., what state do you work in?", right_on='State')
survey['_full_city'] = survey['What city do you work in?'] + ', ' + survey['Abbreviation'] + ', ' + survey['_country']

# Merge and adjust salary
combined = survey.merge(col_data, left_on=['year', '_full_city'], right_on=['year', 'City'])
combined['_salary_adj'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency) * (100 / combined['Cost of Living Index'])

# Save outputs
combined.to_csv('cache/survey_dataset.csv', index=False)
combined.pivot_table(index='_full_city', columns='How old are you?', values='_salary_adj', aggfunc='mean').to_csv('cache/salary_by_location_and_age.csv')
education_pivot = combined.pivot_table(index='_full_city', columns='What is your highest level of education completed?', values='_salary_adj', aggfunc='mean')
education_pivot.to_csv('cache/salary_by_location_and_education.csv')
st.write(education_pivot)
'''
