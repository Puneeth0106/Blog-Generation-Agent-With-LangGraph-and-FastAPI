from langgraph.graph import START, END, StateGraph
from src.llms.groqllm import GroqLLM
from src.states.blogstate import Blogstate
from src.nodes.blog_node import blognode
from dotenv import load_dotenv
import os

load_dotenv()

class Graph_builder:
    def __init__(self,llm):
        self.graph= StateGraph(Blogstate)
        self.llm= llm

    def build_topic_graph(self):
        """
        Build a graph to generate blog
        """
        self.blog_node= blognode(self.llm)

        # self.graph.add_node(START)
        self.graph.add_node("title_creation",self.blog_node.title_creation_node)
        self.graph.add_node("content_generation",self.blog_node.content_generation_node)
        # self.graph.add_node(END)

        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)



    def router_graph(self,use_case):
        if use_case=="topic":
            self.build_topic_graph()
        return self.graph.compile()
        

# --- CLI / STUDIO ENTRY POINT ---

# 1. Setup the LLM
llm_instance = GroqLLM().groqllm()

# 2. Instantiate your builder
builder = Graph_builder(llm_instance)

# 3. Execute the build (This sets up nodes and edges)
builder.build_topic_graph()

# 4. Compile and assign to 'graph' so langgraph.json can find it
graph = builder.graph.compile()