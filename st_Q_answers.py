from datetime import timedelta
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates

file_col1, file_col2 = st.columns(2)  # setting up columns to put file widgets on.

uploaded_first_baseline = file_col1.file_uploader("Choose a baseline data CSV file")

uploaded_file = file_col2.file_uploader("Choose a DB CSV file")


def handling_no_baseline(uploaded_baseline):
    """Handling the uploaded baseline widget if no file is uploaded"""
    if (
        uploaded_baseline != None
    ):  # no file uploaded means the baseline file var will be NONE
        baseline_df = pd.read_csv(uploaded_baseline, index_col=["User"])
    else:
        baseline_df = None
    return baseline_df


df = pd.read_csv(
    uploaded_file,
    index_col=[0, 1],
    parse_dates=True,
    dayfirst=True,
)
df.tail()

df["Week"] = np.nan
week_count = 1
day_count = 1
for n in range(0, len(df)):
    date_bool = (
        df.index.get_level_values(1)[n] - df.index.get_level_values(1)[n - 1]
    ) >= timedelta(3)
    match date_bool:
        case True:  ## This Section handles creating a "week in trial" column by using the dates given a part of the index
            week_count += 1  ## Sunday is the first day of the week!!!!
            df.iloc[n, -1] = week_count
        case False:
            df.iloc[n, -1] = week_count


def create_indiviudal_user_dfs(df):
    """Create a dictionary where keys are user_n and values and individual answer df for that user."""
    users_dfs = {}
    for user in df.index.get_level_values(0).drop_duplicates():  # Used later
        users_dfs[f"{user}"] = df.loc[df.index.get_level_values(0) == user]
    return users_dfs


def user_string_input(df):
    """Creating a text_input for users"""
    st.write(
        f"Data available for users {sorted(list(df.index.get_level_values(0).drop_duplicates()))}"
    )
    user_number = st.text_input("Show data for user:", "1")
    return user_number


def bar_graph_data(df, user_n="1", base_line=None):
    """A function that draws a bar plot where the x axis is the week number and the y axis is the question's answer.
    Streamlit functionality is to only choose the questions you want to see answers for right now."""

    col1, col2 = st.columns(2)  # 2 columns for smoother look

    users_dfs = create_indiviudal_user_dfs(
        df
    )  # Dictionary of DF's for every user in the CSV
    try:
        user = users_dfs[user_n]
        user.set_index(user.index.get_level_values(1), inplace=True)
        if base_line.iloc[0, 0] != None:
            col1.subheader(r"Baseline answers:")
            col1.write(base_line.loc[int(user_n)])
    except KeyError:  # Handling a key error that arises when the user inputs an invalid user ID
        if "" in user_n:
            st.subheader(
                f"ERROR: {user_n} is not found in the selected data-base CSV file"
            )
        else:
            st.subheader(f"ERROR:{type(user_n)} is an invalid user index")
        return
    except AttributeError:  # Handling an attribute error when there's no baseline csv file
        col1.subheader("Missing Baseline CSV file")
        pass

    # st.write(user)
    grouped_week = user.groupby(
        "Week", dropna=False
    ).sum()  # Preping dataframe for weekly answers visualization
    grouped_week.drop("Pain VAS", axis=1, inplace=True)

    bar_graph_dict = {}
    plt.figure(figsize=(8, 8))
    N = len(grouped_week.index)
    ind = np.arange(N)
    width = 0.05

    col2.write("Choose questions to view the answers for:")
    all = col2.checkbox(
        "all"
    )  # Creating checkboxes for every column in our DF and an option to select 'all'.
    if all:
        questions_lst = df.columns[1:-1]
        for question in df.columns[1:-1]:
            checkbox = col2.checkbox(question)

    else:
        questions_lst = []
        for question in df.columns[1:-1]:
            checkbox = col2.checkbox(question)
            if checkbox:
                questions_lst.append(question)

    ### Plotting everything on graphs

    fig, ax = plt.subplots(sharex=True, figsize=(15, 6))
    for i, column in enumerate(questions_lst):

        vals = grouped_week[column]
        bar = ax.bar(ind + width * i, vals, width)
        bar_graph_dict[column] = bar

    plt.xlabel("Week")
    plt.ylabel("Answers")
    plt.title(f"Answers by week, {user_n}")

    plt.xticks(ind + width * 5, list(grouped_week.index))
    plt.legend((bar_graph_dict.values()), (questions_lst))
    st.pyplot(fig)


def pain_vas_graph(df, user_n="1"):
    """A function to draw the pain VAS answers we collect each day (in contrast to the OWESTRY questions we collect once a week"""
    users_dfs = create_indiviudal_user_dfs(df)
    user = users_dfs[user_n]
    user.set_index(user.index.get_level_values(1), inplace=True)
    fig, ax = plt.subplots(figsize=(15, 6))
    ax = sns.lineplot(x=user.index, y=user["Pain VAS"])
    ax.set_xticklabels(user.index, rotation=45)
    myFmt = mdates.DateFormatter("%d-%m-%y")
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_title(f"Pain VAS by date, {user_n}")
    st.pyplot(fig)


baseline_df = handling_no_baseline(uploaded_first_baseline)
user_ = user_string_input(df)
bar_graph_data(df, user_, base_line=baseline_df)
pain_vas_graph(df, user_)
