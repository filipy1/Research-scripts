import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates

### A script to check the amount of answers given by each participant during a certain period of the research.
### The aim of this application is to help track compliance, ideally the graph produced will show only 1 straight line.
### If there are multiple lines (meaning there isn't uniform compliance), it means that some participant has missed some questions.

st.set_page_config(
    page_title="Basic compliance check",
)

st.write("# Basic compliance indicator")

st.markdown(
    """A script to check the amount of answers given by each participant during a certain period of the research.
 The aim of this application is to help track compliance, ideally the graph produced will show only 1 straight line.
 If there are multiple lines (meaning there isn't uniform compliance), it means that some participant has missed some questions.
\n You'll need the basic DB file for this script.""")

uploaded_file = st.file_uploader("Choose a Solio DB CSV/XLSX file")

if '.xlsx' in uploaded_file.name:
    df = pd.read_excel(
        uploaded_file,
        index_col= [0,1],
        parse_dates=True,
    )
elif '.csv' in uploaded_file.name:
    df = pd.read_csv(
        uploaded_file,
        index_col=[0, 1],
        parse_dates=True,
        dayfirst=True,
    )


def create_indiviudal_user_dfs(df):
    """Create a dictionary where keys are user_n and values and individual answer df for that user."""
    users_dfs = {}
    for user in df.index.get_level_values(0).drop_duplicates():
        users_dfs[f"user_{user}"] = df.loc[df.index.get_level_values(0) == user]
    return users_dfs


def user_answer_per_date(df):
    """Create a dictionary where keys are user_n and values are dataframes of number
    of questions answered by date by the user"""
    users_dfs = create_indiviudal_user_dfs(df)

    answers_per_day = {}
    for key, df in users_dfs.items():
        df.set_index(df.index.get_level_values(1), inplace=True)
        answers_per_day[key] = df.count(axis=1)
    return answers_per_day


def create_date_widget(df):
    """Creating a date widget to apply to the graph."""
    ts_dfs = user_answer_per_date(df)
    date_w = st.date_input(
        "Date range to plot",
        [
            ts_dfs[list(ts_dfs.keys())[0]].index[0],
            ts_dfs[list(ts_dfs.keys())[0]].index[-1],
        ],
        min_value=ts_dfs[list(ts_dfs.keys())[0]].index[0],
        max_value=ts_dfs[list(ts_dfs.keys())[0]].index[-1],
    )
    return date_w


def create_user_checkbox(df):

    checkbox_dict = {}
    for user in df.index.get_level_values(0).drop_duplicates():
        checkbox_dict[f"user_{user}"] = st.checkbox(f"user_{user}")
    return checkbox_dict


def create_user_multiselect(df):
    idxes = df.index.get_level_values(0).drop_duplicates()
    user_ids = []
    for id in idxes:
        user_ids.append("user_" + str(id))

    container = st.container()
    all = st.checkbox("Select all")

    if all:
        return container.multiselect(
            "Choose USER IDs to see data for", user_ids, user_ids
        )

    return container.multiselect("Choose USER IDs to see data for", user_ids)


def plot_questions_answered(df):
    """A function that plots the number of questions selected users answered each day"""
    individual_users_dict = user_answer_per_date(df)
    answers_per_date = pd.concat(individual_users_dict.values(), axis=1)
    answers_per_date.columns = individual_users_dict.keys()
    # creating indivudal df for each user ID

    start, end = create_date_widget(df)
    users_list = create_user_multiselect(df)

    ts_dfs = {
        user: individual_users_dict[user] for user in users_list
    }  # Time series data frames
    fig, ax = plt.subplots(sharex=True)
    for key, df in ts_dfs.items():
        if end != df.index[-1]:
            df.loc[end] = 0  # Plotting the graph.
        ax = sns.lineplot(data=df.loc[start:end], label=key, legend=False) #legend="brief"
        ax.set(xlabel="Date", ylabel="Number of answers")
        ax.set_xticklabels(df.loc[start:end].index, rotation=45)
        plt.xticks(df.loc[start:end].index)
    myFmt = mdates.DateFormatter("%d-%m-%y")
    ax.xaxis.set_major_formatter(myFmt)
    st.pyplot(fig)


plot_questions_answered(df)
