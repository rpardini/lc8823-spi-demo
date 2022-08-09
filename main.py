# main.py
import asyncio
from typing import Union

import sys
import led_driver
import light_goggles
import socket
from constants import NUM_LED, UDP_IP, UDP_PORT, r, SPI_BUS, SPI_DEVICE, SPI_SPEED_HZ, BRIGHTNESS
import goggle_light_show_templates
from fastapi import FastAPI

#Initialize Strip
strip = led_driver.APA102(num_led=NUM_LED, 
                            global_brightness=BRIGHTNESS, 
                            SPI_BUS=SPI_BUS, 
                            SPI_DEVICE=SPI_DEVICE,
                            SPI_SPEED_HZ=SPI_SPEED_HZ)  # Initialize the strip

#Initialize UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

#Initialize Goggles
lg = light_goggles.LightGoggles(strip, sock)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    #loop.create_task(lg.get_new_variables())
    #loop.create_task(goggle_light_show_templates.show_R(lg))
    loop.create_task(lg.receive_vid_stream())
    
    #await asyncio.gather(lg.get_new_variables())

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/goggles/brightness")
async def read_brightness():
    return {"brightness": lg.strip.global_brightness}

@app.post("/goggles/brightness/{brightness}")
async def set_brightness(brightness: int, q: Union[str, None] = None):
    lg.strip.global_brightness = brightness
    return {"brightness": brightness, "q": q}

@app.post("/goggles/mode/{mode}")
async def set_mode(mode: str, q: Union[str, None] = None):
    if mode == "rest":
        lg.rest_mode = True
    if mode == "play":
        lg.rest_mode = False
    return {"mode": mode, "q":q}


