from threading import Thread
from flask import request, abort, Flask
from bulb import *


app = Flask(__name__)
app.config["DEBUG"] = True

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

@app.route('/stonks', methods=['POST'])
def stonks():
    global STATUS
    if not request.json: # Just in case
        abort(400)
    
    STATUS = not STATUS
    args = dict(request.json)
    thread = Thread(target=live_market_signals, args=args.values())
    thread.start()
    return f'{STATUS}', 201
    
    
if __name__ == '__main__':
    app.run()