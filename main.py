import streamlit as st
import sqlite3 as sql
import pandas as pd

st.set_page_config(layout="wide")
con = sql.connect("residencies.db")

st.title("Dr. Mahi's Assistant")
st.caption("Made with   :two_hearts: by Vinay")
df = pd.read_sql(
    "SELECT * from residencies",
    con,
)

if "df" not in st.session_state:
    st.session_state.df = df

data, map = st.columns(2)

with data:
    st.header("All Programs")
    st.caption("Select some programs below to view details")
    event = st.dataframe(
        st.session_state.df,
        key="data",
        height=500,
        on_select="rerun",
        selection_mode=["single-row"],
        column_order=[
            "PROGRAM",
            "CITY",
            "STATE",
        ],
    )
with map:
    st.header("Location")
    st.caption("Selected programs will be mapped here")
    if len(event.selection.rows) != 0:
        map_data = pd.DataFrame()
        for i in event.selection.rows:
            map_data = pd.concat([map_data, st.session_state.df.iloc[[i]]])
        st.map(map_data, size=10000, zoom=7)
    else:
        st.map(st.session_state.df, size=10000, zoom=3)

if len(event.selection.rows) != 0:
    data = pd.DataFrame()
    map_data = pd.DataFrame()
    for i in event.selection.rows:
        map_data = pd.concat([map_data, st.session_state.df.iloc[[i]]])
        data = st.session_state.df.iloc[[i]]

        st.header(data["PROGRAM"][i])
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            st.subheader("Location")
            st.text(data["CITY"][i] + ", " + data["STATE"][i])
            st.subheader("Step 2 Score")
            st.text(data["STEP 2 SCORE MIN"][i])
        with d2:
            st.subheader("Percent IMGs")
            st.text("US-IMG:\t\t" + data["US IMG"][i])
            st.text("Non US-IMG:\t" + data["NON-US IMG"][i])
            st.subheader("Salary")
            st.text(data["PGY1 salary"][i])
        with d3:
            st.subheader("Fellowship")
            st.text(data["% going for another program after"][i])
            st.subheader("Alumni")
            st.text("KMC Manipal:\t" + str(data["KMC Manipal Alumni"][i]))
            st.text("KMC Managalore:\t" + str(data["KMC Mangalore Alumni"][i]))
        with d4:
            st.subheader("Certificates")
            st.text("ECFGM: " + str(data["ECFMG timing"][i]))
            st.text("USCE: " + str(data["USCE requirement"][i]))
