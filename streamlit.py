import streamlit as st
import CVReader
import os

st.title("Cover Letter Generator")
st.subheader("Upload your CV and generate professional cover letters effortlessly!")

# Load API Key
apiKeys = st.secrets["API_Keys"]
openAiKey = apiKeys["openAI"]
cv_reader = CVReader.CVReader(openAiKey)

# Upload CV File
cv_file = st.file_uploader("Upload your CV (PDF format):", type="pdf")
if cv_file:
    with st.spinner("Extracting text from CV..."):
        cv_text = cv_reader.getCvText(cv_file.read())
        if "Error" in cv_text:
            st.error(cv_text)
        else:
            st.success("CV text extracted successfully!")
            with st.spinner("Generating CV summary..."):
                summary = cv_reader.getCvSummary()
                if "Error" in summary:
                    st.error(summary)
                else:
                    st.success("CV summary generated successfully!")

# Cover Letter Inputs
st.subheader("Generate a Cover Letter")
employer_name = st.text_input("Employer Name:")
job_title = st.text_input("Job Title:")
recruiter_name = st.text_input("Recruiter Name:")
job_description = st.text_area("Job Description:", height=150)

if st.button("Generate Cover Letter"):
    if not employer_name or not job_title or not recruiter_name or not job_description:
        st.error("Please fill in all fields for the cover letter.")
    else:
        with st.spinner("Generating cover letter..."):
            cover_letter, success = cv_reader.getCoverLetter(
                employer_name, job_title, recruiter_name, job_description
            )
            if success:
                st.success("Cover letter generated successfully!")
                st.text_area("Generated Cover Letter:", cover_letter, height=300)
            else:
                st.error(cover_letter)

# Customize Cover Letter
st.subheader("Customize Your Cover Letter")
feedback = st.text_input("Provide Feedback or Customization Instructions:")
if st.button("Apply Customization"):
    if not feedback:
        st.error("Please provide feedback to customize the cover letter.")
    else:
        with st.spinner("Applying customization..."):
            updated_cover_letter = cv_reader.customizeCoverLetter(feedback)
            if "Error" in updated_cover_letter:
                st.error(updated_cover_letter)
            else:
                st.success("Cover letter customized successfully!")
                st.text_area("Updated Cover Letter:", updated_cover_letter, height=300)