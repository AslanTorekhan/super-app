import streamlit as st
from deep_translator import GoogleTranslator
import qrcode
from PIL import Image
import io
import time

# --- 1. НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="My Super App", layout="centered", page_icon="📱")

# --- 2. УПРАВЛЕНИЕ СОСТОЯНИЕМ (Навигация) ---
# Мы используем "Session State", чтобы помнить, на какой странице мы находимся
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 3. CSS МАГИЯ (Визуал + Скрытие логотипов) ---
st.markdown("""
    <style>
    /* 1. Скрываем все логотипы Streamlit и GitHub */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 2. Фон приложения (Градиент) */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
        color: white;
    }

    /* 3. Стиль кнопок (Плитки меню) */
    div.stButton > button {
        width: 100%;
        height: 100px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        color: white;
        font-size: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Эффект при наведении */
    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
        border-color: #00d4ff;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
    }

    /* 4. Заголовки */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(45deg, #00d4ff, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* 5. Инпуты и поля */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. ФУНКЦИИ СТРАНИЦ ---

def show_home():
    st.title("MY OS 2.0")
    st.write("👋 Привет, Вайбкодер!")
    
    # Сетка кнопок 2x2
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬛ QR Код"):
            navigate_to('qr')
        if st.button("🎵 Музыка"):
            navigate_to('music')
            
    with col2:
        if st.button("🌍 Перевод"):
            navigate_to('translate')
        if st.button("🤖 AI Чат"):
            navigate_to('ai')

def show_qr():
    if st.button("⬅ Назад"):
        navigate_to('home')
        
    st.header("Генератор QR")
    
    tab1, tab2 = st.tabs(["Ссылка", "Wi-Fi"])
    
    with tab1:
        url = st.text_input("Вставь ссылку", "https://t.me/...")
        if st.button("Создать QR", key="btn_url"):
            generate_qr(url)
            
    with tab2:
        ssid = st.text_input("Имя сети (Wi-Fi)")
        password = st.text_input("Пароль", type="password")
        if st.button("Создать QR Wi-Fi", key="btn_wifi"):
            data = f"WIFI:S:{ssid};T:WPA;P:{password};;"
            generate_qr(data)

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Конвертация
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.image(byte_im, width=250)
    st.download_button("Скачать", data=byte_im, file_name="qr.png", mime="image/png")

def show_translate():
    if st.button("⬅ Назад"):
        navigate_to('home')
    
    st.header("Переводчик")
    text = st.text_area("Введите текст")
    lang = st.selectbox("На язык:", ["ru", "kk", "en", "tr", "es", "fr"])
    
    if st.button("Перевести 🚀"):
        try:
            res = GoogleTranslator(source='auto', target=lang).translate(text)
            st.success(res)
        except Exception as e:
            st.error("Ошибка сети")

def show_music():
    if st.button("⬅ Назад"):
        navigate_to('home')
    st.header("Плеер")
    st.info("Пока работает только загрузка файла")
    fl = st.file_uploader("MP3", type=["mp3"])
    if fl:
        st.audio(fl)

def show_ai():
    if st.button("⬅ Назад"):
        navigate_to('home')
    st.header("AI Помощник")
    st.write("Скоро здесь будет мощь OpenAI...")
    st.text_input("Спроси что-нибудь...")

# --- 5. ГЛАВНЫЙ РОУТЕР (Переключатель) ---
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