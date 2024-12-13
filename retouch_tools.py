from requests.exceptions import Timeout
import streamlit as st
import requests
from util import text_to_speech, text_to_speech_spanish
import time
import base64

API_URL_ENDPOINT = st.secrets["API_URL_ENDPOINT"]
API_TRANSLATION = st.secrets["API_TRANSLATION"]

def get_en_to_es(text) :
    data = {
        "text": text,
        "dest": "es",
        "src": "en"
    }
    
    resp = requests.post(API_TRANSLATION, json=data)

    translation = resp.json()["trans"]

    return translation
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

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

            if st.session_state.audio_response :
                file_path = text_to_speech_spanish(f"Editando las raíces del cabello de la imagen dada... Por favor espere aproximadamente 30 segundos.")
                autoplay_audio(file_path)

            bytes_data = st.session_state.img_hair.getvalue()
            resp = requests.post(API_URL_ENDPOINT, data={"inpaint_option": inpaint_option, "hair_color": hair_color, "automatic_hair_root_area": automatic_hair_root_area}, files={'file': bytes_data})

            #st.write(resp.content)
            st.session_state.final_img = resp.content
    
            #time.sleep(5)
            #st.session_state.final_img = st.session_state.img_hair

            return "¡Cabello modificado con éxito!"
        else :
            return "¡Sube una Imagen!"
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

            if hair_color == "" or hair_color == None :
                hair_color = hex_color_name

            if st.session_state.audio_response :
                file_path = text_to_speech_spanish(f"Cambiando el color del cabello a {get_en_to_es(hair_color)}... Por favor espere aproximadamente 30 segundos.")
                autoplay_audio(file_path)

            bytes_data = st.session_state.img_hair.getvalue()
            resp = requests.post(API_URL_ENDPOINT, data={"inpaint_option": inpaint_option, "hair_color": hair_color, "automatic_hair_root_area": automatic_hair_root_area}, files={'file': bytes_data})

            #st.write(resp.content)
            st.session_state.final_img = resp.content

            #time.sleep(5)

            #st.session_state.final_img = st.session_state.img_hair

            return "¡Cabello modificado con éxito!"
        else :
            return "¡Sube una Imagen!"
    except Timeout as e:
        return f"An unexpected Timeout error occurred. {e} Try Again."
    except Exception as e:
        return f"An unexpected error occurred. {e} Try Again."
    except :
        return f"An unexpected error occurred. Try Again."
    
def change_hair_color_with_hexcode() :
    """
    Modify the Color of the Hair in an Image with Generative AI or GANs
    """  
    try :
        if st.session_state.img_hair != None :
            automatic_hair_root_area = st.session_state.automatic_hair_root_area
            inpaint_option = "Touch-up whole Hair"
            hex_color_name = st.session_state.hex_color_name

            if hex_color_name != "" or hex_color_name != None :
                hair_color = hex_color_name

                if st.session_state.audio_response :
                    file_path = text_to_speech_spanish(f"Cambiando el color del cabello a {get_en_to_es(hair_color)}... Por favor espere aproximadamente 30 segundos.")
                    autoplay_audio(file_path)

                bytes_data = st.session_state.img_hair.getvalue()
                resp = requests.post(API_URL_ENDPOINT, data={"inpaint_option": inpaint_option, "hair_color": hair_color, "automatic_hair_root_area": automatic_hair_root_area}, files={'file': bytes_data})

                #st.write(resp.content)
                st.session_state.final_img = resp.content

            #time.sleep(5)

            #st.session_state.final_img = st.session_state.img_hair

                return "¡Cabello modificado con éxito!"
        else :
            return "¡Sube una Imagen!"
    except Timeout as e:
        return f"An unexpected Timeout error occurred. {e} Try Again."
    except Exception as e:
        return f"An unexpected error occurred. {e} Try Again."
    except :
        return f"An unexpected error occurred. Try Again."
    

def change_hair_style(hair_style) :
    """
    Change the Hair Style of an Image with Generative AI or GANs
    """  
    try :

        if st.session_state.img_hair != None :
            automatic_hair_root_area = st.session_state.automatic_hair_root_area
            hair_color = ""
            inpaint_option = "Change Hair Style"
            hex_color_name = st.session_state.hex_color_name

            if st.session_state.audio_response :
                file_path = text_to_speech_spanish(f"Cambiando el estilo de cabello de la imagen dada... Por favor espere aproximadamente 30 segundos.")
                autoplay_audio(file_path)

            bytes_data = st.session_state.img_hair.getvalue()
            resp = requests.post(API_URL_ENDPOINT, data={"inpaint_option": inpaint_option, "hair_color": hair_color, "automatic_hair_root_area": automatic_hair_root_area, "hair_style": hair_style}, files={'file': bytes_data})

            #st.write(resp.content)
            st.session_state.final_img = resp.content
    
            #time.sleep(5)
            #st.session_state.final_img = st.session_state.img_hair

            return "¡Cabello modificado con éxito!"
        else :
            return "¡Sube una Imagen!"
    except Timeout as e:
        return f"An unexpected Timeout error occurred. {e} Try Again."
    except Exception as e:
        return f"An unexpected error occurred. {e} Try Again."
    except :
        return f"An unexpected error occurred. Try Again."
