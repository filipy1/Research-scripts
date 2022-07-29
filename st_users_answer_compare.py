from unittest import skip
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

### A script to compare between participant's answers with an interactive graph.
col1, col2 = st.columns(2)
uploaded_file = col1.file_uploader(
    "Choose a DB CSV file"
)  # Uploading a CSV file as a data-base

df = pd.read_csv(
    uploaded_file,
    index_col=[0, 1],
    parse_dates=True,
    dayfirst=True,
)

### Optional to add another CSV file representing the different groups in the information 
try:
    group_upload = col2.file_uploader(
            'Upload a CSV built from with 2 columns: "User ID" and "Group type" (e.g. sham/real)',
        )
    group_df = pd.read_csv(group_upload)
except:
    col2.write('No User group CSV was provided')
    group_df = None


def create_indiviudal_user_dfs(df):
    """Create a dictionary where keys are user_n and values and individual answer df for that user."""
    users_dfs = {}
    for user in df.index.get_level_values(0).drop_duplicates():  # Used later
        users_dfs[f"{user}"] = df.loc[df.index.get_level_values(0) == user]
    return users_dfs


def question_comprasion(df, device_type_df=None):
    """A function to help compare and plot the answers of all participants answers for a specific question."""

    col1, col2 = st.columns(2)
    radio_option = col1.radio(
        "Which question would you like to compare between USERS?", df.columns
    )
    try:
        group_options = ['All'] + list((device_type_df.iloc[:, 1].drop_duplicates())) 
        group_radio = col2.radio('Choose which device type group to draw a graph for', ['All', 'By group'])
    except:
        group_radio = 'All'
        col2.subheader('No group CSV provided')
        
    if group_radio == 'All':
        df_column = df[radio_option].reset_index()
        df_column.dropna(axis=0, inplace=True)
        fig = px.line(
            df_column,
            x='Date',
            y=radio_option,
            color="User ID",
            line_dash="User ID",
            markers=True,
            title="All participants"
        )
        st.plotly_chart(fig, use_container_width=True)
        return
    
    else:
        cont = st.container()
        for i, group in enumerate(group_options[1:]):
            users_to_show = device_type_df[device_type_df.iloc[:, 1] == group]
            usr_lst = users_to_show.iloc[:, 0].tolist()
            sliced_df = df.loc[usr_lst]
            df_column = sliced_df[radio_option].reset_index()
            df_column.dropna(axis=0, inplace=True)
            fig = px.line(
                df_column,
                x='Date',
                y=radio_option,
                color="User ID",
                line_dash="User ID",
                markers=True,
                title=f'Showing {group} devices'
        ) 
            cont.plotly_chart(fig, use_container_width=True)
        return

question_comprasion(df, group_df)
