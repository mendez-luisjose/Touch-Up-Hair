from requests.exceptions import Timeout
import streamlit as st
import requests

API_URL_ENDPOINT = st.secrets["API_URL_ENDPOINT"]

def modify_hair() :
    """
    Modify the Hair of an Image with Generative AI or GANs
    """  
    try :

        if st.session_state.img_hair != None :
            automatic_hair_root_area = st.session_state.automatic_hair_root_area
            hair_color = ""
            inpaint_option = "Touch-up Hair Roots"
            hex_color_name = st.session_state.hex_color_name

            bytes_data = st.session_state.img_hair.getvalue()
            #resp = requests.post(API_URL_ENDPOINT, data={"inpaint_option": inpaint_option, "hair_color": hair_color, "automatic_hair_root_area": automatic_hair_root_area}, files={'file': bytes_data})

            #st.write(resp.content)
            #st.session_state.final_img = resp.content
            st.session_state.final_img = st.session_state.img_hair

            return "Hair Modified Successfully!"
        else :
            return "Upload an Image!"
    except Timeout as e:
        return f"An unexpected Timeout error occurred. {e} Try Again."
    except Exception as e:
        return f"An unexpected error occurred. {e} Try Again."
    except :
        return f"An unexpected error occurred. Try Again."
    
def change_hair_color(hair_color) :
    """
    Modify the Color of the Hair in an Image with Generative AI or GANs
    """  
    try :
        if st.session_state.img_hair != None :
            automatic_hair_root_area = st.session_state.automatic_hair_root_area
            inpaint_option = "Touch-up whole Hair"
            hex_color_name = st.session_state.hex_color_name

            bytes_data = st.session_state.img_hair.getvalue()
            #resp = requests.post(API_URL_ENDPOINT, data={"inpaint_option": inpaint_option, "hair_color": hair_color, "automatic_hair_root_area": automatic_hair_root_area}, files={'file': bytes_data})

            #st.write(resp.content)
            #st.session_state.final_img = resp.content
            st.session_state.final_img = st.session_state.img_hair

            return "Hair Modified Successfully!"
        else :
            return "Upload an Image!"
    except Timeout as e:
        return f"An unexpected Timeout error occurred. {e} Try Again."
    except Exception as e:
        return f"An unexpected error occurred. {e} Try Again."
    except :
        return f"An unexpected error occurred. Try Again."
