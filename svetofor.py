import tkinter as tk
from tkinter import simpledialog

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

# Функции для кнопок
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

def open_settings():
    global green_duration, red_duration
    green_duration = simpledialog.askinteger("Настройки", "Введите длительность зеленого сигнала (в секундах):", initialvalue=green_duration)
    red_duration = simpledialog.askinteger("Настройки", "Введите длительность красного сигнала (в секундах):", initialvalue=red_duration)

# Кнопки в меню
buttons = {
    "Начать симуляцию": start_simulation,
    "Приостановить": pause_simulation,
    "Продолжить": resume_simulation,
    "Закончить симуляцию": stop_simulation,
    "Настройки": open_settings,
}

# Создаем и размещаем кнопки
for btn_text, func in buttons.items():
    button = tk.Button(menu_frame, text=btn_text, command=func, font=("Arial", 12), height=2, width=20)
    button.pack(pady=5)

# Поле для симуляции
canvas = tk.Canvas(main_frame, bg="white")
canvas.pack(side="right", fill="both", expand=True)

# Создаем разметку дороги и перехода
def draw_road():
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    road_y = canvas_height // 2
    global road_height
    road_height = 350
    canvas.create_rectangle(0, road_y - road_height // 2, canvas_width, road_y + road_height // 2, fill="gray")
    canvas.create_line(0, road_y, canvas_width, road_y, fill="white", dash=(20, 10))

def draw_crosswalk():
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    crosswalk_x = canvas_width // 2 - 130
    crosswalk_width = 280
    crosswalk_start_y = canvas_height // 2 - road_height // 2
    crosswalk_end_y = canvas_height // 2 + road_height // 2

    y = crosswalk_start_y
    while y < crosswalk_end_y:
        canvas.create_rectangle(crosswalk_x, y, crosswalk_x + crosswalk_width, min(y + 30, crosswalk_end_y), fill="yellow")
        y += 30
        if y < crosswalk_end_y:
            canvas.create_rectangle(crosswalk_x, y, crosswalk_x + crosswalk_width, min(y + 30, crosswalk_end_y), fill="white")
            y += 30

    stop_line_offset = 50
    left_stop_line_x = crosswalk_x - stop_line_offset
    right_stop_line_x = crosswalk_x + crosswalk_width + stop_line_offset
    canvas.create_line(left_stop_line_x, crosswalk_start_y, left_stop_line_x, crosswalk_end_y, fill="white", width=5)
    canvas.create_line(right_stop_line_x, crosswalk_start_y, right_stop_line_x, crosswalk_end_y, fill="white", width=5)

# Переменные для таймера и состояния светофора
pedestrian_light_state = "red"
timer_value = 0
timer_text_id = None
waiting_for_green = False
timer_running = False
green_duration = 25
red_duration = 20

def start_pedestrian_timer():
    global pedestrian_light_state, timer_value, waiting_for_green, timer_running
    if pedestrian_light_state == "red" and not waiting_for_green and not timer_running:
        waiting_for_green = True
        timer_value = red_duration
        timer_running = True
        update_pedestrian_light()

def update_pedestrian_light():
    global timer_value, pedestrian_light_state, timer_text_id, waiting_for_green, timer_running
    canvas.delete("pedestrian_light")

    if pedestrian_light_state == "red":
        canvas.create_oval(pedestrian_light_x + 5, pedestrian_light_y + 5, pedestrian_light_x + 40,
                           pedestrian_light_y + 40, fill="red", tags="pedestrian_light")
        if waiting_for_green:
            timer_value -= 1
            if timer_value <= 0:
                pedestrian_light_state = "green"
                timer_value = green_duration
                canvas.delete("pedestrian_light")  # Удаляем красный сигнал
                canvas.create_oval(pedestrian_light_x + 115, pedestrian_light_y + 5, pedestrian_light_x + 150,
                                   pedestrian_light_y + 40, fill="green", tags="pedestrian_light")
    elif pedestrian_light_state == "green":
        canvas.create_oval(pedestrian_light_x + 115, pedestrian_light_y + 5, pedestrian_light_x + 150,
                           pedestrian_light_y + 40, fill="green", tags="pedestrian_light")
        timer_value -= 1
        if timer_value <= 0:
            pedestrian_light_state = "red"
            timer_value = 0
            waiting_for_green = False
            timer_running = False

    if timer_running or pedestrian_light_state == "green":
        color = "green" if pedestrian_light_state == "green" else "red"
        if timer_text_id is None:
            timer_text_id = canvas.create_text(pedestrian_light_x + 75, pedestrian_light_y + 25,
                                                text=str(timer_value), font=("Arial", 16), fill=color)
        else:
            canvas.itemconfigure(timer_text_id, text=str(timer_value), fill=color)
    else:
        if timer_text_id is not None:
            canvas.delete(timer_text_id)
            timer_text_id = None

    if timer_running or pedestrian_light_state == "green":
        canvas.after(1000, update_pedestrian_light)
    else:
        # Убедимся, что светофор снова загорается красным в конце цикла
        pedestrian_light_state = "red"
        canvas.create_oval(pedestrian_light_x + 5, pedestrian_light_y + 5, pedestrian_light_x + 40,
                           pedestrian_light_y + 40, fill="red", tags="pedestrian_light")
        canvas.create_oval(pedestrian_light_x + 115, pedestrian_light_y + 5, pedestrian_light_x + 150,
                           pedestrian_light_y + 40, fill="black", tags="pedestrian_light")
# Добавляем кнопку для пешеходного светофора
button_frame = tk.Frame(menu_frame)
button_frame.pack(pady=20)

pedestrian_button = tk.Button(button_frame, text="Переключить пешеходный свет", command=start_pedestrian_timer)
pedestrian_button.pack()

# Функция для отрисовки светофоров
def draw_traffic_lights():
    global pedestrian_light_x, pedestrian_light_y

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    driver_light_y = canvas_height // 2 - 180
    line_y = canvas_height // 2
    driver_light_x_left = canvas_width // 2 - 170
    driver_light_x_right = canvas_width // 2 + 160

    canvas.create_rectangle(driver_light_x_left, line_y - 45, driver_light_x_left + 30, line_y + 45, fill="black")
    canvas.create_rectangle(driver_light_x_right, line_y - 45, driver_light_x_right + 30, line_y + 45, fill="black")

    pedestrian_light_x = canvas_width // 2 - 60
    pedestrian_light_y = line_y - 30  # Размещаем горизонтальный светофор
    canvas.create_rectangle(pedestrian_light_x, pedestrian_light_y, pedestrian_light_x + 155, pedestrian_light_y + 45, fill="black")

    # Рисуем световые сигналы для пешеходов
    canvas.create_oval(pedestrian_light_x + 10, pedestrian_light_y + 10, pedestrian_light_x + 50, pedestrian_light_y + 40, fill="red", tags="pedestrian_light")
    canvas.create_oval(pedestrian_light_x + 70, pedestrian_light_y + 10, pedestrian_light_x + 110, pedestrian_light_y + 40, fill="black", tags="pedestrian_light")
    canvas.create_oval(pedestrian_light_x + 130, pedestrian_light_y + 10, pedestrian_light_x + 150, pedestrian_light_y + 40, fill="green", tags="pedestrian_light")

    update_pedestrian_light()  # Запускаем обновление состояния светофора

# Функция для обновления размеров при изменении размера окна
def update_canvas(event):
    canvas.delete("all")
    draw_road()
    draw_crosswalk()
    draw_traffic_lights()

# Привязываем функцию обновления к изменению размеров окна
canvas.bind("<Configure>", update_canvas)

# Рисуем все элементы
draw_road()
draw_crosswalk()
draw_traffic_lights()

# Функция для обновления размеров при изменении размера окна
def update_canvas(event):
    canvas.delete("all")
    draw_road()
    draw_crosswalk()
    draw_traffic_lights()

# Привязываем функцию обновления к изменению размеров окна
canvas.bind("<Configure>", update_canvas)

# Запускаем основной цикл приложения
root.mainloop()
