import streamlit as st
import matplotlib.pyplot as plt
import random

# Добавляем заголовок и подзаголовок
st.title("Лабораторная работа №5")
st.subheader("Исследование сигнализатора заземления")

# Выводим изображение
st.image("СЗИ.jpg", caption="Рисунок 1 - Схема сигнализатора заземления", use_column_width=True)

# генерируем рандомное число 
random_number = random.uniform(-0.003, 0.003)

# Выводим рандомное число
st.write(f'Ваше рандомизированное число: {random_number}')

# Инициализируем массив в сессионном состоянии
if 'data_array' not in st.session_state:
    st.session_state.data_array = []

# Ввод значения напряжения контролируемого СЗИ
Uinput = st.number_input('Введите Контролируемое напряжение СЗИ', min_value=21, max_value=27, value="min", step=1)
st.write('Uконтр СЗИ-1 = ', Uinput, ' В')
K0 = Uinput/170-0.1 # Расчет коэффициента смещения графика от входного напряжения
st.write('Коэффициент К0 = ', K0, ' В')
# Тут будет рандом
# U01 = U0 + st.session_state.random_number
#st.write('Uвых R ПЧ-50/25 = ', U01, ' В')

# Добавляем слайдер с сопротивлением заземления
Rzaz = st.slider("Сопротивление заземления", 5, 100, 95)

# Рассчитывае ток утечки
Iut1 = -0.00263*Rzaz+0.713-K0+random_number
Iut = round(Iut1, 2)
if Iut > 0.6:
    st.error('Сработал сигнализатор заземления')
st.write("Сопротивление заземления", Rzaz, 'кОм')
st.write("Ток утечки", Iut, 'мA')

# Обработчик событий для слайдера
if st.button("Добавить в массив"):
    # Добавляем кортеж в массив
    st.session_state.data_array.append((Rzaz, Iut))
    st.success(f"Добавлено в массив: ({Rzaz}, {Iut})")

# Выводим все значения массива Вариант 2
st.write("Значения массива:", ", ".join([f"({x}, {y})" for x, y in st.session_state.data_array]))

# Построение графика
if st.button("Построить график"):
    # Извлекаем значения из массива для построения графика
    x_values = [item[0] for item in st.session_state.data_array]
    y_values = [item[1] for item in st.session_state.data_array]

    # Строим график
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values, marker='o')
    ax.set_ylabel('Напряжение на нагрузке')
    ax.set_xlabel('Ток нагрузки')
    ax.set_title('Нагрузочная характеристика')
    # Добавляем сетку
    ax.grid(True)
    # Отображаем график
    st.pyplot(fig)
