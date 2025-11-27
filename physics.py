import numpy as np
from scipy.integrate import solve_ivp


class BodyFlight:
    """
    Класс для моделирования полёта тела в атмосфере с учётом сопротивления
    """

    def __init__(self, mass=1.0, cross_area=0.01, drag_coef=0.47,
                 gravity=9.81, air_density=1.225):
        """
        Инициализация параметров тела и среды

        Args:
            mass: масса тела (кг)
            cross_area: площадь поперечного сечения (м²)
            drag_coef: коэффициент сопротивления
            gravity: ускорение свободного падения (м/с²)
            air_density: плотность воздуха (кг/м³)
        """
        self.mass = mass
        self.cross_area = cross_area
        self.drag_coef = drag_coef
        self.gravity = gravity
        self.air_density = air_density

    def drag_force(self, velocity):
        """
        Вычисление силы сопротивления воздуха

        Args:
            velocity: вектор скорости [vx, vy, vz] (м/с)

        Returns:
            Вектор силы сопротивления [Fx, Fy, Fz] (Н)
        """
        v = np.linalg.norm(velocity)
        if v == 0:
            return np.zeros(3)

        # Формула силы сопротивления: F = 0.5 * ρ * v² * Cd * A
        drag_magnitude = 0.5 * self.air_density * v ** 2 * self.drag_coef * self.cross_area
        drag_direction = -velocity / v  # Направление противоположно скорости

        return drag_magnitude * drag_direction

    def equations_of_motion(self, t, state):
        """
        Дифференциальные уравнения движения тела

        Args:
            t: время (с)
            state: вектор состояния [x, y, z, vx, vy, vz]

        Returns:
            Производные вектора состояния [vx, vy, vz, ax, ay, az]
        """
        x, y, z, vx, vy, vz = state
        velocity = np.array([vx, vy, vz])

        # Сила тяжести
        gravity_force = np.array([0, 0, -self.mass * self.gravity])

        # Сила сопротивления
        drag_force = self.drag_force(velocity)

        # Суммарная сила
        total_force = gravity_force + drag_force

        # Ускорение (второй закон Ньютона)
        acceleration = total_force / self.mass

        return [vx, vy, vz, acceleration[0], acceleration[1], acceleration[2]]

    def simulate(self, initial_position, initial_velocity, t_span, t_eval=None):
        """
        Моделирование полёта тела

        Args:
            initial_position: начальное положение [x, y, z] (м)
            initial_velocity: начальная скорость [vx, vy, vz] (м/с)
            t_span: интервал времени [t_start, t_end] (с)
            t_eval: массив времён для вывода результатов

        Returns:
            Результат решения solve_ivp
        """
        initial_state = np.concatenate([initial_position, initial_velocity])

        solution = solve_ivp(
            self.equations_of_motion,
            t_span,
            initial_state,
            t_eval=t_eval,
            method='RK45',
            rtol=1e-6,
            atol=1e-9
        )

        return solution