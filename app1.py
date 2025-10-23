import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Configuración de la página (¡un buen detalle!)
st.set_page_config(page_title="App OCR 📸", page_icon="✨")

# --- CSS para el fondo rosado de la cámara ---
# Inyectamos CSS con st.markdown para estilizar el widget de la cámara
st.markdown("""
<style>
/* Apuntamos al contenedor del widget de la cámara por su test-id */
[data-testid="stCameraInput"] {
    background-color: #FFC0CB; /* Rosa pastel (Pink) */
    border: 2px solid #FF69B4; /* Borde rosa más oscuro (HotPink) */
    border-radius: 12px; /* Bordes redondeados */
    padding: 1rem; /* Un poco de espacio interior */
    box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Sombra suave */
}
</style>
""", unsafe_allow_html=True)


# --- Título con Kaomoji ---
st.title("Reconocimiento óptico de Caracteres (๑˃̵ᴗ˂̵)و")
st.write("¡Apunta tu cámara a un texto y mira la magia! ✨")


# --- Barra lateral ---
with st.sidebar:
    st.header("Opciones (o^▽^o)")
    filtro = st.radio(
        "¿Aplicar Filtro?",
        ('Con Filtro (Invertir)', 'Sin Filtro'),
        help="El filtro 'Invertir' (bitwise_not) puede ayudar si el texto es oscuro sobre fondo claro."
    )


# --- Widget de la cámara ---
st.header("Toma una Foto (📸_•́)")
img_file_buffer = st.camera_input("Haz clic aquí para activar la cámara")


if img_file_buffer is not None:
    # Para leer el buffer de la imagen con OpenCV:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    st.info("Procesando imagen... (๑•̀ㅂ•́)و✧")
    
    processed_img = None
    if filtro == 'Con Filtro (Invertir)':
        # Aplicamos el filtro bitwise_not
        processed_img = cv2.bitwise_not(cv2_img)
        st.image(processed_img, caption="Imagen con Filtro Invertido", channels="BGR")
    else:
        # Usamos la imagen tal cual
        processed_img = cv2_img
        # st.image(processed_img, caption="Imagen Original", channels="BGR") # Opcional
        
    
    # Convertir la imagen procesada a RGB (Pytesseract prefiere RGB)
    img_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
    
    # --- Extracción de Texto ---
    st.subheader("Texto Extraído (¬‿¬)")
    with st.spinner('Leyendo el texto... (zZz...)'):
        # Añadí lang='spa' para mejorar la precisión en español. 
        # Cámbialo si esperas otros idiomas.
        try:
            text = pytesseract.image_to_string(img_rgb, lang='spa')
            
            if text:
                st.text_area("Resultado:", text, height=250)
            else:
                st.warning("No se pudo detectar texto. (T_T) Intenta con otra imagen o un filtro diferente.")
        
        except Exception as e:
            st.error(f"Ocurrió un error con Pytesseract: {e} (╯°□°）╯︵ ┻━┻")
            st.info("Asegúrate de tener Tesseract-OCR instalado en el entorno donde corres Streamlit.")

else:
    st.info("Esperando a que tomes una foto... (o_O)")
