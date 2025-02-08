import streamlit as st
import pyttsx3
import tempfile

# Diccionario con palabras a traducir
diccionario = {
    # Agrega aquí tus traducciones
    # 'a': 'uno ',
    # 'b': 'dos ',
    # 'c': 'tres ',
    # 'd': 'cuatro ',
    # 'e': 'cinco ',
    # 'f': 'seis ',
    # 'g': 'siete ',
    # 'mi': 'ri ',
    # 'tuyo': 'tu ',
    # 'mío': 'mi ',
}

def traducir_oracion(oracion):
    palabras = oracion.split()
    oracion_traducida = " ".join([diccionario.get(palabra.lower(), palabra) for palabra in palabras])
    return oracion_traducida

def reproducir_audio(texto):
    engine = pyttsx3.init()
    # Ajustar la velocidad de la voz
    rate = engine.getProperty('rate')
    engine.setProperty('rate', int(rate * 1.25))  # Aumentar la velocidad al 125%

    # Crear un archivo temporal para guardar el audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        engine.save_to_file(texto, tmp.name)
        engine.runAndWait()
        return tmp.name  # Retorna la ruta del archivo temporal

st.title("Texto a Voz")

# Estado de la sesión para la traducción
if 'oracion_traducida' not in st.session_state:
    st.session_state.oracion_traducida = ""

# Opción para introducir texto
oracion_usuario = st.text_area("Introduce una oración :", height=200)

# Botón para ejecutar la traducción
if st.button("ir"):
    if oracion_usuario:
        oracion_traducida = traducir_oracion(oracion_usuario)
        st.session_state.oracion_traducida = oracion_traducida
        audio_file_path = reproducir_audio(oracion_traducida)  # Usando pyttsx3
        st.audio(audio_file_path, format='audio/mp3')

        # Botón para descargar el archivo de audio
        with open(audio_file_path, 'rb') as audio_file:
            st.download_button(
                label="Descargar audio en MP3",
                data=audio_file,
                file_name="audio.mp3",
                mime="audio/mp3"
            )
    else:
        st.warning("Por favor, introduce una oración antes de traducir.")
