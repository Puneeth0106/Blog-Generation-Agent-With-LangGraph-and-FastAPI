from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

class GroqLLM:
    def __init__(self):
        load_dotenv()
        self.groq_api_key= os.getenv("GROQ_API_KEY")
        self.groq_model_name= os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def groqllm(self):
        if not self.groq_api_key:
            raise ValueError("Groq-api-key is not found in Environmental variables")
        try:
            llm= ChatGroq(model=self.groq_model_name,
                         api_key=self.groq_api_key)
            return llm
        except Exception as e:
            raise ValueError("Error occured due to exception {e}")
            return None

        
        

        

        