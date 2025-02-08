import streamlit as st
from gtts import gTTS
import tempfile
from pydub import AudioSegment

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

def reproducir_audio(texto, lang):
    tts = gTTS(text=texto, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        tts.save(tmp.name)
        return tmp.name  # Retorna la ruta del archivo temporal

def cambiar_velocidad_audio(audio_path, velocidad):
    # Cargar el archivo de audio
    audio = AudioSegment.from_file(audio_path)
    # Cambiar la velocidad
    nuevo_audio = audio.speedup(playback_speed=velocidad)
    # Guardar el nuevo archivo
    nuevo_path = audio_path.replace('.mp3', f'_velocidad_{velocidad}.mp3')
    nuevo_audio.export(nuevo_path, format='mp3')
    return nuevo_path

st.title("Texto a Voz")

# Estado de la sesión para la traducción
if 'oracion_traducida' not in st.session_state:
    st.session_state.oracion_traducida = ""

# Opción para introducir texto
oracion_usuario = st.text_area("Introduce una oración :", height=200)

# Opción para seleccionar la velocidad
velocidad = st.slider("Selecciona la velocidad de reproducción:", 1.0, 2.0, 1.25)

# Botón para ejecutar la traducción
if st.button("ir"):
    if oracion_usuario:
        oracion_traducida = traducir_oracion(oracion_usuario)
        st.session_state.oracion_traducida = oracion_traducida
        audio_file_path = reproducir_audio(oracion_traducida, 'es')  # Usando español por defecto
        
        # Cambiar la velocidad del audio
        audio_file_path_modificado = cambiar_velocidad_audio(audio_file_path, velocidad)
        
        # Reproducir el audio modificado
        st.audio(audio_file_path_modificado, format='audio/mp3')

        # Botón para descargar el archivo de audio modificado
        with open(audio_file_path_modificado, 'rb') as audio_file:
            st.download_button(
                label="Descargar audio en MP3",
                data=audio_file,
                file_name=f"audio_velocidad_{velocidad}.mp3",
                mime="audio/mp3"
            )
    else:
        st.warning("Por favor, introduce una oración antes de traducir.")
