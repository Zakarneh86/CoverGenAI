import streamlit as st
import CVReader
import os

apiKeys = st.secrets["API_Keys"]
openAiKey = apiKeys["openAI"]

cvreader = CVReader.CVReader(openAiKey)
uploaded_cv = st.file_uploader("Upload CV")

if uploaded_cv is not None:
    cvText = cvreader.getCvText(uploaded_cv.read())
    summary= cvreader.getCvSummary()
    badClient = cvreader.badClient
    connectionError = cvreader.clientError
    
    if not badClient:
        employerName = st.text_input("Employer Name", "Employer Name")
        jobTitle = st.text_input("Job Title", "Job Title")
        recruiterName = st.text_input("Recruiter Name", "Recruiter")
        jobDescription = st.text_input("Job Description", "Paste Job Description")
        generateLetter = st.button("Generate Letter")

        if generateLetter:
            if employerName != "Employer Name" and employerName != "":
                if jobTitle != "Job Title" and jobTitle !="":
                    if recruiterName !="":
                        if jobDescription != "Paste Job Description" and jobDescription != "":
                            coverLetter, letterGenerated = cvreader.getCoverLetter(employerName, jobTitle, recruiterName, jobDescription)
                            badClient = cvreader.badClient
                            connectionError = cvreader.clientError
                            if not badClient:
                                with st.container(height = 300):
                                    st.write(coverLetter)
                            else:
                                st.write(connectionError)
                            if letterGenerated:
                                pdfLetter = cvreader.loadCoverLetter(coverLetter=coverLetter)
                                st.download_button(
                                    label = "Download Letter",
                                    data = pdfLetter,
                                    file_name = "Cover Letter.pdf",
                                    mime = "application/pdf"
                                )
                        else:
                            st.write("Job Description is Mandatory")
                    else:
                        st.write("Recruiter is Mandatory")
                else:
                    st.write("Job Title is Mandatory")
            else:
                st.write("Employer Name is Mandatory")
    else:
        st.write(connectionError)



