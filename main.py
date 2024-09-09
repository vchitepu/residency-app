import streamlit as st
import pandas as pd
from geopy.distance import geodesic


def calculate_distance(long, lat):
    loc= (lat, long)
    me = (39.96110079066445, -74.89403720990995)
    #her = (42.012463848982506, -88.68485822940616)
    #parents = (26.25264342797538, -80.29153925589763)
    distance= geodesic(loc, me).km
    return distance
    

def data_display(data, i):
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
        st.subheader("LoRs Needed")
        st.text(str(data["Number of rec letters"][i]))


def set_edit():
    st.session_state.editing = True


def stop_edit(data, i):
    st.session_state.editing = False
    st.session_state.df.update(data)
    st.dataframe(st.session_state.df.iloc[[i]])


def delete_row():
    st.warning("Deleted Item")


def data_editor(data):
    new_data = st.data_editor(
        data,
        disabled=False,
        hide_index=True,
        column_order=[
            "PROGRAM",
            "CITY",
            "STATE",
            "Number of positions",
            "STEP 2 SCORE MIN",
            "Number of rec letters",
            "PGY1 salary",
            "KMC Manipal Alumni",
            "KMC Mangalore Alumni",
            "% going for another program after",
            "ECFGM timing",
            "USCE requirement",
            "Notes",
        ],
    )
    return new_data


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    st.title("Mahi's Residency Assistant")
    st.caption("Made with   :two_hearts: by Vinay")

    df = pd.read_csv("residencies.csv")

    if "df" not in st.session_state:
        st.session_state.df = df

    if "editing" not in st.session_state:
        st.session_state.editing = False

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
        if len(event.selection.rows) != 0:
            map_data = pd.DataFrame()
            for i in event.selection.rows:
                map_data = pd.concat([map_data, st.session_state.df.iloc[[i]]])
            distance = calculate_distance(map_data.LONGITUDE.iloc[0], map_data.LATITUDE.iloc[0])
            st.caption("Distance from your boyfriends house: " + str(round(distance, 2)) + " KM")
            st.map(map_data, size=10000, zoom=7)
        else:
            st.map(st.session_state.df, size=10000, zoom=3)

    if len(event.selection.rows) != 0:
        data = pd.DataFrame()
        for i in event.selection.rows:
            data = st.session_state.df.iloc[[i]]
            st.header(data["PROGRAM"][i])
            if st.session_state.editing is True:
                new_data = data_editor(data)
                save_button = st.button("Save", on_click=stop_edit, args=(new_data, i))
            else:
                data_display(data, i)
                b1, b2, b3 = st.columns([1, 2, 10])
                with b1:
                    start_edit = st.button("Edit", on_click=set_edit)
                with b2:
                    delete = st.button("Delete")
                    if delete:
                        delete_row()
