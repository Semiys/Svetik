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
    road_height = 350
    canvas.create_rectangle(road_start_x, road_y - road_height // 2, road_end_x, road_y + road_height // 2, fill="gray")

    # Белая разделительная разметка
    line_y = road_y
    canvas.create_line(road_start_x, line_y, road_end_x, line_y, fill="white", dash=(20, 10))


# Создаем разметку пешеходного перехода
def draw_crosswalk():
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    crosswalk_y = canvas_height // 2
    crosswalk_height = 300
    crosswalk_start_x = canvas_width // 2 - 130
    crosswalk_end_x = canvas_width // 2 + 150

    # Рисуем желто-белые полосы пешеходного перехода (вертикальные)
    for i in range(crosswalk_y - crosswalk_height // 2, crosswalk_y + crosswalk_height // 2, 40):
        canvas.create_rectangle(crosswalk_start_x, i, crosswalk_end_x, i + 30, fill="yellow")
        canvas.create_rectangle(crosswalk_start_x, i + 30, crosswalk_end_x, i + 60, fill="white")

    # Рисуем стоп-линию перед пешеходным переходом
    stop_line_offset = 50
    canvas.create_line(crosswalk_start_x - stop_line_offset, crosswalk_y - road_height // 2,
                       crosswalk_start_x - stop_line_offset, crosswalk_y + road_height // 2,
                       fill="white", width=5)


# Рисуем светофоры
def draw_traffic_lights():
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Светофоры для пешеходов
    pedestrian_light_x_left = canvas_width // 2 - 200
    pedestrian_light_y = canvas_height // 2 - 250
    pedestrian_light_x_right = canvas_width // 2 + 150
    pedestrian_light_y_bottom = canvas_height // 2 + 160

    # Верхний и нижний светофоры для пешеходов
    canvas.create_rectangle(pedestrian_light_x_left, pedestrian_light_y, pedestrian_light_x_left + 30,
                            pedestrian_light_y + 90, fill="black")
    canvas.create_rectangle(pedestrian_light_x_right, pedestrian_light_y_bottom, pedestrian_light_x_right + 30,
                            pedestrian_light_y_bottom + 90, fill="black")

    # Светофоры для водителей слева и справа от пешеходного перехода
    driver_light_x_left = canvas_width // 2 - 180
    driver_light_x_right = canvas_width // 2 + 150
    driver_light_y = canvas_height // 2 - 180

    canvas.create_rectangle(driver_light_x_left, driver_light_y, driver_light_x_left + 30, driver_light_y + 90,
                            fill="black")
    canvas.create_rectangle(driver_light_x_right, driver_light_y, driver_light_x_right + 30, driver_light_y + 90,
                            fill="black")


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





