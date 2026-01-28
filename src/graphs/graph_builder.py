# src/graphs/graph_builder.py
# Graph builder class to create different graphs for blog generation
# Configuration for Langgraph Studio Entry Point

from langgraph.graph import START, END, StateGraph
from src.llms.llm import LLM
from src.states.blogstate import Blogstate
from src.nodes.blog_node import blognode
from dotenv import load_dotenv
import os

# Load environment variables

load_dotenv()

class Graph_builder:
    """
    Graph builder class to create different graphs for blog generation
    """
    #Constructor to initialize the graph builder with LLM and StateGraph
    #Graph builder needs LLM to pass it to the nodes- Passed from app.py
    def __init__(self,llm):
        self.graph= StateGraph(Blogstate)
        self.llm= llm

    # Defining Graph-1
    def build_topic_graph(self):
        """
        Build a graph to generate blog
        """
        self.blog_node= blognode(self.llm)

        #Nodes
        self.graph.add_node("title_creation",self.blog_node.title_creation_node)
        self.graph.add_node("content_generation",self.blog_node.content_generation_node)
        

        #Edges
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)

        return self.graph
    
    def build_language_graph(self):
        """
        Build a graph to generate blog in different language
        """

        # Blognode needs LLM to generate blog: Passing LLM defined in the Constructor to blognode
        self.blog_node= blognode(self.llm)

        #Nodes
        self.graph.add_node("title_creation",self.blog_node.title_creation_node)
        self.graph.add_node("content_generation",self.blog_node.content_generation_node)
        self.graph.add_node('telugu_translation', lambda state: self.blog_node.translation_node(state,"telugu"))
        self.graph.add_node("spanish_translation", lambda state: self.blog_node.translation_node(state,"spanish"))
        self.graph.add_node("french_translation", lambda state: self.blog_node.translation_node(state,"french"))
        self.graph.add_node("german_translation", lambda state: self.blog_node.translation_node(state,"german"))
        self.graph.add_node("swahili_translation", lambda state: self.blog_node.translation_node(state,"swahili"))
        

        #Edges
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation", "content_generation")

        self.graph.add_conditional_edges(
            "content_generation", 
                self.blog_node.language_router_node,
                {
                    "telugu": "telugu_translation",
                    "spanish": "spanish_translation",
                    "french": "french_translation",
                    "german": "german_translation",
                    "swahili": "swahili_translation",
                    "english": END
                } 
                )

        self.graph.add_edge("telugu_translation", END)
        self.graph.add_edge("spanish_translation", END)
        self.graph.add_edge("french_translation", END)
        self.graph.add_edge("german_translation", END)
        self.graph.add_edge("swahili_translation", END)

        return self.graph

    #   Method to return the compiled graph based on use case : Router graph needs use_case to decide which graph to build- Passed in from app.py
    def router_graph(self,use_case):
        if use_case=="topic":
            self.build_topic_graph()
        if use_case=="language":
            self.build_language_graph()
        return self.graph.compile()
        

# Langsmith-Studio ENTRY POINT

# 1. Setup the LLM
llm_instance = LLM().openaillm()
# 2. Instantiate your builder
builder = Graph_builder(llm_instance)
# 3. Build the desired graph
graph= builder.build_language_graph().compile()