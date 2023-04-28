import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.write("# Welcome to my research quick help streamlit app 👋")

st.sidebar.success("Select a analysis script from the sidebar to begin")

st.markdown(
    """
    # Research-scripts
General purpose scripts to aid in the analysis of a clinical trial that uses questionnaires to assess participants.

The scripts are used to create a streamlit multipage app where you can upload CSV/XLSX files containing trial/research participant's answers to questionnaires along with other data.
The CSV/XLSX file has to be constructed in the following format: the index has 2 levels - the first is user ID and the second a date when the row's data was collected.
Each column's title is a research question and the data itself is each user's answers to the questions in numerical form.
CSV template for the uploaded file:

| First Index   | Second Index  | Question 1    | Question 2    | 
| ------------- | ------------- | ------------- | ------------- | 
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
"""
)