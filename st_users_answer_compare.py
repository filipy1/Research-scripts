from datetime import timedelta
from itertools import dropwhile
from re import L
from unittest import skip
from venv import create
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates
import plotly.express as px


uploaded_file = st.file_uploader("Choose a DB CSV file") # Uploading a CSV file as a data-base

df = pd.read_csv(
    uploaded_file,
    index_col=[0, 1],
    parse_dates=True,
    dayfirst=True,
)

def create_indiviudal_user_dfs(df):
    """Create a dictionary where keys are user_n and values and individual answer df for that user."""
    users_dfs = {}
    for user in df.index.get_level_values(0).drop_duplicates():  # Used later
        users_dfs[f"{user}"] = df.loc[df.index.get_level_values(0) == user]
    return users_dfs

def question_comprasion(df):
    """A function to help compare and plot the answers of all participants answers for a specific question. """
    radio = st.radio(
        'Which question would you like to compare between USERS?',
        df.columns)
    
    fig = px.line(df.reset_index(), x='Date', y=radio, color='User ID', line_dash='User ID', markers=True,)
    st.plotly_chart(fig, use_container_width=True)
    return

question_comprasion(df)
