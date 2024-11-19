import streamlit as st
import CVReader

apiKeys = st.secrets["API_Keys"]
openAiKey = apiKeys["openAI"]
st.write(openAiKey)

cvreader = CVReader.CVReader(openAiKey)


uploaded_cv = st.file_uploader("Upload CV")

if cvreader.ClientConnected:
    if uploaded_cv is not None:
        cvText = cvreader.getCvText(uploaded_cv.read())

        summary, gotResponse = cvreader.getCvSummary()
        st.write(summary)
else:
    st.write(cvreader.connectionError)
