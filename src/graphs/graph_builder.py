from langgraph.graph import START, END, StateGraph
from src.llms.groqllm import GroqLLM
from src.states.blogstate import Blogstate
from src.nodes.blog_node import blognode

class Graph_builder:
    def __init__(self,llm):
        self.graph= StateGraph(Blogstate)
        self.llm= llm

    def build_topic_graph(self):
        """
        Build a graph to generate blog
        """
        self.blog_node= blognode(self.llm)

        self.graph.add_node("title_creation",self.blog_node.title_creation_node)
        self.graph.add_node("content_generation",self.blog_node.content_generation_node)

        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)