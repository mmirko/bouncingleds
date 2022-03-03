#!/usr/bin/env python3

import re
import time
import argparse
import random

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport

def gravity(device,gravx,gravy,tminus1):
    posx=tminus1[0]
    posy=tminus1[1]
    velx=tminus1[2]
    vely=tminus1[3]

    return (posx,posy,velx+gravx*(device.width-posx),vely+gravy*(device.height-posy))

def friction(device,frx,fry,tminus1):
    posx=tminus1[0]
    posy=tminus1[1]
    velx=tminus1[2]
    vely=tminus1[3]

    return (posx,posy,velx*(1-frx),vely*(1-fry))

def pfunction(device, tminus1, xaxis_friction, yaxis_friction, x_gravity, y_gravity):
    
    if x_gravity != 0.0 or y_gravity != 0.0:
        tminus1=gravity(device,x_gravity,y_gravity,tminus1)

    if xaxis_friction != 0.0 or yaxis_friction != 0.0:
        tminus1=friction(device,xaxis_friction,yaxis_friction,tminus1)

    posx=tminus1[0]
    posy=tminus1[1]
    velx=tminus1[2]
    vely=tminus1[3]

    # Vertical walls
    if posx+velx >= device.width or posx+velx < 0:
        velx=-velx
    
    # Horizontal walls
    if posy+vely >= device.height or posy+vely < 0:
        vely=-vely

    return (posx+velx,posy+vely,velx,vely)

def impulse(device,tminus1):
    posx=tminus1[0]
    posy=tminus1[1]
    velx=tminus1[2]
    vely=tminus1[3]

    return (posx,posy,random.randint(-10,2),random.randint(-2,2))

def nearest(p):
    return(p)

def bounce(n, block_orientation, rotate, inreverse, particles, xaxis_friction, yaxis_friction, x_gravity, y_gravity):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
                     rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)

    numparticles = particles
    tminus1 = []

    for i in range(numparticles):
        tminus1.append([random.randint(0,device.width-1),random.randint(0,device.height-1),random.randint(-2,2),random.randint(-2,2)])
        #tminus1.append([random.randint(0,device.width-1),random.randint(0,device.height-1),4.0*random.random()-2.0, 4.0*random.random()-2.0])
        #tminus1.append([random.randint(0,device.width-1),random.randint(0,device.height-1),0,4.0*random.random()-2.0])

    fcvount=0    
    while True:

        floorcheck=True
        with canvas(device) as draw:
            for i in range(numparticles):
                tminus1[i] = pfunction(device, tminus1[i], xaxis_friction, yaxis_friction, x_gravity, y_gravity)
                draw.point(nearest((tminus1[i][0],tminus1[i][1])),255)
                if tminus1[i][0] < device.width - 1 :
                    floorcheck=False

        time.sleep(0.1)

        if floorcheck:
            fcvount+=1
            if fcvount==10:
                for i in range(numparticles):
                    tminus1[i] = impulse(device, tminus1[i])
                fcvount=0
        else:
            fcvount=0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='raspi4 arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--xaxis-gravity', type=float, default=0.05, help='Gravity on X axis')
    parser.add_argument('--yaxis-gravity', type=float, default=0.0, help='Gravity on Y axis')
    parser.add_argument('--xaxis-friction', type=float, default=0.05, help='Friction on X axis')
    parser.add_argument('--yaxis-friction', type=float, default=0.05, help='Friction on Y axis')
    parser.add_argument('--particles', '-p', type=int, default=5, help='Number of particles')
    parser.add_argument('--cascaded', '-n', type=int, default=4, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=-90, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    try:
        bounce(args.cascaded, args.block_orientation, args.rotate, args.reverse_order, args.particles, args.xaxis_friction, args.yaxis_friction, args.xaxis_gravity, args.yaxis_gravity)
    except KeyboardInterrupt:
        pass
