import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_groq import ChatGroq
import time
from langchain_core.output_parsers import StrOutputParser
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import numpy as np
from PIL import Image, ImageColor
from util import get_colour_name, speech_to_text
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import uuid
from template import MESSAGE
import requests

if "img_hair" not in st.session_state :
    st.session_state.img_hair = None  

if "agent" not in st.session_state :
    st.session_state.agent = None  

if "final_img" not in st.session_state :
    st.session_state.final_img = None  

if "hair_imgs_dict" not in st.session_state :
    st.session_state.hair_imgs_dict = {}

if "hair_imgs_generated_count" not in st.session_state :
    st.session_state.hair_imgs_generated_count = 0 

if "agent_results" not in st.session_state :
    st.session_state.agent_results = 0 

if "automatic_hair_root_area" not in st.session_state :
    st.session_state.automatic_hair_root_area = False

if "hex_color_name" not in st.session_state :
    st.session_state.hex_color_name = None

if "speech_to_text_history" not in st.session_state :
    st.session_state.speech_to_text_history = []

if "audio_response" not in st.session_state :
    st.session_state.audio_response = False

HUGGINGFACEHUB_API_TOKEN = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
API_TRANSLATION = st.secrets["API_TRANSLATION"]

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

img_file = None

if "chat_history" not in st.session_state :
    st.session_state.chat_history = [AIMessage(content=MESSAGE),]

st.set_page_config(page_title="Touch-Up Hair", page_icon="💈", layout="wide")

example_prompts = [
    "¿Cómo funciona esta aplicación?",
    "¿Cual es tu función?",
    "Dime qué puedes hacer.",
    "¿Esta App es de uso gratuito?"
]

def get_es_to_en(text) :
    data = {
        "text": text,
        "dest": "en",
        "src": "es"
    }
    
    resp = requests.post(API_TRANSLATION, json=data)

    translation = resp.json()["trans"]

    return translation

def get_en_to_es(text) :
    data = {
        "text": text,
        "dest": "es",
        "src": "en"
    }
    
    resp = requests.post(API_TRANSLATION, json=data)

    translation = resp.json()["trans"]

    return translation


def get_agent_response(user_query) :
    #st_callback = StreamlitCallbackHandler(st.container())

    transcription_en = get_es_to_en(user_query)


    result = st.session_state.agent.invoke(
        {"input": transcription_en}, config={"configurable": {"session_id": "<foo>"}})
    result = result["output"]

    transcription_es = get_en_to_es(result)

    return transcription_es

def get_agent_action(user_query) :
    st.session_state.chat_history.append(HumanMessage(content=user_query))
            
    with st.chat_message("user") :
        st.markdown(user_query)

    with st.chat_message("assistant") :
        with st.spinner("Generando Respuesta...") :
            ai_response = get_agent_response(user_query)
            
        message_placeholder = st.empty()
        full_response = ""
        # Simulate a streaming response with a slight delay
        for chunk in ai_response.split():
            full_response += chunk + " "
            time.sleep(0.05)

            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        
        # Display the full response
        message_placeholder.info(full_response)

        #if final_hair_img != None and ai_response == "Hair Modified Successfully!" :
        if ai_response == "¡Cabello modificado con éxito!" :
            progress_bar = st.progress(0)

            for perc_completed in range(100) :
                time.sleep(0.001)
                progress_bar.progress(perc_completed+1)
                
            _,  col_img, _ = st.columns([0.85, 1, 0.85])
            col_img.image(st.session_state.final_img, use_container_width=True)
            #col_img.image(st.session_state.img_hair, use_column_width=True)


            #col_img.button("Download Image", use_container_width=True, key=f"Button {str(st.session_state.hair_imgs_generated_count)}", icon="⏬")

            buf = BytesIO()
            pillow_img = Image.open(BytesIO(st.session_state.final_img)).convert('RGB')
            #pillow_img = Image.open(st.session_state.final_img).convert('RGB')
            pillow_img.save(buf, format="JPEG")
            byte_im = buf.getvalue()

            col_img.download_button(
                label="Descargar Imagen",
                data=byte_im,
                file_name='{}.jpeg'.format(uuid.uuid1()),
                mime="image/jpeg",
                icon="⏬",
                use_container_width=True,
                key=f"Button {str(st.session_state.hair_imgs_generated_count)}"
                )  

            st.session_state.hair_imgs_dict[str(st.session_state.hair_imgs_generated_count)] = st.session_state.final_img
            st.session_state.hair_imgs_generated_count = st.session_state.hair_imgs_generated_count + 1


    st.session_state.chat_history.append(AIMessage(content=ai_response))
    
def main() :
    agent_results = 0
    _, col_1, _ = st.columns([1, 1, 1])
    
    col_1.image("./imgs/7.png")

    st.write(" ")
    st.write(" ")

    with st.expander("🌐 ¿En que Consiste y como Utilizar esta Aplicacion?"):
        st.subheader("🦜 ¿En que Consiste esta Aplicacion?")
        st.write("La presente aplicacion consiste en un app que permite mediante la utilizacion de LangChain, poder modificar el cabello de una persona usando un ChatBot facil e interactivo con el usuario.")
        st.write("La tecnologia que se utiliza para el ChatBot se llama LangChain, en el cual es un marco para desarrollar aplicaciones basadas en modelos de lenguaje de gran tamaño (LLM). LangChain funciona como una interfaz genérica para casi cualquier LLM, brindando un entorno de desarrollo centralizado para crear aplicaciones LLM e integrarlas con fuentes de datos externas y flujos de trabajo de software. ")
        st.info("Para poder realizar la modificacion del cabello, solamente hace falta subir la fota en la barra lateral y decirle al ChatBot los cambios que se quieren realizar, como retocar las raices o cambiar el color del pelo a cualquier color.")
        st.divider()
        _, col3, col4, _ = st.columns([1, 1, 1, 1], gap="large", vertical_alignment="center")

        col3.image("./imgs/img-prev-1.jpg", use_container_width=True, caption="Imagen Original 🖼️")
        col4.image("./imgs/img-prev-result-1.jpeg", use_container_width=True, caption="Imagen Generada💈")

        st.divider()


        st.subheader("🖥️ Tecnologia Stable Diffusion")
        st.write("La tecnologia para poder editar la imagen original del cabello se llama Stable Diffusion, especificamente se esta utilizando el modelo de Inpaint de Realistic Vision. Asi gracias al prompt del usuario, y las capas de redes neuronales convolucionales y las capas de Encoder y Decoder, se logra producir la nueva imagen.")
        st.caption("Diagrama de Stable Diffusion:")
        _,  col_2, _ = st.columns([0.4, 1, 0.4])
        col_2.image("./imgs/stable-diffusion-unet-steps.png", use_container_width=True)
        #col_2.image("./imgs/2.jpg", use_column_width=True)
        st.divider()

        st.markdown(
            """
            Estas son todas las modificaciones que el usuario puede realizar:
            
            - Cambiar el color del Cabello: El usuario puede modificar el color del cabello a cualquier otro color con solo decirle al ChatBot.
            - Retoque de Raices: Se puede modificar las raices que no estan del mismo color del pelo tiñado o descolorado, para asi que todo el cabello poseea un mismo color.
            - Estilos: Se puede cambiar el estilo o la apariencia del cabello y el color de la persona.
            """
        )

        st.divider()
        _, col5, col6, _ = st.columns([1, 1, 1, 1], gap="large", vertical_alignment="center")

        col5.image("./imgs/img-prev-2.jpg", use_container_width=True, caption="Imagen Original 🖼️")
        col6.image("./imgs/img-prev-result-2.jpeg", use_container_width=True, caption="Imagen Generada 💈")


    st.divider()

    with st.sidebar:     
        st.sidebar.caption("🧑🏻‍💻 App de Retoque de Cabello Programada por [Luis Jose Mendez](https://github.com/mendez-luisjose)")
        st.info("**Comienza a Usar la App ↓**", icon="👋🏻")
    
        with st.expander("🌐 Aplicacion ReTouch", expanded=True):
            st.title("🦜 Agente con LangChain")
            #st.divider()
            st.caption("🖼️ Carga las Imagenes que quieras Modificar.")
            #st.divider()
            st.success("Imagenes Compatibles como PNG, JPG o JPEG")

            st.divider()

            st.write(
                """
                Recuerda cargar primero la Imagen para que el Chatbot puede iniciar. \n
                """
            )

            st.info("❗Solo se puede cargar una Imagen a la vez.")
            st.header("📍 Explora")
            st.caption(
                """
                Puedes realizar desde ajuste de raices, cambio de color del cabello o modificar el estilo del pelo. \n
                """
            )
            #option = st.multiselect("Options:", ["ReTouch", "Tutorial"], default=["ReTouch"], max_selections=1)

        #if len(option) !=0 :
            #option = option[0]

    st.caption("🚀 Alimentado con Stable Diffusion, Gemini y LangChain")
    for index, message in enumerate(st.session_state.chat_history) :
        if isinstance(message, HumanMessage) :
            with st.chat_message("user") :
                st.markdown(message.content)
        else :
            with st.chat_message("assistant") :
                st.markdown(message.content)
                if len(st.session_state.hair_imgs_dict) !=  0 and message.content == "¡Cabello modificado con éxito!" :
                    #for i in range(0, len(st.session_state.hair_imgs_list)) :
                    _,  col, _ = st.columns([0.85, 1, 0.85])
                    #col.image(final_hair_img, use_column_width=True, width=300)
                    #col.image(st.session_state.img_hair, width=300)

                    col.image(st.session_state.hair_imgs_dict[str(agent_results)], use_container_width=True)
                    #col.button("Download Image", use_container_width=True, key=f"Button {str(agent_results)}", icon="⏬")
                    buf = BytesIO()
                    pillow_img = Image.open(BytesIO(st.session_state.hair_imgs_dict[str(agent_results)])).convert('RGB')
                    #pillow_img = Image.open(st.session_state.hair_imgs_dict[str(agent_results)]).convert('RGB')
                    pillow_img.save(buf, format="JPEG")
                    byte_im = buf.getvalue()

                    col.download_button(
                        label="Descargar Imagen",
                        data=byte_im,
                        file_name='{}.jpeg'.format(uuid.uuid1()),
                        mime="image/jpeg",
                        icon="⏬",
                        use_container_width=True,
                        key=f"Button {str(agent_results)}"
                        )  

                    agent_results =  agent_results + 1



    #st.write(st.session_state.chat_history)


    button_cols = st.columns(4)

    user_query = ""

    if button_cols[0].button(example_prompts[0], help="Ejemplo de Prompt", key="Boton1", use_container_width=True, on_click=None):
        user_query = example_prompts[0]
        #response_action(user_query)
        get_agent_action(user_query)
    elif button_cols[1].button(example_prompts[1], help="Ejemplo de Prompt", key="Boton2", use_container_width=True, on_click=None):
        user_query = example_prompts[1]
        get_agent_action(user_query)
    elif button_cols[2].button(example_prompts[2], help="Ejemplo de Prompt", key="Boton3", use_container_width=True, on_click=None):
        user_query = example_prompts[2]
        get_agent_action(user_query)
    elif button_cols[3].button(example_prompts[3], help="Ejemplo de Prompt", key="Boton4", use_container_width=True, on_click=None):
        user_query = example_prompts[3]
        get_agent_action(user_query)

    with st.sidebar.expander("Configuracion ReTouch", icon="⚙️") :
        camera_photo = None
        enable = st.checkbox("Toma una Foto con tu Camara", value=False, help="Habilita esta casilla para acceder a la camara.")

        st.session_state.audio_response = st.checkbox("Respuesta con Voz IA", value=False, help="Habilita esta casilla para respuesta con voz.")
        st.caption("Prueba esta opcion experimental para mejores resultados.")
        automatic_hair_root_area = st.checkbox("Seleccion Automatica del Area del Cabello", value=True, help="Prueba esta opcion experimental.")
        st.warning("Recuerda que esta opcion es experimental y puede resultar peor o mejor dependiendo de la imagen.")

        st.divider()

        col1, col2 = st.columns([1, 0.3], vertical_alignment="center", gap="medium")
        col1.info("Selecciona un codigo de color de cabello especifico.")
        hex_code_color = col2.color_picker("Escoge:")
        
        rgb_code_color = ImageColor.getcolor(hex_code_color, "RGB")
        actual_name, closest_name = get_colour_name(rgb_code_color)

        if (actual_name == None) :
            hair_color = (closest_name + '.')[:-1]
        elif (actual_name != None) :
            hair_color = (actual_name + '.')[:-1]

        st.session_state.automatic_hair_root_area = automatic_hair_root_area
        st.session_state.hex_color_name = hair_color

        st.divider()
        chat_with_voice = st.checkbox("Activa el Microfono 🎙️", value=False)
        st.warning("Habla con claridad al Microfono. Para grabar presiona el Icono del Microfono.")

        if chat_with_voice :
            footer_container = st.container()
            with footer_container:
                audio_bytes = audio_recorder(text="🔊 Presiona para Activar Microfono.", icon_size="2x")
                
                if (audio_bytes != None) and (chat_with_voice) :
                    with st.spinner("Escuchando..."):
                        webm_file_path = "./temp/temp_audio.mp3"
                        with open(webm_file_path, "wb") as f:
                            f.write(audio_bytes)

                        transcript = speech_to_text(webm_file_path)
                        if transcript!="Error" and transcript!= None:
                            st.session_state.speech_to_text_history.append(transcript)
                            os.remove(webm_file_path)

        elif chat_with_voice!=True :
            st.session_state.speech_to_text_history = []

    if enable :
        camera_photo = st.camera_input(" ")

    with st.sidebar.expander("🖼️ Carga tu Foto", expanded=True) :
        img_file = st.file_uploader("Sube tu Imagen:", type=["jpg", "png", "jpeg"], accept_multiple_files=False)

    if img_file is None and enable is False :
        st.divider()
        st.info("🖼️ Por favor subir una Foto primero para empezar a interactuar con el ChatBot.")
    elif camera_photo is not None or img_file is not None :
        if camera_photo is not None :
            image = np.array(Image.open(camera_photo))
            
            with st.sidebar.expander("🖼️ Preview:", expanded=True) :
                #st.success(" Image Loaded Correctly!", icon="✅")
                _,  img_preview, _ = st.columns([0.5, 1, 0.5])
                #col.image(final_hair_img, use_column_width=True, width=300)
                img_preview.image(image, use_container_width=True)
                #st.image(image, width=200)

            st.session_state.img_hair = camera_photo
        elif img_file is not None :
            image = np.array(Image.open(img_file))
            
            with st.sidebar.expander("🖼️ Preview:", expanded=True) :
                #st.success(" Image Loaded Correctly!", icon="✅")
                _,  img_preview, _ = st.columns([0.5, 1, 0.5])
                #col.image(final_hair_img, use_column_width=True, width=300)
                img_preview.image(image, use_container_width=True)
                #st.image(image, width=200)

            st.session_state.img_hair = img_file


        from ai_agent import initialize_agent
        from ai_tools import re_tools

        agent = initialize_agent(tools=re_tools)

        st.session_state.agent = agent 

        user_query = st.chat_input("Escribe tu mensaje...")
        
        if (user_query is not None and user_query != "") and (chat_with_voice!=True) :
            get_agent_action(user_query)
        elif (chat_with_voice) and (len(st.session_state.speech_to_text_history) > 0):
            user_query = st.session_state.speech_to_text_history[-1]
            get_agent_action(user_query)


    #elif option == "Conversation" :
        #user_query = st.chat_input("Type your message here...")
            
        #if user_query is not None and user_query != "" and (chat_with_voice!=True):
            #response_action(user_query)

    #if enable :
        #st.session_state.camera_photo = st.camera_input(" ")
        #st.session_state.use_camera = True
        
if __name__ == "__main__" :
    main()
