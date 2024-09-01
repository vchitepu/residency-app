import streamlit as st
import sqlite3 as sql
import pandas as pd

st.set_page_config(layout="wide")
con = sql.connect("residencies1.db")

st.title("Dr. Mahi's Assistant")
st.write("Made with   :two_hearts: by Vinay")
df = pd.read_sql(
    "SELECT * from residencies",
    con,
)

if "df" not in st.session_state:
    st.session_state.df = df


event = st.dataframe(
    st.session_state.df,
    key="data",
    on_select="rerun",
    selection_mode=["single-row"],
    column_order=[
        "PROGRAM",
        "CITY",
        "STATE",
        "US IMG",
        "NON-US IMG",
        "STEP 2 SCORE MIN",
        "Number of rec letters",
    ],
)

if len(event.selection.rows) != 0:
    details, map = st.columns(2)
    index = event.selection.rows[0]
    data = st.session_state.df.iloc[[index]]

    with details:
        st.header(data["PROGRAM"][index])
        d1, d2 = st.columns(2)
        with d1:
            st.subheader("Location")
            st.text(data["CITY"][index] + ", " + data["STATE"][index])
            st.subheader("Step 2 Score")
            st.text(data["STEP 2 SCORE MIN"][index])
            st.subheader("Salary")
            st.text(data["PGY1 salary"][index])
            st.subheader("Fellowship")
            st.text(data["% going for another program after"][index])
        with d2:
            st.subheader("Percent IMGs")
            st.text("US-IMG:\t\t" + data["US IMG"][index])
            st.text("Non US-IMG:\t" + data["NON-US IMG"][index])
            st.subheader("Alumni")
            st.text("KMC Manipal:\t" + str(data["KMC Manipal Alumni"][index]))
            st.text("KMC Managalore:\t" + str(data["KMC Mangalore Alumni"][index]))
            st.subheader("Certificates")
            st.text("ECFGM: " + str(data["ECFMG timing"][index]))

    with map:
        st.map(data, size=10000, zoom=7)
