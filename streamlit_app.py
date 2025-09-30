import streamlit as st
import app
import cloud_app1
import graph1

PAGES = {
    "Insurance Predictor": app,
    "Patient Manager": cloud_app1,
    "Mini Cloud Storage": graph1,
}

st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", list(PAGES.keys()))


page = PAGES[choice]
page.app()   # each app file must have an `app()` function

    