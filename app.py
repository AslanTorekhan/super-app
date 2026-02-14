import streamlit as st
from deep_translator import GoogleTranslator
import qrcode
from PIL import Image
import io
import time

# --- 1. НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="VibeOS", layout="centered", page_icon="⚡")

# --- 2. STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# --- 3. CSS (СТИЛЬ REACT BITS) ---
st.markdown("""
    <style>
    /* Убираем лишнее */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ФОН: Глубокий космос + Сетка */
    .stApp {
        background-color: #0e0e12;
        background-image: radial-gradient(at 50% 0%, #2b2b45 0px, transparent 50%),
                          radial-gradient(at 100% 0%, #3a1c71 0px, transparent 50%);
        color: #e0e0e0;
    }

    /* ЗАГОЛОВОК: Градиентный текст */
    h1 {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
        text-align: center;
        padding-bottom: 20px;
    }
    
    h2, h3 {
        color: #ffffff;
        font-weight: 600;
    }

    /* КНОПКИ-КАРТОЧКИ (Главная фишка) */
    div.stButton > button {
        width: 100%;
        height: 120px; /* Высокие карточки */
        background: rgba(255, 255, 255, 0.03); /* Почти прозрачные */
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px; /* Сильное скругление */
        color: #e0e0e0;
        font-size: 18px;
        font-weight: 500;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Пружинистая анимация */
        backdrop-filter: blur(10px);
    }
    
    /* Эффект при наведении (Glow Effect) */
    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: #00C9FF;
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 30px -10px rgba(0, 201, 255, 0.4);
        color: white;
    }
    
    /* Инпуты (поля ввода) */
    .stTextInput > div > div > input {
        background-color: #1a1a20;
        color: white;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 10px;
    }
    
    /* Табы */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
        color: white;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00C9FF !important;
        color: black !important;
        font-weight: bold;
    }
    
    /* Линии разделители */
    hr {
        border-color: rgba(255,255,255,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. ЭКРАНЫ ---

def show_home():
    st.title("VIBE OS")
    st.markdown("<p style='text-align: center; color: #888; margin-bottom: 40px;'>Твой личный цифровой хаб</p>", unsafe_allow_html=True)
    
    # Сетка
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("") # отступ
        if st.button("⬛\nQR Code"):
            navigate_to('qr')
        st.write("") 
        if st.button("🎵\nMusic Vibe"):
            navigate_to('music')
            
    with col2:
        st.write("") 
        if st.button("🌍\nTranslate"):
            navigate_to('translate')
        st.write("") 
        if st.button("🤖\nAI Core"):
            navigate_to('ai')

def show_qr():
    if st.button("← Back", key="back"):
        navigate_to('home')
        
    st.title("QR Generator")
    
    tab1, tab2 = st.tabs(["🔗 Ссылка", "📶 Wi-Fi"])
    
    with tab1:
        st.write("Создай QR для любой ссылки или текста")
        url = st.text_input("Вставь ссылку", "https://instagram.com")
        if st.button("Сгенерировать QR", key="btn_url"):
            generate_qr(url)
            
    with tab2:
        st.write("Поделись Wi-Fi без пароля")
        ssid = st.text_input("Имя сети (SSID)")
        password = st.text_input("Пароль", type="password")
        if st.button("Сгенерировать Wi-Fi QR", key="btn_wifi"):
            data = f"WIFI:S:{ssid};T:WPA;P:{password};;"
            generate_qr(data)

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#000000", back_color="#ffffff")
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.image(byte_im, width=300)
    st.download_button("Скачать PNG", data=byte_im, file_name="qr_vibe.png", mime="image/png")

def show_translate():
    if st.button("← Back"):
        navigate_to('home')
    
    st.title("Neural Translate")
    text = st.text_area("Что переводим?", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        lang = st.selectbox("Язык", ["ru", "kk", "en", "tr", "ja", "de"])
    with col2:
        if st.button("Translate ⚡"):
            try:
                res = GoogleTranslator(source='auto', target=lang).translate(text)
                st.success(res)
            except:
                st.error("Ошибка соединения")

def show_music():
    if st.button("← Back"):
        navigate_to('home')
    st.title("Music Lab")
    
    # Визуальный обман (фейковый плеер)
    st.markdown("""
        <div style="background: #1a1a20; padding: 20px; border-radius: 20px; text-align: center; border: 1px solid #333;">
            <h3 style="margin:0">Vibe FM</h3>
            <p style="color: #666;">Waiting for track...</p>
        </div>
        <br>
    """, unsafe_allow_html=True)
    
    fl = st.file_uploader("Загрузи MP3", type=["mp3"])
    if fl:
        st.audio(fl)

def show_ai():
    if st.button("← Back"):
        navigate_to('home')
    st.title("AI Core")
    
    st.markdown("""
        <div style="padding: 20px; background: rgba(0, 201, 255, 0.1); border-radius: 15px; border-left: 5px solid #00C9FF;">
            Система ожидает подключения API OpenAI. <br>
            <b>Status:</b> Offline
        </div>
    """, unsafe_allow_html=True)

# --- 5. ЗАПУСК ---
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'qr':
    show_qr()
elif st.session_state.page == 'translate':
    show_translate()
elif st.session_state.page == 'music':
    show_music()
elif st.session_state.page == 'ai':
    show_ai()