import pymupdf
import json
import openai
from openai import OpenAI
import io


class CVReader:

    def __init__(self, openAiKey):
        self.cvText = ''
        self.coverText = ''
        self.client = OpenAI(api_key=openAiKey)

    def getCvText(self, cvFile):
        doc = pymupdf.open(stream = 
                        cvFile)
        for i in range(doc.page_count):
            page = doc.load_page(i)
            self.cvText += page.get_text()
        return self.cvText

    def getCvSummary(self):
        prompt = "Provide a detailed summary, focusing on Education, Experience, Achievments, Certification and Projects: "
        prompt = prompt + self.cvText

        message = [{"role": "user", "content": f"{prompt}"}]

        try:
            response = self.client.chat.completions.create(
                model = "gpt-4",
                messages= message,
                max_tokens= 500,
                temperature = 0.8)
            gotResponse = True
            self.badClient = False
            self.clientError = None
        except Exception as e:
            gotResponse = False
            self.badClient = True
            #self.clientError = f"Error: {str(e)}, Type: {type(e)}"
            self.clientError = f'API Connection Error. Contact mm_zak@hotmail.com'

        if gotResponse:
            self.summary = response.choices[0].message.content
        else:
            self.summary = None
        return self.summary
    
    def getCoverLetter(self, employerName, jobTitle, recruiterName, jobDescription):
        cover_prompt = f'''Given the below resume summary:
              {self.summary}
              and the below job description:
              {jobDescription}
              write a job application cover letter (300 words). The company name is 
              {employerName} and the job title is {jobTitle}.
                And the recruiter name is {recruiterName}'''
        messages = [
        {"role": "user", "content": f"{cover_prompt}"}]
        
        try:
            response = self.client.chat.completions.create(model="gpt-4",
                                        messages=messages,
                                        max_tokens=500,
                                        temperature=0.8)
            letterGenerated = True
            self.badClient = False
            self.clientError = None
        except Exception as e:
            letterGenerated = False
            self.badClient = True
            #self.clientError = f"Error: {str(e)}, Type: {type(e)}"
            self.clientError = f'API Connection Error. Contact mm_zak@hotmail.com'
        
        if letterGenerated:
            coverLetter = response.choices[0].message.content
        else:
            coverLetter = None
        return coverLetter, letterGenerated
    
    def loadCoverLetter(self, coverLetter):
        # Letter Parameters
        a4_width = 595.28
        a4_height = 841.89
        bg_color_left = (0.10196, 0.25098, 0.6)
        bg_color_right = (1, 1, 1)
        left_rect = pymupdf.Rect(0,0, 186, a4_height)
        right_rect = pymupdf.Rect(186, 0, a4_width, a4_height)
        bodyFontName = "times-roman"
        bodyFontSize = 12
        sideFontName = 'times-bold'
        sideFontSize = 30

        #Letter Building
        pdfBuffer = io.BytesIO()
        letterPDF = pymupdf.open()
        page = letterPDF.new_page(width = a4_width, height = a4_height)

        # Letter Formating
        shape = page.new_shape()
        shape.draw_rect(left_rect)
        shape.finish(width=0, color=None, fill=bg_color_left)
        shape.draw_rect(right_rect)
        shape.finish(width=0, color=None, fill=bg_color_right)
        shape.commit()

        # Inserting Side Text
        page.insert_textbox(
            pymupdf.Rect(19, 24, 156, 208),
            'Mohamed Zakarneh',
            fontsize=30,
            fontname = 'times-bold',
            color = (1,1,1),
            align=0
        )

        # Insert Body text
        page.insert_textbox(
            pymupdf.Rect(204, 132, 575, 800),
            coverLetter,
            fontname = 'times-roman',
            fontsize=14,
            align=0
        )

        letterPDF.save(pdfBuffer)
        letterPDF.close()

        pdfBuffer.seek(0)

        return pdfBuffer