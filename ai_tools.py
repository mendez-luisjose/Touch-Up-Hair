from pydantic import BaseModel, Field
from langchain_core.tools import tool
from retouch_tools import modify_hair, change_hair_color

class ColorNameInput(BaseModel):
    hair_color: str = Field(description="color name in the user's request", default="", exclude=None)

@tool("modify_hair", return_direct=True) 
def tool_modify_hair() :
    """
    Use this tool when a user wants to modify the hair or the hair roots of an image.
    """
    return modify_hair()

@tool("change_hair_color", args_schema=ColorNameInput, return_direct=True) 
def tool_change_hair_color(hair_color: str) -> str :
    """
    Use this tool when a user wants to change the color of the hair in an image.
    You will need to identify the color name from the user's request.
    Usually, the requests will look like 'Change the hair color with {hair_color}' or 'Change the color of the hair with {hair_color}'. 
    The parameter of the hair color must be of type string.
    """
    return change_hair_color(hair_color)

re_tools = [
    tool_modify_hair,
    tool_change_hair_color
]