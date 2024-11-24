import streamlit as st
import CVReader
import os

apiKeys = st.secrets["API_Keys"]
openAiKey = apiKeys["openAI"]
cv_reader = CVReader.CVReader(openAiKey)

cv_file = st.file_uploader("Upload your CV (PDF format):", type="pdf").read()
if cv_file:
    cv_text = cv_reader.getCvText(cv_file)
    #st.text_area("Extracted CV Text:", cv_text, height=200)

    # Generate CV Summary
    #if st.button("Generate CV Summary"):
    summary = cv_reader.getCvSummary()
    #st.text_area("CV Summary:", summary, height=200)

    # Cover Letter Generation
    employer_name = st.text_input("Employer Name:")
    job_title = st.text_input("Job Title:")
    recruiter_name = st.text_input("Recruiter Name:")
    job_description = st.text_area("Job Description:", height=150)

    if st.button("Generate Cover Letter"):
        cover_letter = cv_reader.getCoverLetter(
            employer_name, job_title, recruiter_name, job_description
        )
        cover_letter = cover_letter.replace("\n", "\n")
        st.text_area("Generated Cover Letter:", cover_letter, height=300)

        # Customization Loop
        feedback = st.text_input("Provide Feedback or Customization Instructions:")
        if st.button("Apply Customization"):
            updated_cover_letter = cv_reader.customizeCoverLetter(feedback)
            st.text_area("Updated Cover Letter:", updated_cover_letter, height=300)