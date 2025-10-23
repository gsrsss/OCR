import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS  # Importamos gTTS para el audio
import io  # Importamos io para manejar el audio en memoria

st.title("Reconocimiento óptico de Caracteres (OCR) y TTS")

img_file_buffer = st.camera_input("Toma una Foto")

with st.sidebar:
    st.header("Configuración")
    filtro = st.radio("Aplicar Filtro", ('Sin Filtro', 'Invertir (Blanco/Negro)'))

if img_file_buffer is not None:
    # Para leer la imagen desde el buffer
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Aplicar el filtro seleccionado
    if filtro == 'Invertir (Blanco/Negro)':
        # Convertir a escala de grises primero
        gray_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        # Invertir la imagen (ayuda si el texto es blanco sobre fondo negro)
        processed_img = cv2.bitwise_not(gray_img)
        st.image(processed_img, caption="Imagen con Filtro (Invertida)")
    else:
        # Usar la imagen original
        processed_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        st.image(processed_img, caption="Imagen Original")

    # --- Reconocimiento de Texto (OCR) ---
    st.subheader("Texto Reconocido:")
    try:
        # Usamos la imagen procesada (ya sea original o filtrada) para el OCR
        text = pytesseract.image_to_string(processed_img, lang='spa')  # Especificamos español

        if text.strip():
            st.text_area("Texto", text, height=200)

            # --- Conversión a Audio (TTS) ---
            st.subheader("Escuchar el Texto:")

            # Usamos un buffer en memoria para no guardar el archivo
            audio_buffer = io.BytesIO()
            
            # Creamos el objeto gTTS
            tts = gTTS(text=text, lang='es', slow=False)
            
            # Escribimos el audio en el buffer
            tts.write_to_fp(audio_buffer)
            
            # Mostramos el reproductor de audio en Streamlit
            st.audio(audio_buffer, format='audio/mp3')

        else:
            st.warning("No se pudo detectar texto en la imagen.")

    except Exception as e:
        st.error(f"Ocurrió un error durante el OCR o TTS: {e}")


