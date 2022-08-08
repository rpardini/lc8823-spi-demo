LED_START = 0b11100000 # Three "1" bits, followed by 5 brightness bits
RGB_MAP = {'rgb': [3, 2, 1], 'rbg': [3, 1, 2], 'grb': [2, 3, 1],
           'gbr': [2, 1, 3], 'brg': [1, 3, 2], 'bgr': [1, 2, 3]}
NUM_LED = 122
UDP_IP = "0.0.0.0"
UDP_PORT = 1337