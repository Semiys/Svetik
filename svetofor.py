import tkinter as tk
import timeit

# Функция для измерения времени выполнения
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        print(f"Время выполнения функции {func.__name__}: {end_time - start_time:.4f} секунд")
        return result
    return wrapper

# Создаем главное окно
root = tk.Tk()
root.title("Симуляция светофора")

# Устанавливаем окно на полный экран
root.state('zoomed')
root.resizable(False, False)  # Запрещаем изменение размера окна

# Основная рамка для размещения всех элементов
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Создаем панель меню слева
menu_frame = tk.Frame(main_frame, bg="lightgrey", width=200)
menu_frame.pack(side="left", fill="y")

# Кнопки в меню
buttons = {
    "Настройки": None,
    "Начать симуляцию": None,
    "Приостановить": None,
    "Продолжить": None,
    "Закончить симуляцию": None,
    "Тестовый режим": None
}

# Функции для кнопок (пока пустые)
def start_simulation():
    print("Симуляция начата")

def pause_simulation():
    print("Симуляция приостановлена")

def resume_simulation():
    print("Симуляция продолжается")

def stop_simulation():
    print("Симуляция завершена")

def test_mode():
    print("Тестовый режим активирован")

# Создаем и размещаем кнопки
for i, (btn_text, func) in enumerate(buttons.items()):
    if btn_text == "Начать симуляцию":
        func = start_simulation
    elif btn_text == "Приостановить":
        func = pause_simulation
    elif btn_text == "Продолжить":
        func = resume_simulation
    elif btn_text == "Закончить симуляцию":
        func = stop_simulation
    elif btn_text == "Тестовый режим":
        func = test_mode

    buttons[btn_text] = tk.Button(menu_frame, text=btn_text, command=func, font=("Arial", 12), height=2, width=20)
    buttons[btn_text].pack(pady=5)

# Поле для симуляции
canvas = tk.Canvas(main_frame, bg="white")
canvas.pack(side="right", fill="both", expand=True)

# Создаем разметку дороги
def draw_road():
    # Ширина и высота окна
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Координаты дороги
    road_start_x = 0
    road_end_x = canvas_width
    road_y = canvas_height // 2

    # Высота дороги
    global road_height
    road_height = 350
    canvas.create_rectangle(road_start_x, road_y - road_height // 2, road_end_x, road_y + road_height // 2, fill="gray")

    # Белая разделительная разметка
    line_y = road_y
    canvas.create_line(road_start_x, line_y, road_end_x, line_y, fill="white", dash=(20, 10))

# Создаем разметку пешеходного перехода
def draw_crosswalk():
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    crosswalk_x = canvas_width // 2 - 130
    crosswalk_width = 280
    crosswalk_start_y = canvas_height // 2 - road_height // 2
    crosswalk_end_y = canvas_height // 2 + road_height // 2  # Нижняя граница дороги

    # Рисуем желто-белые полосы пешеходного перехода (вертикальные)
    y = crosswalk_start_y
    while y < crosswalk_end_y:
        canvas.create_rectangle(crosswalk_x, y, crosswalk_x + crosswalk_width, min(y + 30, crosswalk_end_y), fill="yellow")
        y += 30
        if y < crosswalk_end_y:
            canvas.create_rectangle(crosswalk_x, y, crosswalk_x + crosswalk_width, min(y + 30, crosswalk_end_y), fill="white")
            y += 30

    # Рисуем стоп-линии перед пешеходным переходом (слева и справа)
    stop_line_offset = 50
    left_stop_line_x = crosswalk_x - stop_line_offset
    right_stop_line_x = crosswalk_x + crosswalk_width + stop_line_offset

    canvas.create_line(left_stop_line_x, crosswalk_start_y, left_stop_line_x, crosswalk_end_y, fill="white", width=5)
    canvas.create_line(right_stop_line_x, crosswalk_start_y, right_stop_line_x, crosswalk_end_y, fill="white", width=5)


# Переменные для таймера
pedestrian_light_state = "red"  # Начальное состояние светофора для пешеходов
timer_value = 20  # Количество секунд до смены сигнала


def start_pedestrian_timer():
    global pedestrian_light_state, timer_value
    if pedestrian_light_state == "red":
        pedestrian_light_state = "green"
        timer_value = 20  # Устанавливаем таймер на 10 секунд
        update_pedestrian_light()  # Обновляем отображение светофора


def update_pedestrian_light():
    global timer_value, pedestrian_light_state
    canvas.delete("pedestrian_light")  # Удаляем старое состояние

    # Отрисовка светофора для пешеходов
    if pedestrian_light_state == "green":
        canvas.create_oval(pedestrian_light_x_left + 5, pedestrian_light_y + 5, pedestrian_light_x_left + 25,
                           pedestrian_light_y + 25,
                           fill="green", tags="pedestrian_light")
        timer_value -= 1
        if timer_value <= 0:
            pedestrian_light_state = "red"
            timer_value = 10
    else:
        canvas.create_oval(pedestrian_light_x_left + 5, pedestrian_light_y + 60, pedestrian_light_x_left + 25,
                           pedestrian_light_y + 80,
                           fill="red", tags="pedestrian_light")

    # Запускаем таймер через 1 секунду
    canvas.after(1000, update_pedestrian_light)


# Добавляем кнопку для пешеходного светофора
button_frame = tk.Frame(menu_frame)
button_frame.pack(pady=20)

pedestrian_button = tk.Button(button_frame, text="Переключить пешеходный свет", command=start_pedestrian_timer)
pedestrian_button.pack()


# Функция для отрисовки светофоров
def draw_traffic_lights():
    global pedestrian_light_x_left, pedestrian_light_y

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Высота размещения светофоров для водителей
    driver_light_y = canvas_height // 2 - 180
    line_y = canvas_height // 2

    # Светофоры для водителей (слева и справа)
    driver_light_x_left = canvas_width // 2 - 170
    driver_light_x_right = canvas_width // 2 + 160

    canvas.create_rectangle(driver_light_x_left, line_y - 45, driver_light_x_left + 30, line_y + 45, fill="black")
    canvas.create_rectangle(driver_light_x_right, line_y - 45, driver_light_x_right + 30, line_y + 45, fill="black")

    # Светофоры для пешеходов (слева и справа)
    pedestrian_light_x_left = canvas_width // 2 - 160
    pedestrian_light_y = canvas_height // 2 - 250
    pedestrian_light_x_right = canvas_width // 2 + 150
    pedestrian_light_y_bottom = canvas_height // 2 + 160

    canvas.create_rectangle(pedestrian_light_x_left, pedestrian_light_y, pedestrian_light_x_left + 30,
                            pedestrian_light_y + 90, fill="black")
    canvas.create_rectangle(pedestrian_light_x_right, pedestrian_light_y_bottom, pedestrian_light_x_right + 30,
                            pedestrian_light_y_bottom + 90, fill="black")

    update_pedestrian_light()  # Обновляем состояние светофоров для пешеходов

# Функция для обновления размеров при изменении размера окна
def update_canvas(event):
    canvas.delete("all")
    draw_road()
    draw_crosswalk()
    draw_traffic_lights()

# Привязываем функцию обновления к изменению размеров окна
canvas.bind("<Configure>", update_canvas)

# Запуск главного цикла программы
root.mainloop()
