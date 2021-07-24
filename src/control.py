from yeelight import Bulb
from time import time, sleep

light = Bulb('192.168.1.104')


def police(light, min_bright=10, max_bright=100, steps=10, interval=.5):
    old_brightness = int(light.get_properties()['bright'])
    old_effect = light.effect
    light.effect = 'sudden'
    light.set_brightness(100)
    color = [(255,0,0), (0,0,255)]
    for i in range(2*steps):
        curr_color = color[i%len(color)]
        light.set_rgb(*curr_color)
        sleep(interval)
    
    light.effect = old_effect
    light.set_brightness(old_brightness)


police(light)



    