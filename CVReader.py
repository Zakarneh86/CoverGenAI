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
            "Provide a detailed summary, focusing on Education, Experience, "
            "Achievements, Certification, and Projects: " + self.cvText
        )
        self.messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=self.messages,
                max_tokens=500,
                temperature=0.8,
            )
            self.summary = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": self.summary})
        except Exception as e:
            self.clientError = f"Error generating summary: {str(e)}"
            return self.clientError

        return self.summary

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