from fastapi import FastAPI, Request
import uvicorn
from src.graphs.graph_builder import Graph_builder
from src.llms.groqllm import GroqLLM
from dotenv import load_dotenv
load_dotenv()

app= FastAPI()

@app.post("/blogs")
async def create_blog(request:Request):
    data= await request.json()
    topic= data.get("topic", "")

    groqllm= GroqLLM()
    llm= groqllm.groqllm()

    graph_builder= Graph_builder(llm)

    if topic:
        graph=graph_builder.router_graph(use_case="topic")
        state= graph.invoke({'topic':topic})
    return {"data": state}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0",port=8000, reload=True)








