import streamlit as st
import CVReader

apiKeys = st.secrets["API_Keys"]
openAiKey = apiKeys["openAI"]

cvreader = CVReader.CVReader(openAiKey)


uploaded_cv = st.file_uploader("Upload CV")

if uploaded_cv is not None:
    cvText = cvreader.getCvText(uploaded_cv.read())

    summary, gotResponse = cvreader.getCvSummary()
    st.write(summary)

