#Defining the structure of the blog state using Pydantic and TypedDict
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field

# Defining the Blog model with title and content
class Blog(BaseModel):
    title: Annotated[str, Field(description=" Title of the blog")]
    content: Annotated[str, Field(description="Main Content of the blog")]


# Defining the Blogstate TypedDict to represent the state of the blog generation process
class Blogstate(TypedDict):
    topic: Annotated[str, Field(description=" Title of the blog")]
    # Blog model is used to represent the blog details
    blog: Annotated[Blog, Field(description=" Content of the blog")]
    language_content: Annotated[str, Field(description=" Language of the blog blog")]



    