from yeelight import Bulb, Flow, transitions
from server import get_rgb
from time import sleep
import math

BASE = '192.168.1.10'
CT = 3089
RGB = 16711680

lights = [4,9]


def convert_rgb(rgb_unsigned):
    red = (rgb_unsigned >> 16) & 0xFF
    blue = (rgb_unsigned >> 8) & 0XFF
    green = (rgb_unsigned & 0XFF)

    return (red, blue, green)


def color_temp_to_rgb(temp):
    temp /= 100
    red, green, blue = 0,0,0

    if temp <= 66:
        red = 255
        green = 99.4708025861 * math.log(temp) - 161.1195681661
    else:
        red = 329.698727446 * ((temp-60) ^ -0.1332047592)
        green = 288.1221695283 * ((temp-60) ^ -0.0755148492)
    
    # Blue
    if temp >= 66:
        blue = 255
    else:
        if temp <= 19:
            blue = 0
        else:
            blue = 138.5177312231 * math.log(temp-10) - 305.0447927307

    rgb = [red, green, blue]

    for i in range(3):
        if rgb[i] < 0:
            rgb[i] = 0
        elif rgb[i] > 255:
            rgb[i] = 255
    
    return tuple(rgb)



def set_scene(scene):
    for k, v in scene.items():
        bulb = Bulb(f'{BASE}{k}', effect="smooth", duration=2000)
        keys = v.keys()
        if 'rgb' in keys:
            bulb.set_rgb(*v['rgb'])
        if 'ct' in keys:
            bulb.set_color_temp(v['ct'])
        if 'bright' in keys:
            bulb.set_brightness(v['brightness'])


# --- SCENES --- #
police = {
    4: {'rgb' (255,0,0)},
    7: {'rgb': (0,0,255)},
    9: {'rgb': (255,0,0)}
}

cozy = {
    4: {'ct': 3200, 'bright': 2},
    9: {'ct': 3200, 'bright': 2},
    7: {'ct': color_temp_to_rgb(3200), 'bright': 2},
}

