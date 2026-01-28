from src.states.blogstate import Blogstate

# Defining the blognode class to handle blog generation and translation
class blognode:
    # Blog node needs LLM to generate and translate blog content
    def __init__(self,llm):
        self.llm= llm
    
    # Node to generate blog title: Need graphstate as input
    def title_creation_node(self, state:Blogstate):
        """
        Generates a catchy blog title based on the topic provided in the state.
        : Takes the topic from the state and uses LLM to generate a title.
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
        
    # Node to generate blog content: Need graphstate as input
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
            Consider SEO best practices while creating the content. and make sure the content is plagiarism-free.
            Have a conclusion at the end of the blog.Have a minimum of 500 words.
            """

            system_message= prompt.format(title= state['blog']['title'], topic= state['topic'])

            response= self.llm.invoke(system_message).content

            return {'blog':{'title': state['blog']['title'], 'content': response}}
        

    def language_router_node(self, state: Blogstate):
        """
        Routes to the appropriate translation node based on the desired language specified in the state.
        """
        print("Inside language router node")
        if 'language_content' in state:
            language= state.get('language_content','english')

            if language == "telugu":
                return "telugu"
            elif language == "spanish":
                return "spanish"
            elif language == "french":
                return "french"
            elif language == "german":
                return "german"
            elif language == "swahili":
                return "swahili"
            else:
                return "english"  # Default to English if language not recognized
            
    def translation_node(self, state: Blogstate, target_language: str):
        """
        Translates the blog content into the specified target language.
        """
        print(f"Inside translation node for {target_language}")

        if "blog" in state and "content" in state['blog']:
            prompt= """
           -  Translate the following blog content into {target_language}:
            {content}
           -  Ensure that the translation maintains the original meaning and tone of the content.
            Provide the translated content in Markdown format. No emojis.
           -  Consider cultural nuances and context while translating the content.
            """

            system_message= prompt.format(target_language= target_language, content= state['blog']['content'])

            response= self.llm.invoke(system_message).content

            return {'blog':{'title': state['blog']['title'], 'content': response}}
    
    


        


