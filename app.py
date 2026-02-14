import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import qrcode
from PIL import Image
import io

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="My Super App", layout="wide")

# --- БОКОВОЕ МЕНЮ ---
st.sidebar.title("Меню")
app_mode = st.sidebar.selectbox("Выбери инструмент", 
    ["QR-Генератор", "Переводчик", "Музыка", "AI Инструменты"])

# ================= QR ГЕНЕРАТОР (НОВОЕ) =================
if app_mode == "QR-Генератор":
    st.header("⬛ Генератор QR-кодов")
    
    qr_type = st.radio("Что шифруем?", ["Ссылка / Текст", "Wi-Fi Сеть"])
    
    if qr_type == "Ссылка / Текст":
        text_input = st.text_input("Вставь ссылку или текст", "https://instagram.com")
        data_to_encode = text_input
        
    elif qr_type == "Wi-Fi Сеть":
        wifi_name = st.text_input("Название сети (SSID)")
        wifi_password = st.text_input("Пароль", type="password")
        # Формат для Wi-Fi: WIFI:S:MyNetwork;T:WPA;P:MyPassword;;
        data_to_encode = f"WIFI:S:{wifi_name};T:WPA;P:{wifi_password};;"

    if st.button("Создать QR"):
        if data_to_encode:
            # Генерация
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(data_to_encode)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Конвертация для Streamlit
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            st.image(img_byte_arr, caption="Твой QR-код", width=300)
            
            # Кнопка скачивания
            st.download_button(label="Скачать картинку", 
                               data=img_byte_arr,
                               file_name="qr_code.png",
                               mime="image/png")

# ================= ПЕРЕВОДЧИК =================
elif app_mode == "Переводчик":
    st.header("🌍 Переводчик (Google)")
    text = st.text_area("Текст для перевода")
    lang = st.selectbox("На какой язык?", ["ru", "kk", "en", "tr"])
    
    if st.button("Перевести"):
        try:
            res = GoogleTranslator(source='auto', target=lang).translate(text)
            st.success(res)
        except Exception as e:
            st.error(f"Ошибка: {e}")

# ================= МУЗЫКА =================
elif app_mode == "Музыка":
    st.header("🎵 Плеер")
    st.info("Загрузи mp3 файл, чтобы послушать")
    uploaded_file = st.file_uploader("Файл", type=["mp3"])
    if uploaded_file:
        st.audio(uploaded_file, format='audio/mp3')

# ================= AI =================
elif app_mode == "AI Инструменты":
    st.header("🤖 AI Помощник")
    st.warning("Сюда потом добавим ChatGPT, когда получим API ключ")