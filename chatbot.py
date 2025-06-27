import streamlit as st
from groq import Groq 

st.set_page_config(page_title="Mi chat de IA", page_icon="🤖", layout="centered")

st.title("Mi primera aplicacion con Streamlit")

nombre = st.text_input("¿Cúal es tu nombre?: ")

if st.button("Saludar"):
    st.write(f"¡Hola {nombre}! Bienvenido/a a mi chatbot.")


modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'gemma2-9b-it']

def configurar_pagina():
    st.title("Mi Chat")
    st.sidebar.title("Configurar la IA")
    elegirModelo = st.sidebar.selectbox("Elegi un modelo",options=modelos,index=0)
    return elegirModelo

#Funcion que nos ayuda a conectar con Groq
def crear_usuario_groq():
    claveSecreta = st.secrets["clave_api"]
    return Groq(api_key=claveSecreta)

#Configurar el modelo y el mensaje del usuario. 
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages =[{"role":"user", "content": mensajeDeEntrada}],
        stream=True
    )

def incializacion_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

#CLASE 8
#Actualizar historial 
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role":rol, "content":contenido , "avatar": avatar})

#Mostar Hisotiral 
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

#Area Historial 
def area_chat():
    contenedorDelChat = st.container(height=300, border=True)
    with contenedorDelChat:
        mostrar_historial()

#Clase #9
#Generar repuesta (voy a capturar la respuesta del modelo)
def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa


def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    incializacion_estado()
    area_chat()
    mensaje = st.chat_input("Escribí tu mensaje")
    if mensaje:
        actualizar_historial("user", mensaje, "👦")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")

            st.rerun()

if __name__ == "__main__":
    main() 
    