import numpy as np


class CelestialBody:
    """Класс для хранения параметров планет Солнечной системы"""

    BODIES = {
        'mercury': {
            'radius': 2439700,  # м
            'mass': 3.301e23,  # кг
            'surface_gravity': 3.7,  # м/с²
            'atmosphere_height': 0,  # м (почти нет атмосферы)
            'color': 'gray',
            'orbital_period': 88,  # дней
            'description': 'Ближайшая к Солнцу планета'
        },
        'venus': {
            'radius': 6051800,  # м
            'mass': 4.867e24,  # кг
            'surface_gravity': 8.87,  # м/с²
            'atmosphere_height': 250000,  # м
            'color': 'orange',
            'orbital_period': 225,
            'description': 'Планета с плотной атмосферой'
        },
        'earth': {
            'radius': 6371000,  # м
            'mass': 5.972e24,  # кг
            'surface_gravity': 9.81,  # м/с²
            'atmosphere_height': 100000,  # м
            'color': 'blue',
            'orbital_period': 365,
            'description': 'Наша родная планета'
        },
        'mars': {
            'radius': 3389500,  # м
            'mass': 6.39e23,  # кг
            'surface_gravity': 3.71,  # м/с²
            'atmosphere_height': 11000,  # м
            'color': 'red',
            'orbital_period': 687,
            'description': 'Красная планета'
        },
        'jupiter': {
            'radius': 69911000,  # м
            'mass': 1.898e27,  # кг
            'surface_gravity': 24.79,  # м/с²
            'atmosphere_height': 500000,  # м
            'color': 'brown',
            'orbital_period': 4333,
            'description': 'Крупнейшая планета'
        },
        'saturn': {
            'radius': 58232000,  # м
            'mass': 5.683e26,  # кг
            'surface_gravity': 10.44,  # м/с²
            'atmosphere_height': 400000,  # м
            'color': 'gold',
            'orbital_period': 10759,
            'description': 'Планета с кольцами'
        },
        'uranus': {
            'radius': 25362000,  # м
            'mass': 8.681e25,  # кг
            'surface_gravity': 8.69,  # м/с²
            'atmosphere_height': 300000,  # м
            'color': 'lightblue',
            'orbital_period': 30687,
            'description': 'Ледяной гигант'
        },
        'neptune': {
            'radius': 24622000,  # м
            'mass': 1.024e26,  # кг
            'surface_gravity': 11.15,  # м/с²
            'atmosphere_height': 350000,  # м
            'color': 'darkblue',
            'orbital_period': 60190,
            'description': 'Ветреная планета'
        },
        'pluto': {
            'radius': 1188300,  # м
            'mass': 1.309e22,  # кг
            'surface_gravity': 0.62,  # м/с²
            'atmosphere_height': 0,  # м
            'color': 'darkgray',
            'orbital_period': 90560,
            'description': 'Карликовая планета'
        }
    }

    @classmethod
    def get_body_params(cls, body_name):
        """Получить параметры небесного тела"""
        return cls.BODIES.get(body_name.lower(), cls.BODIES['earth'])

    @classmethod
    def list_available_bodies(cls):
        """Список доступных небесных тел"""
        return list(cls.BODIES.keys())

    @classmethod
    def get_body_info(cls, body_name):
        """Получить информацию о планете"""
        params = cls.get_body_params(body_name)
        info = f"""
{body_name.upper()}:
- Радиус: {params['radius'] / 1000:.0f} км
- Масса: {params['mass']:.2e} кг
- Гравитация: {params['surface_gravity']:.1f} м/с²
- Атмосфера: {'Есть' if params['atmosphere_height'] > 0 else 'Нет'}
- Орбитальный период: {params['orbital_period']} дней
- Описание: {params['description']}
"""
        return info