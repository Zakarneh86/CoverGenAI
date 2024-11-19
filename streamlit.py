import streamlit as st
import CVReader

apiKeys = st.secrets["API_Keys"]
openAiKey = apiKeys["openAI"]

cvreader = CVReader.CVReader(openAiKey)


uploaded_cv = st.file_uploader("Upload CV")

if cvreader.ClientConnected:
    if uploaded_cv is not None:
        cvText = cvreader.getCvText(uploaded_cv.read())
        summary, gotResponse = cvreader.getCvSummary()
        
        if gotResponse:
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
                                st.write("Ready to Run!")
                            else:
                                st.write("Job Description is Mandatory")
                        else:
                            st.write("Recruiter is Mandatory")
                    else:
                        st.write("Job Title is Mandatory")
                else:
                    st.write("Employer Name is Mandatory")

else:
    st.write(cvreader.connectionError)
