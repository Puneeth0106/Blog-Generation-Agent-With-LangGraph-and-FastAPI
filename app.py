# FastAPI application to create blog posts based on topic and language

from fastapi import FastAPI, Request
import uvicorn
from src.graphs.graph_builder import Graph_builder
from src.llms.llm import LLM
from dotenv import load_dotenv
load_dotenv()

app= FastAPI()

# API endpoint to create blog based on topic and language
@app.post("/blogs")
async def create_blog(request:Request):
    # Parse the incoming request to get topic and language
    data= await request.json()
    topic= data.get("topic", "")
    language= data.get("language", None)

    # Initialize LLM (Using OpenAI LLM here, can be changed to Groq LLM if needed)
    llm= LLM().openaillm()

    # Initialize Graph Builder with LLM
    graph_builder= Graph_builder(llm)

    # Decide which graph to build based on presence of language
    # If both topic and language are provided, use language graph
    # If only topic is provided, use topic graph
    if topic and language is not None:
        graph=graph_builder.router_graph(use_case="language")
        state= graph.invoke({'topic':topic, 'language_content': language})
    elif topic:
        graph=graph_builder.router_graph(use_case="topic")
        state= graph.invoke({'topic': topic})
    return {"data": state}



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0",port=8000, reload=True)








