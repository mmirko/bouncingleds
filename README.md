# BouncingLeds

A simple python script to make leds bouncing like crazy.

![Example](example.gif)

The script uses the [Luma library](https://luma-led-matrix.readthedocs.io) and targets a 8x8(x4) led matrix based on the MAX7219 chip (but probably it will work also for other devices based on it).

Connect the device, install Luma as explained on the library instructions and you will be ready to execute it.

The image shows the default of 5 bouncing leds, [Full video](https://youtu.be/6u6TJ07zb0s). Some other examples are:

One led with no gravity and no friction:

```
bouncingleds.py -p 1 --xaxis-gravity 0.0 --xaxis-friction 0.0 --yaxis-riction 0.0
```

Ten leds:

```
bouncingleds.py -p 10
```


The full option list is:


```
usage: bouncingleds.py [-h] [--xaxis-gravity XAXIS_GRAVITY]
                       [--yaxis-gravity YAXIS_GRAVITY]
                       [--xaxis-friction XAXIS_FRICTION]
                       [--yaxis-friction YAXIS_FRICTION]
                       [--particles PARTICLES] [--cascaded CASCADED]
                       [--block-orientation {0,90,-90}] [--rotate {0,1,2,3}]
                       [--reverse-order REVERSE_ORDER]

bouncingleds arguments

optional arguments:
  -h, --help            show this help message and exit
  --xaxis-gravity XAXIS_GRAVITY
                        Gravity on X axis (default: 0.05)
  --yaxis-gravity YAXIS_GRAVITY
                        Gravity on Y axis (default: 0.0)
  --xaxis-friction XAXIS_FRICTION
                        Friction on X axis (default: 0.05)
  --yaxis-friction YAXIS_FRICTION
                        Friction on Y axis (default: 0.05)
  --particles PARTICLES, -p PARTICLES
                        Number of particles (default: 5)
  --cascaded CASCADED, -n CASCADED
                        Number of cascaded MAX7219 LED matrices (default: 4)
  --block-orientation {0,90,-90}
                        Corrects block orientation when wired vertically
                        (default: -90)
  --rotate {0,1,2,3}    Rotate display 0=0°, 1=90°, 2=180°, 3=270° (default:
                        0)
  --reverse-order REVERSE_ORDER
                        Set to true if blocks are in reverse order (default:
                        False)
```