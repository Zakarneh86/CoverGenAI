import fitz
import json
import openai
import os
from openai import OpenAI


class CVReader:

    def __init__(self):
        self.cvText = ''
        self.coverText = ''

    def getCVText(self, cvFile):
        doc = fitz.open(cvFile)
        for i in range(doc.page_count):
            page = doc.load_page(i)
            self.cvText += page.get_text()
        return self.getCVText