#! /usr/bin/env python3

# Import numpy and matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Import local modules from the file module.py in the current directory
from module import *

#
# Read parameters for the present case
#
case = setup(r"param.dat")

u = quantity(case, "u.dat")
v = quantity(case, "v.dat")
w = quantity(case, "w.dat")
p = quantity(case, "p.dat")
t = quantity(case, "phi.dat")

dudx = quantity(case, "dudx.dat")
dudy = quantity(case, "dudy.dat")
dudz = quantity(case, "dudz.dat")

dvdx = quantity(case, "dvdx.dat")
dvdy = quantity(case, "dvdy.dat")
dvdz = quantity(case, "dvdz.dat")

dwdx = quantity(case, "dwdx.dat")
dwdy = quantity(case, "dwdy.dat")
dwdz = quantity(case, "dwdz.dat")

k = quantity(case, "k.dat")
uu = quantity(case, "uu.dat")
vv = quantity(case, "vv.dat")
ww = quantity(case, "ww.dat")
uv = quantity(case, "uv.dat")
uw = quantity(case, "uw.dat")
vw = quantity(case, "vw.dat")
tt = quantity(case, "phiphi.dat")
ut = quantity(case, "uphi.dat")
vt = quantity(case, "vphi.dat")
wt = quantity(case, "wphi.dat")


if False:
   x = 0.1
   fig, ax = xplot(x, k)
   fig, ax = xplot(x, uu, fig, ax)
   fig, ax = xplot(x, vv, fig, ax)
   fig, ax = xplot(x, ww, fig, ax)
   ax.set_ylabel("")
   ax.legend()
   fig.show()

if False:
   y = 0.9
   fig, ax = yplot(y, k)
   fig, ax = yplot(y, uu, fig, ax)
   fig, ax = yplot(y, vv, fig, ax)
   fig, ax = yplot(y, ww, fig, ax)
   ax.set_ylabel("")
   ax.legend()
   fig.show()

if False:
   fig, axs = plt.subplots(1, 2)
   fig, axs[0] = xyctr(t, fig, axs[0])
   fig, axs[1] = xyctr(tt, fig, axs[1])
   fig.show()

# xyplot requires Axes3D
from mpl_toolkits.mplot3d import Axes3D

if False:
   fig, axs = plt.subplots(1, 2, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(t, fig, axs[0])
   fig, axs[1] = xyplot(tt, fig, axs[1])
   fig.show()

if False:
   fig, axs = plt.subplots(2, 2, subplot_kw={"projection": "3d"})
   fig, axs[0,0] = xyplot(uu, fig, axs[0,0])
   fig, axs[1,0] = xyplot(vv, fig, axs[1,0])
   fig, axs[0,1] = xyplot(ww, fig, axs[0,1])
   fig, axs[1,1] = xyplot(k, fig, axs[1,1])
   fig.show()

# Check grad(u)
if True:
   fig, axs = plt.subplots(1, 3, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(dudx, fig, axs[0])
   fig, axs[1] = xyplot(dudy, fig, axs[1])
   fig, axs[2] = xyplot(dudz, fig, axs[2])
   fig.show()

# Check grad(v)
if True:
   fig, axs = plt.subplots(1, 3, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(dvdx, fig, axs[0])
   fig, axs[1] = xyplot(dvdy, fig, axs[1])
   fig, axs[2] = xyplot(dvdz, fig, axs[2])
   fig.show()

# Check grad(w)
if True:
   fig, axs = plt.subplots(1, 3, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(dwdx, fig, axs[0])
   fig, axs[1] = xyplot(dwdy, fig, axs[1])
   fig, axs[2] = xyplot(dwdz, fig, axs[2])
   fig.show()

#
# Read parameters for the present budget
#
#bud = budget(case = case, config = r"budget_u.dat")

