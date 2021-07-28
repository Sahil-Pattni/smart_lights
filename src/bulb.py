from binancebot.bots import BinanceBot, BinanceException
from yeelight import Bulb
from time import sleep
from bulb import *
import os

env = os.environ

bot = BinanceBot(env.get('BINANCE_KEY'), env.get('BINANCE_SECRET'))
STATUS = False

def get_rgb(light):
    """
    Converts an unsigned int value returned by the
    bulb to red, blue and green values.

    Calls: 1

    Args:
        light (`yeelight.Bulb`): The Yeelight device.
    
    Returns:
        (`tuple`): A tuple containing the red, blue and green values.
    """
    rgb_unsigned = int(light.get_properties()['rgb'])
    red = (rgb_unsigned >> 16) & 0xFF
    blue = (rgb_unsigned >> 8) & 0XFF
    green = (rgb_unsigned & 0XFF)

    return (red, blue, green)


async def police(light, delay=.1):
    """
    Flashes red and blue for a given number of steps.

    Calls: 6 static + (60/delay) per minute.

    Args:
        light (`yeelight.Bulb`): The Yeelight device.
        steps (`int`): The number of flashes (One flash is red and blue alternating).
        delay (`float`): The delay in seconds between the red and blue alternating.
    
    Returns:
        None
    """
    old_brightness = int(light.get_properties()['bright'])
    old_effect = light.effect
    light.effect = 'sudden'
    light.set_brightness(100)
    color = [(255,0,0), (0,0,255)]
    i = 0
    while STATUS:
        i += 1
        curr_color = color[i%len(color)]
        light.set_rgb(*curr_color)
        sleep(delay)
    
    light.effect = old_effect
    light.set_brightness(old_brightness)



