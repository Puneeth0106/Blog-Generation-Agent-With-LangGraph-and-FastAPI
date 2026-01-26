from typing import TypedDict, Annotated
from pydantic import BaseModel, Field


class Blog(BaseModel):
    title: Annotated[str, Field(description=" Title of the blog")]
    content: Annotated[str, Field(description="Main Content of the blog")]



class Blogstate(TypedDict):
    topic: Annotated[str, Field(description=" Title of the blog")]
    blog: Annotated[Blog, Field(description=" Content of the blog")]
    language_content: Annotated[str, Field(description=" Language of the blog blog")]



    