#!/usr/bin/env python

from math import *
import sys

def rotate(x, y, degrees):
    c = cos(pi * degrees / 180.0)
    s = sin(pi * degrees / 180.0)
    return x * c + y * s, y * c - x * s

def width():
    # Extrusion vertical edge near metal bend.
    x1 = extrusion_width / 2
    y1 = frame_radius
    # Same point on other end of panel.
    x2, y2 = rotate(-x1, y1, 120)
    # Width of the straight section, between extrusion bends.
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def move(verb, **kwargs):
    keys = kwargs.keys()
    keys.sort()
    words = [verb.upper()]
    for key in keys:
        words.append('%s%g' % (key.upper(), kwargs[key]))
    print ' '.join(words)

def linear(**kwargs): move('G1', **kwargs)
def clockwise(**kwargs): move('G2', **kwargs)

def up(): linear(z=20)
def down(): linear(z=0)

def jump(**kwargs):
    up()
    linear(**kwargs)
    down()

frame_radius = 150
frame_height = 75
frame_width = 250  # Extrusion to extrusion.
flange = 12
drill = 1.6  # 1/16 inch radius.

extrusion_width = 15
extrusion_thickness = 15

motor_screw_grid = 31
motor_cutout_diameter = 22
motor_width = 42.2
motor_offset = 30  # Motor face to extrusion.
motor_side, motor_bend = rotate(0, motor_offset, 30)
motor_side += extrusion_width/2
mc = motor_cutout_diameter/2 + drill

thickness = 0.0478 * 25.4  # 18 gauge steel.
roundness = 7.5

print >> sys.stderr, 'thickness', thickness
print >> sys.stderr, 'motor_bend', motor_bend
print >> sys.stderr, 'motor_side', motor_side
print >> sys.stderr, 'mc', mc
print >> sys.stderr, 'extrusion-to-extrusion', frame_width
print >> sys.stderr, 'edge-to-edge', frame_width + 2*extrusion_thickness

xa = frame_width/2 + extrusion_thickness + drill  # Outside
xb = frame_width/2 + extrusion_thickness - roundness
xc = frame_width/2 + extrusion_thickness/2  # Extrusion screws
xe = frame_width/2  # Extrusion corner
xf = frame_width/2 - flange/tan(pi/12)/2  # 15 degrees
xt = frame_width/2 - motor_bend
xm = xt + motor_side
xms = xm - motor_screw_grid/2
xmc = xm - mc

ya = frame_height/2 + drill  # Top without flange
yb = frame_height/2 - roundness
yc = frame_height/2 - extrusion_thickness/2  # Extrusion screws
yf = frame_height/2 + flange + drill  # Top flange
yg = frame_height/2 + flange/2 + drill  # Half flange
yt = motor_width/2 + drill
yt2 = yt + 4
ym = 0
yms = ym + motor_screw_grid/2
ymc = ym + mc

r = roundness + drill

print 'G17 ; Select XY plane for arcs'
print 'G90 ; Absolute coordinates'
print '; Start at bottom left corner'
move('G92', x=-xa, y=-yg, z=0)
linear(x=-xa, y=-yg, z=0)

print '; Screw holes for extrusion'
for x in (-1, 1):
    jump(x=x*xc, y=x*yc)
    jump(x=x*xms, y=x*yms)
    jump(x=x*xms, y=-1*x*yms)
    jump(x=x*xc, y=-1*x*yc)

print '; Motor tabs'
for x in (1, -1):
    jump(x=x*xt, y=-x*yt2)
    linear(x=x*xm, y=-x*yt)
    linear(y=-x*ymc)
    clockwise(y=x*ymc, r=mc)
    linear(y=x*yt)
    linear(x=x*xt, y=x*yt2)

print '; Left wing (for vertical extrusion)'
jump(x=-xb, y=-ya)
clockwise(x=-xa, y=-yb, i=0, j=r)
linear(y=yb)
clockwise(x=-xb, y=ya, i=r, j=0)

print '; Top flange'
linear(x=-xb, y=ya)
linear(x=-xe)
linear(y=yg)
linear(x=-xf, y=yf)
linear(x=xf)
linear(x=xe, y=yg)
linear(y=ya)
linear(x=xb)

print '; Right wing (for vertical extrusion)'
clockwise(x=xa, y=yb, i=0, j=-r)
linear(y=-yb)
clockwise(x=xb, y=-ya, i=-r, j=0)

print '; Bottom flange'
linear(x=xe)
linear(y=-yg)
linear(x=-xe)
linear(y=-ya)
linear(x=-xa)
