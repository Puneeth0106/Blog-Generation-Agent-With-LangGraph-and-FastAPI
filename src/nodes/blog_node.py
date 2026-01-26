from src.states.blogstate import Blogstate



class blognode:
    def __init__(self,llm):
        self.llm= llm
    
    def title_creation_node(self, state:Blogstate):
        """
        Generates a catchy blog title based on the topic provided in the state.
        """
        print("Inside title creation node")
        if state['topic'] and "topic" in state:
            prompt= """
            Generate a catchy blog title on the topic: {topic}.
            Use the Markdown format for the title. Make sure the title is engaging and relevant to the topic.
            Also consider SEO best practices while creating the title.
            """
            system_message= prompt.format(topic=state['topic'])

            response= self.llm.invoke(system_message).content

            return {'blog':{'title': response}}
        
    def content_generation_node(self, state: Blogstate):
        """
        Generates the main content of the blog based on the title and topic provided in the state.
        """
        print("Inside content generation node")
        if state['topic'] and "blog" in state and "title" in state['blog']:
            prompt= """
            Generates the main content of the blog based on the {title} and {topic} provided in the state.
            Make sure the content is well-structured, informative, and engaging. Also, ensure that the 
            content aligns with the title and topic. Provide the content in Markdown format. No emojis.
            Consider SEO best practices while creating the content. and make sure the content is plagiarism-free."""

            system_message= prompt.format(title= state['blog']['title'], topic= state['topic'])

            response= self.llm.invoke(system_message).content

            return {'blog':{'title': state['blog']['title'], 'content': response}}




