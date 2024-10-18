import tkinter as tk
from tkinter import simpledialog, messagebox
import time

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

# Переменные для таймера и состояния светофора
pedestrian_light_state = "red"
timer_value = 0
timer_text_id = None
waiting_for_green = False
timer_running = False
green_duration = 25
red_duration = 20
simulation_started = False
last_update_time = 0


# Функции для кнопок
def start_simulation():
    global timer_running, simulation_started, last_update_time
    if simulation_started:
        messagebox.showinfo("Внимание", "Для перезапуска симуляции необходимо сначала закончить текущую и начать новую")
        return
    timer_running = True
    simulation_started = True
    last_update_time = time.time()
    update_pedestrian_light()
    print("Симуляция начата")


def pause_simulation():
    global timer_running
    if not simulation_started:
        messagebox.showinfo("Внимание", "Необходимо начать симуляцию")
        return
    timer_running = False
    print("Симуляция приостановлена")


def resume_simulation():
    global timer_running, last_update_time
    if not simulation_started:
        messagebox.showinfo("Внимание", "Необходимо начать симуляцию")
        return
    timer_running = True
    last_update_time = time.time()
    update_pedestrian_light()
    print("Симуляция продолжается")


def stop_simulation():
    global timer_running, pedestrian_light_state, timer_value, waiting_for_green, simulation_started
    timer_running = False
    simulation_started = False
    pedestrian_light_state = "red"
    timer_value = 0
    waiting_for_green = False
    update_pedestrian_light()
    print("Симуляция завершена")


def open_settings():
    global green_duration, red_duration
    settings_window = tk.Toplevel(root)
    settings_window.title("Настройки")

    tk.Label(settings_window, text="Длительность зеленого сигнала (в секундах):").grid(row=0, column=0, padx=5, pady=5)
    green_entry = tk.Entry(settings_window)
    green_entry.insert(0, str(green_duration))
    green_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(settings_window, text="Длительность красного сигнала (в секундах):").grid(row=1, column=0, padx=5, pady=5)
    red_entry = tk.Entry(settings_window)
    red_entry.insert(0, str(red_duration))
    red_entry.grid(row=1, column=1, padx=5, pady=5)

    def save_settings():
        global green_duration, red_duration
        green_duration = int(green_entry.get())
        red_duration = int(red_entry.get())
        settings_window.destroy()

    tk.Button(settings_window, text="Сохранить", command=save_settings).grid(row=2, column=0, columnspan=2, pady=10)


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
        canvas.create_rectangle(crosswalk_x, y, crosswalk_x + crosswalk_width, min(y + 30, crosswalk_end_y),
                                fill="yellow")
        y += 30
        if y < crosswalk_end_y:
            canvas.create_rectangle(crosswalk_x, y, crosswalk_x + crosswalk_width, min(y + 30, crosswalk_end_y),
                                    fill="white")
            y += 30

    stop_line_offset = 50
    left_stop_line_x = crosswalk_x - stop_line_offset
    right_stop_line_x = crosswalk_x + crosswalk_width + stop_line_offset
    canvas.create_line(left_stop_line_x, crosswalk_start_y, left_stop_line_x, crosswalk_end_y, fill="white", width=5)
    canvas.create_line(right_stop_line_x, crosswalk_start_y, right_stop_line_x, crosswalk_end_y, fill="white", width=5)


def start_pedestrian_timer():
    global pedestrian_light_state, timer_value, waiting_for_green, timer_running
    if not simulation_started:
        messagebox.showinfo("Внимание", "Необходимо начать симуляцию")
        return
    if not timer_running:
        messagebox.showinfo("Внимание", "Необходимо продолжить симуляцию или начать заново")
        return
    if pedestrian_light_state == "red" and not waiting_for_green and timer_running:
        waiting_for_green = True
        timer_value = red_duration
        update_pedestrian_light()


def update_pedestrian_light():
    global timer_value, pedestrian_light_state, timer_text_id, waiting_for_green, timer_running, last_update_time
    canvas.delete("pedestrian_light")

    current_time = time.time()
    elapsed_time = current_time - last_update_time
    last_update_time = current_time

    if pedestrian_light_state == "red":
        canvas.create_oval(pedestrian_light_x + 5, pedestrian_light_y + 5, pedestrian_light_x + 40,
                           pedestrian_light_y + 40, fill="red", tags="pedestrian_light")
        if waiting_for_green and timer_running:
            timer_value -= elapsed_time
            if timer_value <= 0:
                pedestrian_light_state = "green"
                timer_value = green_duration
                canvas.delete("pedestrian_light")  # Удаляем красный сигнал
                canvas.create_oval(pedestrian_light_x + 115, pedestrian_light_y + 5, pedestrian_light_x + 150,
                                   pedestrian_light_y + 40, fill="green", tags="pedestrian_light")
    elif pedestrian_light_state == "green":
        canvas.create_oval(pedestrian_light_x + 115, pedestrian_light_y + 5, pedestrian_light_x + 150,
                           pedestrian_light_y + 40, fill="green", tags="pedestrian_light")
        if timer_running:
            timer_value -= elapsed_time
            if timer_value <= 0:
                pedestrian_light_state = "red"
                timer_value = 0
                waiting_for_green = False

    if timer_running or pedestrian_light_state == "green":
        color = "green" if pedestrian_light_state == "green" else "red"
        if timer_text_id is None:
            timer_text_id = canvas.create_text(pedestrian_light_x + 75, pedestrian_light_y + 25,
                                               text=f"{timer_value:.1f}", font=("Arial", 16), fill=color)
        else:
            canvas.itemconfigure(timer_text_id, text=f"{timer_value:.1f}", fill=color)
    else:
        if timer_text_id is not None:
            canvas.itemconfigure(timer_text_id, text=f"{timer_value:.1f}")

    if timer_running:
        canvas.after(100, update_pedestrian_light)
    else:
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
    canvas.create_rectangle(pedestrian_light_x, pedestrian_light_y, pedestrian_light_x + 155, pedestrian_light_y + 45,
                            fill="black")

    # Рисуем световые сигналы для пешеходов
    canvas.create_oval(pedestrian_light_x + 10, pedestrian_light_y + 10, pedestrian_light_x + 50,
                       pedestrian_light_y + 40, fill="red", tags="pedestrian_light")
    canvas.create_oval(pedestrian_light_x + 70, pedestrian_light_y + 10, pedestrian_light_x + 110,
                       pedestrian_light_y + 40, fill="black", tags="pedestrian_light")
    canvas.create_oval(pedestrian_light_x + 130, pedestrian_light_y + 10, pedestrian_light_x + 150,
                       pedestrian_light_y + 40, fill="green", tags="pedestrian_light")

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
