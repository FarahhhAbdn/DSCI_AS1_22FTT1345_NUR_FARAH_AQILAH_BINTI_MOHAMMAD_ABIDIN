import streamlit as st
import pandas as pd

# Load your dataset
df = pd.read_csv('cause_of_deaths.csv')

# Main Dashboard
st.title('Health Statistics Dashboard')

# Creating new column for the total number of deaths (Sum all cause of deaths)
cause_of_deaths = [col for col in df.columns if col not in ('Country/Territory', 'Code', 'Year')]
df['Total Deaths'] = df[cause_of_deaths].sum(axis=1)

# Display total deaths from 1990 to 2019
total_deaths = df.groupby('Year')['Total Deaths'].sum().loc[1990:2019].sum()
st.write(f'Total Deaths from 1990 to 2019: {total_deaths}')

selected_country = st.selectbox('Select Country', df['Country/Territory'].unique())

# Filter data for the selected country
selected_country_data = df[df['Country/Territory'] == selected_country]

# Line Plot: Total Deaths Over Time (all years)
st.subheader(f'Total Deaths Over Time ({selected_country})')
st.line_chart(selected_country_data.groupby('Year')['Total Deaths'].sum())

# Bar Plot: Total Cases of Diseases
st.subheader('Total Cases of Diseases')
disease_totals = df[cause_of_deaths].sum().sort_values(ascending=True)
st.bar_chart(disease_totals)

# Separate between death caused by accident and illness
accident_death_columns = ['Drowning', 'HIV/AIDS', 'Drug Use Disorders', 'Alcohol Use Disorders',
                           'Conflict and Terrorism', 'Poisonings', 'Fire, Heat, and Hot Substances',
                           'Self-harm', 'Road Injuries', 'Environmental Heat and Cold Exposure', 'Interpersonal Violence',
                           'Exposure to Forces of Nature']

illness_death_columns = ['Meningitis', 'Alzheimers Disease and Other Dementias', 'Parkinsons Disease',
                         'Nutritional Deficiencies', 'Malaria', 'Maternal Disorders', 'Tuberculosis',
                         'Cardiovascular Diseases', 'Lower Respiratory Infections', 'Neonatal Disorders',
                         'Diarrheal Diseases', 'Neoplasms', 'Diabetes Mellitus', 'Chronic Kidney Disease',
                         'Protein-Energy Malnutrition', 'Chronic Respiratory Diseases',
                         'Cirrhosis and Other Chronic Liver Diseases', 'Digestive Diseases', 'Acute Hepatitis']

# Create DataFrames for accident deaths and illness deaths
accident_Deaths = selected_country_data[accident_death_columns].sum()
illness_Deaths = selected_country_data[illness_death_columns].sum()

# Create separate bar plots for accident deaths and illness deaths
st.subheader('Total Cases of Accident Deaths')
st.bar_chart(accident_Deaths)

st.subheader('Total Cases of Illness Deaths')
st.bar_chart(illness_Deaths)

# Select data from Top 10 countries that have the highest number of deaths
Top10_deaths = df.groupby('Country/Territory')['Total Deaths'].sum().nlargest(10).reset_index()

# Display the table for Top 10 countries
st.subheader('Top 10 Countries with the Highest Total Deaths')
st.table(Top10_deaths)
