#Importing Chatmodels from OpenAI and Groq
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


#LLM class to initialize different chat models
class LLM:
    #Constructor to load environment variables
    def __init__(self):
        load_dotenv()
        #Load Groq API Key and Model Name
        self.groq_api_key= os.getenv("GROQ_API_KEY")
        self.groq_model_name= os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        #Load OpenAI API Key and Model Name
        self.open_api_key= os.getenv("OPENAI_API_KEY")
        self.openai_model_name= os.getenv("OPENAI_MODEL", "gpt-5-nano")

    #Method to initialize Groq LLM
    def groqllm(self):
        #Initialize Groq LLM
        if not self.groq_api_key:
            raise ValueError("Groq-api-key is not found in Environmental variables")
        try:
            llm= ChatGroq(model=self.groq_model_name,
                         api_key=self.groq_api_key)
            return llm
        except Exception as e:
            raise ValueError(f"Error occured due to exception {e}")
            return None

    #Method to initialize OpenAI LLM   
    def openaillm(self):
        #Initialize OpenAI LLM
        if not self.open_api_key:
            raise ValueError("OpenAI-api-key is not found in Environmental variables")
        try:
            llm = ChatOpenAI(
                openai_api_key=self.open_api_key,
                model_name=self.openai_model_name,
                temperature=0,
            )
            return llm
        except Exception as e:
            raise ValueError(f"Error occurred due to exception {e}")
            return None
        
        
        

        

        