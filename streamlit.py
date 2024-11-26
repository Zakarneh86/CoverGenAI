import streamlit as st
from io import BytesIO
from CVReader import CVReader


apiKeys = st.secrets["API_Keys"]
openAiKey = apiKeys["openAI"]
if "cv_reader" not in st.session_state:
    st.session_state.cv_reader = CVReader(openAiKey)

st.title("CV and Cover Letter Generator")
st.subheader("Upload your CV and generate professional cover letters effortlessly!")

# File Upload
uploaded_cv = st.file_uploader("Upload your CV (PDF format):", type="pdf")
if uploaded_cv:
    # Check if CV text is already stored in session state
    if "cv_text" not in st.session_state:
        with st.spinner("Extracting text from CV..."):
            try:
                st.session_state.cv_text = st.session_state.cv_reader.getCvText(BytesIO(uploaded_cv.read()))
                st.success("CV text extracted successfully!")
            except Exception as e:
                st.session_state.cv_text = None
                st.error(f"Error extracting text from CV: {str(e)}")
    else:
        st.success("CV text already loaded!")
    
    # Display extracted CV text
    if st.session_state.cv_text:
        #st.text_area("Extracted CV Text:", st.session_state.cv_text, height=200)

        # Generate CV Summary
        #if st.button("Generate CV Summary"):
        if "cv_summary" not in st.session_state:
            with st.spinner("Generating CV summary..."):
                try:
                    st.session_state.cv_summary, st.session_state.userName, st.session_state.eMail, st.session_state.phone = st.session_state.cv_reader.getCvSummary()
                    if "Error" in st.session_state.cv_summary:
                        raise ValueError(st.session_state.cv_summary)
                    st.success("CV summary generated successfully!")
                except Exception as e:
                    st.session_state.cv_summary = None
                    st.error(f"Error generating CV summary: {str(e)}")
        else:
            st.success("CV summary already generated!")
        
        # Display CV summary
        #if st.session_state.cv_summary:
            #st.text_area("CV Summary:", st.session_state.cv_summary, height=200)

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
            try:
                cover_letter, success = st.session_state.cv_reader.getCoverLetter(
                    employer_name, job_title, recruiter_name, job_description
                )
                if success:
                    st.session_state.cover_letter = cover_letter
                    st.success("Cover letter generated successfully!")
                else:
                    raise ValueError(cover_letter)
            except Exception as e:
                st.session_state.cover_letter = None
                st.error(f"Error generating cover letter: {str(e)}")

        # Display generated cover letter
        if st.session_state.cover_letter:
            st.text_area("Generated Cover Letter:", st.session_state.cover_letter, height=300)

# Customize Cover Letter
st.subheader("Customize Your Cover Letter")
feedback = st.text_input("Provide Feedback or Customization Instructions:")
if st.button("Apply Customization"):
    if not feedback:
        st.error("Please provide feedback to customize the cover letter.")
    elif "cover_letter" not in st.session_state:
        st.error("Please generate a cover letter first.")
    else:
        with st.spinner("Applying customization..."):
            try:
                updated_cover_letter = st.session_state.cv_reader.customizeCoverLetter(feedback)
                st.session_state.cover_letter = updated_cover_letter
                st.success("Cover letter customized successfully!")
            except Exception as e:
                st.error(f"Error customizing cover letter: {str(e)}")

        # Display updated cover letter
        if "cover_letter" in st.session_state and st.session_state.cover_letter:
            st.text_area("Generated Cover Letter:", st.session_state.cover_letter, height=300)

# Section for PDF download functionality
st.subheader("Download Your Cover Letter as PDF")

    # Ensure the PDF fields and button always remain visible
if "userName" not in st.session_state:
    st.session_state.userName = "Your Name"
if "eMail" not in st.session_state:
    st.session_state.eMail = "Email"
if "phone" not in st.session_state:
    st.session_state.phone = "Phone"


# Allow users to input their name and title for the PDF
st.session_state.userName = st.text_input(st.session_state.userName, value=st.session_state.user_name)
st.session_state.eMail = st.text_input(st.session_state.eMail, value=st.session_state.user_title)
st.session_state.phone = st.text_input(st.session_state.phone, value = st.session_state.phone)

# Generate PDF button
if st.button("Generate PDF"):
    with st.spinner("Generating PDF..."):
        try:
            pdf_buffer, error, inError = st.session_state.cv_reader.loadCoverLetter(
                coverLetter=st.session_state.cover_letter,
                userName=st.session_state.userName,
                usereMail=st.session_state.eMail,
                userPhone = st.session_state.phone
            )
            if not inError:
                st.success("PDF generated successfully!")
                st.download_button(
                    label="Download Cover Letter PDF",
                    data=pdf_buffer.getvalue(),
                    file_name="Cover_Letter.pdf",
                    mime="application/pdf",
                )
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")