from pydantic import BaseModel, Field
from langchain_core.tools import tool
from retouch_tools import modify_hair, change_hair_color, change_hair_style, change_hair_color_with_hexcode

class ColorNameInput(BaseModel):
    hair_color: str = Field(description="color name in the user's request", default="", exclude=None)

class HairStyleInput(BaseModel):
    hair_style: str = Field(description="hair style name in the user's request", default="", exclude=None)

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
    If the color name is not recognized or the user does not give a color name, use always the parameter "".
    """
    return change_hair_color(hair_color)


@tool("change_hair_color_with_hexcode", return_direct=True) 
def tool_change_hair_color_with_color_picker() :
    """
    Use this tool when a user wants to change the color of the hair in an image.
    You do not need to identify the color name from the user's request.
    Usually, the requests will look like 'Change the hair color' or 'Change the color of the hair'. 
    """
    return change_hair_color_with_hexcode()

@tool("change_hair_style", args_schema=HairStyleInput, return_direct=True) 
def tool_change_hair_style(hair_style: str) -> str :
    """
    Use this tool when a user wants to change the style of the hair in an image.
    You will need to identify the style name from the user's request.
    Usually, the requests will look like 'Change the hair style with {hair_style}' or 'Change the style of the hair to {hair_style}'. 
    The parameter of the hair color must be of type string.
    """
    return change_hair_style(hair_style)

re_tools = [
    tool_modify_hair,
    tool_change_hair_color,
    tool_change_hair_color_with_color_picker,
    tool_change_hair_style
]
