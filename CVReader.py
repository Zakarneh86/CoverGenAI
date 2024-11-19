import fitz
import json
import openai
import os
from openai import OpenAI


class CVReader:

    def __init__(self, openAiKey):
        self.cvText = ''
        self.coverText = ''
        try:
            self.client = OpenAI(api_key=openAiKey)
            self.ClientConnected = True
        except Exception as e:
            self.ClientConnected = False
            self.connectionError = e
        

    def getCvText(self, cvFile):
        doc = fitz.open(stream = 
                        cvFile)
        for i in range(doc.page_count):
            page = doc.load_page(i)
            self.cvText += page.get_text()
        return self.cvText

    def getCvSummary(self):
        prompt = "Provide a detailed summary, focusing on Education, Experience, Achievments, Certification and Projects: "
        prompt = prompt + self.cvText

        message = [{"role": "user", "content": f"{prompt}"}]

        if self.ClientConnected:
            try:
                response = self.client.chat.completions.create(
                    model = "gpt-4",
                    messages= message,
                    max_tokens= 500,
                    temperature = 0.8)
                gotResponse = True
            except:
                gotResponse = False

            if gotResponse:
                self.summary = response.choices[0].message.content
            else:
                self.summary = None
        return self.summary, gotResponse
