import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


class PlanetVisualizer:
    """
    Класс для визуализации падения тела на планету
    """

    def __init__(self, body_params):
        self.body_params = body_params
        self.fig = None
        self.ax = None

    def create_planet_plot(self):
        """Создание 3D визуализации планеты"""
        self.fig = plt.figure(figsize=(14, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Рисуем планету как простую сферу
        self._draw_simple_planet()

        self.ax.set_xlabel('X (м)')
        self.ax.set_ylabel('Y (м)')
        self.ax.set_zlabel('Z (м)')

        # Устанавливаем равные масштабы осей
        max_range = self.body_params['radius'] * 1.5
        self.ax.set_xlim([-max_range, max_range])
        self.ax.set_ylim([-max_range, max_range])
        self.ax.set_zlim([-max_range, max_range])

        self.ax.grid(True, alpha=0.3)
        return self.fig, self.ax

    def _draw_simple_planet(self):
        """Рисование простой сферы без текстуры"""
        radius = self.body_params['radius']

        # Создаём сферу
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 25)
        u, v = np.meshgrid(u, v)

        x = radius * np.sin(v) * np.cos(u)
        y = radius * np.sin(v) * np.sin(u)
        z = radius * np.cos(v)

        # Рисуем одноцветную сферу
        self.ax.plot_surface(x, y, z,
                             color=self.body_params['color'],
                             alpha=0.8,
                             shade=True,
                             antialiased=True)

    def create_animation(self, trajectory, time, title="Анимация падения тела"):
        """Создание анимации падения в реальном времени"""
        fig, ax = self.create_planet_plot()
        ax.set_title(title, fontsize=14, fontweight='bold')

        # Подготовка элементов анимации
        trajectory_line, = ax.plot([], [], [], 'r-', linewidth=3, alpha=0.8, label='Траектория')
        current_point, = ax.plot([], [], [], 'ro', markersize=8, label='Текущее положение')
        start_point, = ax.plot([], [], [], 'go', markersize=10, label='Старт')
        impact_point, = ax.plot([], [], [], 'rx', markersize=12, label='Удар')

        # Отображаем начальную точку сразу
        start_point.set_data([trajectory[0][0]], [trajectory[1][0]])
        start_point.set_3d_properties([trajectory[2][0]])

        # Отображаем конечную точку сразу
        impact_point.set_data([trajectory[0][-1]], [trajectory[1][-1]])
        impact_point.set_3d_properties([trajectory[2][-1]])

        def animate(frame):
            # Показываем траекторию до текущего кадра
            idx = min(frame, len(trajectory[0]) - 1)

            trajectory_line.set_data(trajectory[0][:idx], trajectory[1][:idx])
            trajectory_line.set_3d_properties(trajectory[2][:idx])

            current_point.set_data([trajectory[0][idx]], [trajectory[1][idx]])
            current_point.set_3d_properties([trajectory[2][idx]])

            # Вычисляем текущую высоту
            current_pos = np.array([trajectory[0][idx], trajectory[1][idx], trajectory[2][idx]])
            current_altitude = np.linalg.norm(current_pos) - self.body_params['radius']

            ax.set_title(f'{title}\nВремя: {time[idx]:.1f} с, Высота: {current_altitude:.0f} м',
                         fontsize=12)

            return trajectory_line, current_point, start_point, impact_point

        # Создаём анимацию
        frames = len(trajectory[0])
        interval = max(10, min(50, 3000 // frames))  # Автоматический расчет интервала

        anim = animation.FuncAnimation(
            fig, animate, frames=frames,
            interval=interval, blit=False, repeat=True
        )

        ax.legend()
        plt.tight_layout()
        plt.show()

        return anim

    def show_static_plot(self, trajectory, title="Траектория падения тела"):
        """Показать статический график траектории"""
        fig, ax = self.create_planet_plot()
        ax.set_title(title, fontsize=14, fontweight='bold')

        # Рисуем полную траекторию
        x, y, z = trajectory
        ax.plot(x, y, z, 'r-', linewidth=3, alpha=0.8, label='Траектория')
        ax.plot(x[0], y[0], z[0], 'go', markersize=10, label='Старт')
        ax.plot(x[-1], y[-1], z[-1], 'rx', markersize=12, label='Удар')

        ax.legend()
        plt.tight_layout()
        plt.show()

    def close(self):
        """Закрыть график"""
        if self.fig:
            plt.close(self.fig)