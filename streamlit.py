import streamlit as st
import CVReader

cvreader = CVReader.CVReader()

uploaded_cv = st.file_uploader("Upload CV")

if uploaded_cv is not None:
    cvText = cvreader.getCVText(uploaded_cv)

    st.write(cvText)
