import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class FlightVisualizer:
    """
    Класс для визуализации траектории полёта тела
    """

    def __init__(self):
        self.fig = None
        self.ax = None

    def create_3d_plot(self):
        """Создание 3D графика"""
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.ax.set_xlabel('X (м)')
        self.ax.set_ylabel('Y (м)')
        self.ax.set_zlabel('Z (м)')
        self.ax.set_title('Траектория полёта тела в атмосфере')

        # Добавление сетки
        self.ax.grid(True)

    def plot_trajectory(self, trajectory, color='blue', label='Траектория'):
        """
        Построение траектории полёта

        Args:
            trajectory: массив координат [x, y, z]
            color: цвет линии
            label: метка для легенды
        """
        x, y, z = trajectory

        self.ax.plot(x, y, z, color=color, linewidth=2, label=label)

        # Отметка начальной точки
        self.ax.scatter(x[0], y[0], z[0], color='green', s=100, label='Старт', marker='o')

        # Отметка конечной точки
        self.ax.scatter(x[-1], y[-1], z[-1], color='red', s=100, label='Финиш', marker='x')

    def plot_without_drag(self, trajectory_no_drag, color='orange', label='Без сопротивления'):
        """
        Построение траектории без учёта сопротивления для сравнения
        """
        x, y, z = trajectory_no_drag
        self.ax.plot(x, y, z, color=color, linestyle='--', linewidth=1, label=label)

    def add_ground(self, max_range):
        """Добавление плоскости земли"""
        xx, yy = np.meshgrid(
            np.linspace(-max_range, max_range, 10),
            np.linspace(-max_range, max_range, 10)
        )
        zz = np.zeros_like(xx)

        self.ax.plot_surface(xx, yy, zz, alpha=0.3, color='brown')

    def show(self):
        """Отображение графика"""
        self.ax.legend()
        plt.tight_layout()
        plt.show()

    def save_animation_frames(self, trajectory, time, num_frames=50):
        """
        Создание кадров для анимации (опционально)
        """
        x, y, z = trajectory

        # Выбираем равномерно распределённые индексы для кадров
        indices = np.linspace(0, len(x) - 1, num_frames, dtype=int)

        frames = []
        for i in indices:
            self.create_3d_plot()
            self.ax.plot(x[:i + 1], y[:i + 1], z[:i + 1], color='blue', linewidth=2)
            self.ax.scatter(x[i], y[i], z[i], color='red', s=100)
            self.ax.set_title(f'Траектория полёта (t = {time[i]:.2f} с)')

            # Сохраняем кадр
            self.fig.canvas.draw()
            frame = np.array(self.fig.canvas.renderer.buffer_rgba())
            frames.append(frame)
            plt.close(self.fig)

        return frames