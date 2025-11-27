import numpy as np


def analyze_planet_fall(solution, body_radius):
    """
    Анализ результатов падения на планету
    """
    t = solution.t
    states = solution.y

    # Координаты и скорости
    x, y, z = states[0], states[1], states[2]
    vx, vy, vz = states[3], states[4], states[5]

    # Расстояние от центра планеты
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)

    # Высота над поверхностью
    altitude = r - body_radius

    # Скорость
    velocity = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2)

    # Угловое положение
    latitude = np.arcsin(z / r) * 180 / np.pi  # широта в градусах
    longitude = np.arctan2(y, x) * 180 / np.pi  # долгота в градусах

    analysis = {
        'time': t,
        'position': np.array([x, y, z]),
        'velocity': velocity,
        'altitude': altitude,
        'latitude': latitude,
        'longitude': longitude,
        'flight_time': t[-1],
        'max_velocity': np.max(velocity),
        'final_velocity': velocity[-1],
        'impact_coordinates': [latitude[-1], longitude[-1]]
    }

    return analysis


def calculate_orbit_velocity(body_radius, body_mass, altitude, G=6.67430e-11):
    """Вычисление орбитальной скорости для заданной высоты"""
    r = body_radius + altitude
    return np.sqrt(G * body_mass / r)


def optimize_trajectory_for_animation(trajectory, time, max_points=500):
    """
    Оптимизация траектории для анимации - уменьшение количества точек
    если траектория слишком длинная
    """
    if len(time) <= max_points:
        return trajectory, time

    # Выбираем точки с равными интервалами
    indices = np.linspace(0, len(time) - 1, max_points, dtype=int)

    optimized_trajectory = [
        trajectory[0][indices],
        trajectory[1][indices],
        trajectory[2][indices]
    ]
    optimized_time = time[indices]

    return optimized_trajectory, optimized_time