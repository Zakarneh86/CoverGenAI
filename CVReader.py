import pymupdf
import json
import openai
from openai import OpenAI
import io
import re


class CVReader:

    def __init__(self, openAiKey):
        self.cvText = ''
        self.coverText = ''
        self.client = OpenAI(api_key=openAiKey)
        self.messages = []
        self.summary = None
        self.clientError = None

    def getCvText(self, cvFile):
        try:
            doc = pymupdf.open(stream=cvFile)
            for i in range(doc.page_count):
                page = doc.load_page(i)
                self.cvText += page.get_text()
            return self.cvText
        except Exception as e:
            return f"Error reading CV file: {str(e)}"

    def getCvSummary(self):
        if not self.cvText:
            return "No CV text extracted to summarize."
        
        prompt = (
            f'''Given {self.cvText}, Provide a detailed summary focusing
            on Education, Experience, Achievements, Certification and
            Executed Projects. Also, return in a dict format "User Name, Email Address and Phone Number"'''
        )
        self.messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=self.messages,
                max_tokens=500,
                temperature=0.8
            )
            self.summary = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": self.summary})
        except Exception as e:
            self.clientError = f"Error generating summary: {str(e)}"
            return self.clientError
        
        try:
            match1 = re.search(r"{", self.summary)
            match2 = re.search(r"}", self.summary)
            info = dict(self.summary[match1.start():match2.start()])
            info = dict(re.findall(r'"(.*?)": "(.*?)"', info))
            self.userName = info['User Name']
            self.eMail = info['Email Address']
            self.phone = info['Phone Number']
        except Exception as e:
            self.userName = None
            self.eMail = None
            self.phone = None

        return self.summary, self.userName, self.eMail, self.phone

    def getCoverLetter(self, employerName, jobTitle, recruiterName, jobDescription):
        if not self.summary:
            return "Please generate a CV summary first.", False
        
        cover_prompt = (
            f"Given the below resume summary:\n{self.summary}\n"
            f"and the below job description:\n{jobDescription}\n"
            f"write a job application cover letter (300 words). "
            f"The company name is {employerName} and the job title is {jobTitle}. "
            f"And the recruiter name is {recruiterName}"
        )
        self.messages.append({"role": "user", "content": cover_prompt})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=self.messages,
                max_tokens=500,
                temperature=0.8,
            )
            self.coverText = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": self.coverText})
            return self.coverText, True
        except Exception as e:
            self.clientError = f"Error generating cover letter: {str(e)}"
            return self.clientError, False

    def customizeCoverLetter(self, feedback):
        if not self.coverText:
            return "No cover letter to customize. Generate one first."
        
        self.messages.append({"role": "user", "content": feedback})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=self.messages,
                max_tokens=500,
                temperature=0.8,
            )
            self.coverText = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": self.coverText})
        except Exception as e:
            return f"Error customizing cover letter: {str(e)}"
        return self.coverText
    
    def loadCoverLetter(self, coverLetter, userName="Your Name", usereMail="Yor Email",userPhone = "Your Phone Number" ):
        try:
            # Letter Parameters
            a4_width = 595.28  # A4 width in points
            a4_height = 841.89  # A4 height in points
            left_bar_width = 186
            bg_color_left = (0.10196, 0.25098, 0.6)  # Dark blue
            bg_color_right = (1, 1, 1)  # White
            left_rect = pymupdf.Rect(0, 0, left_bar_width, a4_height)
            right_rect = pymupdf.Rect(left_bar_width, 0, a4_width, a4_height)
            bodyFontName = "times-roman"
            bodyFontSize = 12
            sideFontName = "times-bold"
            sideFontSize = 16

            # Letter Building
            pdfBuffer = io.BytesIO()
            letterPDF = pymupdf.open()
            page = letterPDF.new_page(width=a4_width, height=a4_height)

            # Letter Formatting
            shape = page.new_shape()
            shape.draw_rect(left_rect)
            shape.finish(width=0, color=None, fill=bg_color_left)
            shape.draw_rect(right_rect)
            shape.finish(width=0, color=None, fill=bg_color_right)
            shape.commit()

            # Inserting Left Bar Text (Name and Title)
            page.insert_textbox(
                pymupdf.Rect(19, 25, left_bar_width - 5, 50),
                userName,
                fontsize=sideFontSize,
                fontname=sideFontName,
                color=(1, 1, 1),  # White text
                align=0  # Left align
            )
            page.insert_textbox(
                pymupdf.Rect(19, 55, left_bar_width - 5, 80),
                usereMail,
                fontsize=16,  # Slightly smaller title
                fontname=sideFontName,
                color=(1, 1, 1),  # White text
                align=0  # Left align
            )
            page.insert_textbox(
            pymupdf.Rect(19, 85, left_bar_width - 5, 110),
            userPhone,
            fontsize=16,  # Slightly smaller title
            fontname=sideFontName,
            color=(1, 1, 1),  # White text
            align=0  # Left align
            )

            # Insert Body Text (Cover Letter Content)
            page.insert_textbox(
                pymupdf.Rect(left_bar_width + 18, 132, a4_width - 20, 800),
                coverLetter,
                fontname=bodyFontName,
                fontsize=bodyFontSize,
                color=(0, 0, 0),  # Black text
                align=0  # Left align
            )

            # Save PDF to buffer
            letterPDF.save(pdfBuffer)
            letterPDF.close()
            pdfBuffer.seek(0)

            return pdfBuffer, None, False

        except Exception as e:
            raise
            
