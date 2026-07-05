import base64
import streamlit as st
from src.agente_final import inicializar_agente

# 1. Función con Caché: Solo lee y convierte la imagen UNA VEZ
@st.cache_data(show_spinner=False)
def obtener_imagen_base64(ruta_imagen):
    with open(ruta_imagen, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# 2. Función que aplica el estilo (ahora es ultrarrápida)
def configurar_imagen_fondo(ruta_imagen):
    try:
        data = obtener_imagen_base64(ruta_imagen)
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{data}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"No se encontró la imagen de fondo en la ruta: {ruta_imagen}")

# Función para codificar la imagen local e inyectarla en el CSS de la app
def configurar_imagen_fondo(ruta_imagen):
    try:
        with open(ruta_imagen, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode()
        
        # Ajuste del fondo para que cubra toda la pantalla de forma fija
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{data}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"No se encontro la imagen de fondo en la ruta: {ruta_imagen}")


# 1. Configuracion de la pagina
st.set_page_config(
    page_title="Veridis AI | Asistente de Colaboradores",
    layout="centered"
)

configurar_imagen_fondo("fondo.png")

# Estilos CSS para mejorar contraste y legibilidad
st.markdown("""
<style>
    /* 1. Sombra fuerte para los titulos principales */
    h1, h2, h3 {
        color: #FFFFFF !important;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.9);
    }

    /* 2. Caja del aviso de IA */
    .ia-disclaimer {
        font-size: 0.85rem;
        color: #FFFFFF;
        background-color: rgba(10, 37, 64, 0.95);
        padding: 12px;
        border-left: 4px solid #D4AF37;
        border-radius: 6px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
    }

    /* 3. Estilizar los contenedores de los mensajes del chat */
    [data-testid="stChatMessage"] {
        background-color: rgba(10, 37, 64, 0.85) !important; /* Azul corporativo con 85% de opacidad */
        border: 1px solid rgba(212, 175, 55, 0.4) !important; /* Borde dorado sutil */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
    }

    /* 4. Forzar que el texto y listas dentro del chat sean blancos y legibles */
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] li {
        color: #FFFFFF !important;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* 5. Ajustar el color de los iconos de usuario/IA en el chat */
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #D4AF37 !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Encabezado
st.title("Veridis Eco-Park & Resort")
st.subheader("Portal de Asistencia Corporativa")
st.markdown('<div class="ia-disclaimer">Aviso: Este es un sistema de Inteligencia Artificial. Las respuestas se generan exclusivamente con base en los manuales oficiales indexados.</div>', unsafe_allow_html=True)

# 3. Carga del agente RAG en cache
@st.cache_resource(show_spinner="Iniciando motor de busqueda...")
def cargar_motor():
    return inicializar_agente()

agente = cargar_motor()

# 4. Inicializar variables de estado
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Renderizado del historial de conversacion
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Sistema de retroalimentacion para respuestas de la IA
        if message["role"] == "assistant":
            col1, col2, _ = st.columns([2, 3, 7]) # Proporciones más amplias
            col1.button("Util", key=f"up_{idx}", use_container_width=True)
            col2.button("No util", key=f"down_{idx}", use_container_width=True)

# 6. Procesamiento de consultas
if prompt := st.chat_input("Ingrese su consulta sobre las politicas del resort..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Consultando base de conocimientos..."):
            try:
                respuesta_ia = agente.invoke(prompt)
                st.markdown(respuesta_ia)
            except Exception as e:
                respuesta_ia = f"Error interno en la consulta. Reportar al area de sistemas. Detalle: {e}"
                st.error(respuesta_ia)
# Botones de evaluacion para la respuesta actual
        col1, col2, _ = st.columns([2, 3, 7]) # Proporciones más amplias
        col1.button("Util", key=f"up_{len(st.session_state.messages)}", use_container_width=True)
        col2.button("No util", key=f"down_{len(st.session_state.messages)}", use_container_width=True)

    st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})