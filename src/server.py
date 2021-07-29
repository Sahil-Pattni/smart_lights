from threading import Thread
from flask import request, abort, Flask
from yeelight import Bulb, Flow, transitions
from binancebot.bots import BinanceBot, BinanceException
import os
from time import sleep

env = os.environ
bot = BinanceBot(env.get('BINANCE_KEY'), env.get('BINANCE_SECRET'))
app = Flask(__name__)
app.config["DEBUG"] = True
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


def live_market_signals(ticker, light, delay=5):
    print('Starting...')
    light = Bulb(light)
    price = bot.price(ticker)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    sleep(delay)
    count = 1
    while STATUS:
        print(f'Loop {count}')
        count += 1
        current_price = bot.price(ticker)
        if current_price < price:
            light.set_rgb(*red)
        elif current_price > price:
            light.set_rgb(*green)
        else:
            light.set_rgb(*blue)
        sleep(delay)



def pre_check(request):
    if not request.json:
        abort(400)


def flow_control(flow, args):
    global STATUS
    STATUS = not STATUS
    light = Bulb(args['light'])
    if STATUS:
        flow = Flow(transitions=flow)
        light.start_flow(flow)
    else:
        light.stop_flow()


@app.route('/stonks', methods=['POST'])
def stonks():
    pre_check(request)
    global STATUS
    STATUS = not STATUS
    args = dict(request.json)
    thread = Thread(target=live_market_signals, args=args.values())
    thread.start()
    return f'{STATUS}', 201


@app.route('/police', methods=['POST'])
def police():
    pre_check(request )
    args = dict(request.json)
    flow_control(transitions.police2, args)


@app.route('/strobe', methods=['POST'])
def police():
    pre_check(request )
    args = dict(request.json)
    flow_control(transitions.strobe, args)    

    
    
if __name__ == '__main__':
    app.run()