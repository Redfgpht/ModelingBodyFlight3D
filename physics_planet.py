import numpy as np
from scipy.integrate import solve_ivp


class PlanetFall:
    """
    Класс для моделирования падения тела на планету с учётом:
    - Гравитации, зависящей от высоты
    - Кривизны планеты
    - Атмосферного сопротивления
    - Вращения планеты (опционально)
    """

    def __init__(self, body_name='earth', drag_coef=0.47, cross_area=1.0, mass=1000,
                 enable_coriolis=False, planet_rotation_rate=7.2921159e-5):
        """
        Инициализация параметров

        Args:
            body_name: название небесного тела
            drag_coef: коэффициент аэродинамического сопротивления
            cross_area: площадь поперечного сечения (м²)
            mass: масса тела (кг)
            enable_coriolis: учитывать силу Кориолиса
            planet_rotation_rate: угловая скорость вращения планеты (рад/с)
        """
        from celestial_bodies import CelestialBody

        self.body_params = CelestialBody.get_body_params(body_name)
        self.drag_coef = drag_coef
        self.cross_area = cross_area
        self.mass = mass
        self.enable_coriolis = enable_coriolis
        self.planet_rotation_rate = planet_rotation_rate

        # Гравитационная постоянная
        self.G = 6.67430e-11

        print(f"Инициализирована модель для: {body_name}")
        print(f"Радиус: {self.body_params['radius'] / 1000:.0f} км")
        print(f"Поверхностная гравитация: {self.body_params['surface_gravity']:.2f} м/с²")

    def atmospheric_density(self, height):
        """
        Модель плотности атмосферы в зависимости от высоты
        """
        if height > self.body_params['atmosphere_height']:
            return 0.0

        # Плотность на поверхности зависит от планеты
        if self.body_params['color'] == 'earth':
            surface_density = 1.225
        elif self.body_params['color'] == 'venus':
            surface_density = 65.0  # Очень плотная атмосфера
        elif self.body_params['color'] == 'mars':
            surface_density = 0.020
        else:
            surface_density = 0.0

        # Масштаб высоты
        scale_height = self.body_params['atmosphere_height'] / 8

        return surface_density * np.exp(-height / scale_height)

    def gravity_at_height(self, position):
        """
        Вычисление гравитации на заданной высоте

        Args:
            position: вектор положения [x, y, z] в метрах

        Returns:
            Вектор ускорения свободного падения [gx, gy, gz]
        """
        r = np.linalg.norm(position)
        if r == 0:
            return np.zeros(3)

        # Закон всемирного тяготения: g = -G * M / r² * (r_vector / r)
        g_magnitude = self.G * self.body_params['mass'] / r ** 2
        g_direction = -position / r

        return g_magnitude * g_direction

    def atmospheric_density(self, height):
        """
        Модель плотности атмосферы в зависимости от высоты
        Упрощённая экспоненциальная модель
        """
        if height > self.body_params['atmosphere_height']:
            return 0.0

        # Плотность на поверхности (кг/м³)
        if self.body_params['color'] == 'earth':
            surface_density = 1.225
        elif self.body_params['color'] == 'mars':
            surface_density = 0.020
        else:
            surface_density = 0.0

        # Масштаб высоты (м)
        scale_height = self.body_params['atmosphere_height'] / 8

        return surface_density * np.exp(-height / scale_height)

    def drag_force(self, position, velocity):
        """
        Сила аэродинамического сопротивления

        Args:
            position: вектор положения
            velocity: вектор скорости относительно атмосферы
        """
        height = np.linalg.norm(position) - self.body_params['radius']
        if height < 0:
            return np.zeros(3)

        density = self.atmospheric_density(height)
        if density == 0:
            return np.zeros(3)

        v = np.linalg.norm(velocity)
        if v == 0:
            return np.zeros(3)

        # Формула сопротивления: F = 0.5 * ρ * v² * Cd * A
        drag_magnitude = 0.5 * density * v ** 2 * self.drag_coef * self.cross_area
        drag_direction = -velocity / v

        return drag_magnitude * drag_direction

    def coriolis_force(self, position, velocity):
        """
        Сила Кориолиса (для вращающейся планеты)
        """
        if not self.enable_coriolis:
            return np.zeros(3)

        # Вектор угловой скорости (направлен вдоль оси Z)
        omega = np.array([0, 0, self.planet_rotation_rate])

        # Сила Кориолиса: F = -2m * (ω × v)
        coriolis_acceleration = -2 * np.cross(omega, velocity)
        return self.mass * coriolis_acceleration

    def equations_of_motion(self, t, state):
        """
        Дифференциальные уравнения движения в гравитационном поле планеты

        Args:
            state: [x, y, z, vx, vy, vz]
        """
        x, y, z, vx, vy, vz = state
        position = np.array([x, y, z])
        velocity = np.array([vx, vy, vz])

        # Гравитация
        gravity_acceleration = self.gravity_at_height(position)

        # Сопротивление атмосферы
        drag_acceleration = self.drag_force(position, velocity) / self.mass

        # Сила Кориолиса
        coriolis_acceleration = self.coriolis_force(position, velocity) / self.mass

        # Суммарное ускорение
        total_acceleration = gravity_acceleration + drag_acceleration + coriolis_acceleration

        return [vx, vy, vz,
                total_acceleration[0],
                total_acceleration[1],
                total_acceleration[2]]

    def simulate_fall(self, initial_altitude, initial_velocity=None,
                      t_span=None, max_time=3600):
        """
        Моделирование падения на планету

        Args:
            initial_altitude: начальная высота над поверхностью (м)
            initial_velocity: начальная скорость [vx, vy, vz] (м/с)
            t_span: временной интервал
            max_time: максимальное время симуляции (с)
        """
        if initial_velocity is None:
            initial_velocity = [0, 0, 0]

        # Начальное положение (на заданной высоте над поверхностью)
        initial_position = np.array([0, 0, self.body_params['radius'] + initial_altitude])

        # Начальное состояние
        initial_state = np.concatenate([initial_position, initial_velocity])

        # Временной интервал
        if t_span is None:
            t_span = [0, max_time]

        # Событие для остановки при достижении поверхности
        def surface_event(t, state):
            r = np.linalg.norm(state[0:3])
            return r - self.body_params['radius']

        surface_event.terminal = True
        surface_event.direction = -1

        print(f"Начальная высота: {initial_altitude / 1000:.1f} км")
        print(f"Начальная скорость: {np.linalg.norm(initial_velocity):.1f} м/с")

        # Решение дифференциальных уравнений
        solution = solve_ivp(
            self.equations_of_motion,
            t_span,
            initial_state,
            events=[surface_event],
            method='RK45',
            rtol=1e-8,
            atol=1e-10,
            max_step=10
        )

        return solution

    def calculate_impact_energy(self, final_velocity):
        """Вычисление энергии удара о поверхность"""
        kinetic_energy = 0.5 * self.mass * np.linalg.norm(final_velocity) ** 2
        return kinetic_energy