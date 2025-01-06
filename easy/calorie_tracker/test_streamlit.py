import streamlit as st

# Заголовок приложения
st.title("Моё первое Streamlit приложение")

# Текст
st.write("Это простое приложение на Streamlit!")

# Интерактивный элемент
name = st.text_input("Введите ваше имя:")

# Кнопка
if st.button("Поздороваться"):
    st.write(f"Привет, {name}!")
