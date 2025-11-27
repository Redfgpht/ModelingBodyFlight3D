import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from physics_planet import PlanetFall
from visualization_planet import PlanetVisualizer
from utils import analyze_planet_fall, calculate_orbit_velocity
from celestial_bodies import CelestialBody


class PlanetFallGUI:
    """Графический интерфейс для симуляции падения на планеты Солнечной системы"""

    def __init__(self, root):
        self.root = root
        self.root.title("🌌 Симулятор падения на планеты")
        self.root.geometry("650x750")  # Уменьшил размер окна
        self.root.resizable(False, False)  # Запретил изменение размера

        # Переменные для хранения параметров
        self.body_var = tk.StringVar(value="earth")
        self.mass_var = tk.DoubleVar(value=1000.0)
        self.area_var = tk.DoubleVar(value=2.0)
        self.altitude_var = tk.DoubleVar(value=400000.0)
        self.velocity_type_var = tk.StringVar(value="orbital")
        self.custom_velocity_var = tk.DoubleVar(value=0.0)
        self.coriolis_var = tk.BooleanVar(value=True)
        self.animation_var = tk.BooleanVar(value=True)

        self.setup_ui()

    def setup_ui(self):
        """Настройка компактного пользовательского интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(main_frame,
                                text="🌌 Симулятор падения на планеты",
                                font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))

        # Фрейм для выбора планеты
        planet_frame = ttk.LabelFrame(main_frame, text="Выбор планеты", padding="8")
        planet_frame.pack(fill=tk.X, pady=5)

        # Сетка для кнопок планет (3x3)
        planets_grid = ttk.Frame(planet_frame)
        planets_grid.pack(fill=tk.X)

        planets = [
            ("Меркурий", "mercury", "○"),
            ("Венера", "venus", "♀"),
            ("Земля", "earth", "🌍"),
            ("Марс", "mars", "♂"),
            ("Юпитер", "jupiter", "♃"),
            ("Сатурн", "saturn", "♄"),
            ("Уран", "uranus", "♅"),
            ("Нептун", "neptune", "♆"),
            ("Плутон", "pluto", "⯓")
        ]

        # Создаём кнопки в сетке 3x3
        for i, (name, value, symbol) in enumerate(planets):
            row = i // 3
            col = i % 3

            btn = ttk.Radiobutton(planets_grid,
                                  text=f"{symbol} {name}",
                                  variable=self.body_var,
                                  value=value,
                                  command=self.on_planet_change)
            btn.grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)

        # Информация о выбранной планете (компактная)
        self.info_label = ttk.Label(planet_frame, text="", font=("Arial", 8), wraplength=600)
        self.info_label.pack(fill=tk.X, pady=5)

        # Основные параметры в одной строке
        params_frame = ttk.LabelFrame(main_frame, text="Основные параметры", padding="8")
        params_frame.pack(fill=tk.X, pady=5)

        # Сетка для параметров (2 колонки)
        params_grid = ttk.Frame(params_frame)
        params_grid.pack(fill=tk.X)

        # Масса
        ttk.Label(params_grid, text="Масса (кг):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        mass_scale = ttk.Scale(params_grid, from_=10, to=10000,
                               variable=self.mass_var, orient=tk.HORIZONTAL, length=150)
        mass_scale.grid(row=0, column=1, padx=5, pady=2)
        self.mass_label = ttk.Label(params_grid, text="1000 кг", width=8)
        self.mass_label.grid(row=0, column=2, padx=5, pady=2)

        # Площадь
        ttk.Label(params_grid, text="Площадь (м²):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        area_scale = ttk.Scale(params_grid, from_=0.1, to=10.0,
                               variable=self.area_var, orient=tk.HORIZONTAL, length=150)
        area_scale.grid(row=1, column=1, padx=5, pady=2)
        self.area_label = ttk.Label(params_grid, text="2.0 м²", width=8)
        self.area_label.grid(row=1, column=2, padx=5, pady=2)

        # Высота
        ttk.Label(params_grid, text="Высота (км):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.altitude_scale = ttk.Scale(params_grid, from_=100, to=1000000,
                                        variable=self.altitude_var, orient=tk.HORIZONTAL, length=150)
        self.altitude_scale.grid(row=2, column=1, padx=5, pady=2)
        self.altitude_label = ttk.Label(params_grid, text="400 км", width=8)
        self.altitude_label.grid(row=2, column=2, padx=5, pady=2)

        # Начальные условия
        init_frame = ttk.LabelFrame(main_frame, text="Начальные условия", padding="8")
        init_frame.pack(fill=tk.X, pady=5)

        # Скорость в компактном виде
        speed_frame = ttk.Frame(init_frame)
        speed_frame.pack(fill=tk.X, pady=2)

        ttk.Label(speed_frame, text="Скорость:").pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(speed_frame, text="Орбитальная",
                        variable=self.velocity_type_var, value="orbital").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(speed_frame, text="Нулевая",
                        variable=self.velocity_type_var, value="zero").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(speed_frame, text="Заданная",
                        variable=self.velocity_type_var, value="custom").pack(side=tk.LEFT, padx=5)

        # Пользовательская скорость
        custom_speed_frame = ttk.Frame(init_frame)
        custom_speed_frame.pack(fill=tk.X, pady=2)

        ttk.Label(custom_speed_frame, text="Скорость (м/с):").pack(side=tk.LEFT, padx=5)
        ttk.Entry(custom_speed_frame, textvariable=self.custom_velocity_var, width=10).pack(side=tk.LEFT, padx=5)

        # Дополнительные параметры в одной строке
        advanced_frame = ttk.LabelFrame(main_frame, text="Дополнительно", padding="8")
        advanced_frame.pack(fill=tk.X, pady=5)

        advanced_grid = ttk.Frame(advanced_frame)
        advanced_grid.pack(fill=tk.X)

        ttk.Checkbutton(advanced_grid, text="Сила Кориолиса",
                        variable=self.coriolis_var).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)

        ttk.Checkbutton(advanced_grid, text="Анимация",
                        variable=self.animation_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        # Кнопки управления - делаем основную кнопку большой и заметной
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # Большая заметная кнопка запуска
        self.simulate_btn = tk.Button(button_frame,
                                      text="🚀 СМОДЕЛИРОВАТЬ ПОЛЁТ",
                                      font=("Arial", 12, "bold"),
                                      bg="#4CAF50",  # Зелёный цвет
                                      fg="white",
                                      relief=tk.RAISED,
                                      bd=3,
                                      command=self.run_simulation,
                                      cursor="hand2")
        self.simulate_btn.pack(fill=tk.X, pady=5, ipady=8)

        # Второстепенные кнопки
        secondary_buttons = ttk.Frame(button_frame)
        secondary_buttons.pack(fill=tk.X)

        ttk.Button(secondary_buttons, text="🔄 Сбросить",
                   command=self.clear_all).pack(side=tk.LEFT, padx=5, pady=2)

        ttk.Button(secondary_buttons, text="📊 Инфо",
                   command=self.show_info).pack(side=tk.LEFT, padx=5, pady=2)

        ttk.Button(secondary_buttons, text="❌ Выход",
                   command=self.root.quit).pack(side=tk.RIGHT, padx=5, pady=2)

        # Информационная панель
        info_frame = ttk.LabelFrame(main_frame, text="Ход симуляции", padding="8")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.info_text = tk.Text(info_frame, height=8, font=("Courier", 8))
        scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)

        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Обновление меток
        self.mass_var.trace('w', self.update_mass_label)
        self.area_var.trace('w', self.update_area_label)
        self.altitude_var.trace('w', self.update_altitude_label)

        # Инициализация информации о планете
        self.on_planet_change()

        # Вывод начальной информации
        self.log_info("Добро пожаловать в симулятор падения на планеты!")
        self.log_info("Выберите планету и параметры, затем нажмите 'СМОДЕЛИРОВАТЬ ПОЛЁТ'")
        self.log_info("=" * 50)

    def on_planet_change(self):
        """Обновление информации при смене планеты"""
        body_name = self.body_var.get()
        body_params = CelestialBody.get_body_params(body_name)

        # Компактная информация о планете
        info = f"{body_name.upper()}: Радиус: {body_params['radius'] / 1000:.0f}км, Гравитация: {body_params['surface_gravity']:.1f}м/с², {body_params['description']}"
        self.info_label.config(text=info)

        # Обновляем диапазон высоты в зависимости от размера планеты
        max_altitude = body_params['radius'] * 10
        self.altitude_scale.config(to=max_altitude)
        self.altitude_var.set(min(self.altitude_var.get(), max_altitude))
        self.update_altitude_label()

    def update_mass_label(self, *args):
        """Обновление метки массы"""
        self.mass_label.config(text=f"{self.mass_var.get():.0f} кг")

    def update_area_label(self, *args):
        """Обновление метки площади"""
        self.area_label.config(text=f"{self.area_var.get():.1f} м²")

    def update_altitude_label(self, *args):
        """Обновление метки высоты"""
        altitude_km = self.altitude_var.get() / 1000
        self.altitude_label.config(text=f"{altitude_km:.0f} км")

    def log_info(self, message):
        """Добавление сообщения в информационную панель"""
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)
        self.info_text.update()

    def clear_info(self):
        """Очистка информационной панели"""
        self.info_text.delete(1.0, tk.END)

    def run_simulation(self):
        """Запуск симуляции с выбранными параметрами"""
        try:
            # Временно отключаем кнопку чтобы избежать двойного нажатия
            self.simulate_btn.config(state=tk.DISABLED, bg="#cccccc")
            self.root.update()

            self.clear_info()
            self.log_info("🔄 Запуск симуляции...")

            # Получение параметров из GUI
            body_name = self.body_var.get()
            mass = self.mass_var.get()
            cross_area = self.area_var.get()
            initial_altitude = self.altitude_var.get()
            enable_coriolis = self.coriolis_var.get()
            show_animation = self.animation_var.get()

            body_params = CelestialBody.get_body_params(body_name)

            # Вычисление начальной скорости
            if self.velocity_type_var.get() == "orbital":
                orbit_velocity = calculate_orbit_velocity(
                    body_params['radius'],
                    body_params['mass'],
                    initial_altitude
                )
                initial_velocity = [orbit_velocity, 0, 0]
                self.log_info(f"📊 Орбитальная скорость: {orbit_velocity:.1f} м/с")

            elif self.velocity_type_var.get() == "zero":
                initial_velocity = [0, 0, 0]
                self.log_info("📊 Начальная скорость: 0 м/с")

            else:  # custom
                custom_speed = self.custom_velocity_var.get()
                initial_velocity = [custom_speed, 0, 0]
                self.log_info(f"📊 Заданная скорость: {custom_speed:.1f} м/с")

            # Создание модели
            fall_model = PlanetFall(
                body_name=body_name,
                mass=mass,
                cross_area=cross_area,
                drag_coef=2.0 if body_params['atmosphere_height'] > 0 else 0,
                enable_coriolis=enable_coriolis and body_name == 'earth'
            )

            # Запуск симуляции
            self.log_info(f"🛰️  Начальная высота: {initial_altitude / 1000:.1f} км")
            self.log_info("⚡ Выполнение расчётов...")

            solution = fall_model.simulate_fall(
                initial_altitude=initial_altitude,
                initial_velocity=initial_velocity,
                max_time=3600
            )

            # Анализ результатов
            analysis = analyze_planet_fall(solution, body_params['radius'])
            impact_energy = fall_model.calculate_impact_energy(solution.y[3:6, -1])

            # Вывод результатов
            self.log_info("\n" + "=" * 50)
            self.log_info("📈 РЕЗУЛЬТАТЫ СИМУЛЯЦИИ")
            self.log_info("=" * 50)
            self.log_info(f"⏱️  Время падения: {analysis['flight_time']:.1f} с")
            self.log_info(f"📈 Максимальная скорость: {analysis['max_velocity']:.1f} м/с")
            self.log_info(f"💥 Скорость удара: {analysis['final_velocity']:.1f} м/с")
            self.log_info(f"⚡ Энергия удара: {impact_energy / 1e6:.1f} МДж")

            # Визуализация
            self.log_info("\n🎬 Создание визуализации...")

            title = f"Падение на {body_name.capitalize()}"

            visualizer = PlanetVisualizer(body_params)

            if show_animation:
                self.log_info("▶️  Запуск анимации...")
                visualizer.create_animation(
                    analysis['position'],
                    analysis['time'],
                    title
                )
            else:
                self.log_info("📊 Построение траектории...")
                visualizer.show_static_plot(analysis['position'], title)

            self.log_info("✅ Симуляция завершена успешно!")

        except Exception as e:
            error_msg = f"❌ Ошибка: {str(e)}"
            self.log_info(error_msg)
            messagebox.showerror("Ошибка", error_msg)
        finally:
            # Включаем кнопку обратно
            self.simulate_btn.config(state=tk.NORMAL, bg="#4CAF50")

    def clear_all(self):
        """Очистка всех полей"""
        self.mass_var.set(1000.0)
        self.area_var.set(2.0)
        self.altitude_var.set(400000.0)
        self.velocity_type_var.set("orbital")
        self.custom_velocity_var.set(0.0)
        self.coriolis_var.set(True)
        self.animation_var.set(True)
        self.clear_info()
        self.log_info("🔄 Параметры сброшены.")
        self.log_info("✅ Готов к новой симуляции!")

    def show_info(self):
        """Показать информацию о программе"""
        info_text = """
Симулятор падения на планеты Солнечной системы

Возможности:
• Моделирование падения на 9 планет
• Реалистичная физика с учётом гравитации
• Визуализация траектории в 3D
• Анимация процесса падения
• Расчёт энергии удара

Рекомендации:
• Используйте орбитальную скорость для реалистичности
• Начинайте с высоты 100-1000 км
• Экспериментируйте с разными планетами!
        """
        messagebox.showinfo("О программе", info_text)


def main():
    """Запуск GUI приложения"""
    root = tk.Tk()
    app = PlanetFallGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()