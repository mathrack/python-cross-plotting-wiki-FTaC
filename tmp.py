#! /usr/bin/env python3

# Import numpy and matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Import local modules from the file module.py in the current directory
from module import *

#
# Read parameters for the present case
#
case = setup(r"case_ra_1e8_lin.dat")

# Load quantities <U>, <V>, <W>, <P> and <T>
u = quantity(case, "qty_u.dat")
v = quantity(case, "qty_v.dat")
w = quantity(case, "qty_w.dat")
p = quantity(case, "qty_p.dat")
t = quantity(case, "qty_t.dat")

# Load gradients of <U>, <V>, <W>, <P>, <T>
dudx = quantity(case, "qty_dudx.dat")
dudy = quantity(case, "qty_dudy.dat")
dudz = quantity(case, "qty_dudz.dat")
dvdx = quantity(case, "qty_dvdx.dat")
dvdy = quantity(case, "qty_dvdy.dat")
dvdz = quantity(case, "qty_dvdz.dat")
dwdx = quantity(case, "qty_dwdx.dat")
dwdy = quantity(case, "qty_dwdy.dat")
dwdz = quantity(case, "qty_dwdz.dat")
dpdx = quantity(case, "qty_dpdx.dat")
dpdy = quantity(case, "qty_dpdy.dat")
dpdz = quantity(case, "qty_dpdz.dat")
dtdx = quantity(case, "qty_dphidx.dat")
dtdy = quantity(case, "qty_dphidy.dat")
dtdz = quantity(case, "qty_dphidz.dat")

# Load quantities k, Reynolds stress, temperature variance, turbulent heat flux, pressure variance
k = quantity(case, "qty_k.dat")
uu = quantity(case, "qty_uu.dat")
vv = quantity(case, "qty_vv.dat")
ww = quantity(case, "qty_ww.dat")
uv = quantity(case, "qty_uv.dat")
uw = quantity(case, "qty_uw.dat")
vw = quantity(case, "qty_vw.dat")
tt = quantity(case, "qty_tt.dat")
ut = quantity(case, "qty_ut.dat")
vt = quantity(case, "qty_vt.dat")
wt = quantity(case, "qty_wt.dat")
pp = quantity(case, "qty_pp.dat")

# Load budget of <U>, <V>, <W>, <T>
bud_u = budget(case, "bud_u.dat")
bud_v = budget(case, "bud_v.dat")
bud_w = budget(case, "bud_w.dat")
bud_t = budget(case, "bud_t.dat")

# Load budget of Reynolds stress
if False:
   bud_uu = budget(case, "bud_uu.dat")
   bud_vv = budget(case, "bud_vv.dat")
   bud_ww = budget(case, "bud_ww.dat")
   bud_uv = budget(case, "bud_uv.dat")
else:
   bud_uu = budget(case, "bud_uu_bis.dat")
   bud_vv = budget(case, "bud_vv_bis.dat")
   bud_ww = budget(case, "bud_ww_bis.dat")
   bud_uv = budget(case, "bud_uv_bis.dat")

# Load budget of the turbulent kinetic energy
bud_k = budget(case, "bud_k.dat")

# Load budget of turbulent heat flux
bud_ut = budget(case, "bud_ut.dat")
bud_vt = budget(case, "bud_vt.dat")

# Load budget of temperature variance
bud_tt = budget(case, "bud_tt.dat")

#
# Examples below illustrate visualization of quantities and budgets
#
# Switch False to True to activate any given example
#

# Some 1D plot at x=0.1
if False:
   x = 0.1
   fig, ax = k.xplot(x)
   fig, ax = uu.xplot(x, fig, ax)
   fig, ax = vv.xplot(x, fig, ax)
   fig, ax = ww.xplot(x, fig, ax)
   ax.set_ylabel("")
   ax.legend()
   fig.show()

# Some 1D plot at y=0.9
if False:
   y = 0.9
   fig, ax = yplot(y, k)
   fig, ax = yplot(y, uu, fig, ax)
   fig, ax = yplot(y, vv, fig, ax)
   fig, ax = yplot(y, ww, fig, ax)
   ax.set_ylabel("")
   ax.legend()
   fig.show()

# Some contour plots
if False:
   fig, axs = plt.subplots(1, 2)
   fig, axs[0] = xyctr(t, fig, axs[0])
   fig, axs[1] = xyctr(tt, fig, axs[1])
   fig.show()

# Budget of <U>
if False:
   x=0.1
   fig, ax = bud_u.xplot(x)
   fig.show()
   fig, ax = bud_u.xypie(x, 0.1)
   fig.show()
   fig, ax = bud_u.ijpie(10, 40)
   fig.show()

# Budget of <V>
if False:
   x=0.1
   fig, ax = bud_v.xplot(x)
   fig.show()

# Budget of <W>
if False:
   x=0.1
   fig, ax = bud_w.xplot(x)
   fig.show()

# Budget of <T>
if False:
   x=0.1
   fig, ax = bud_t.xplot(x)
   fig.show()

#
# xyplot requires Axes3D
#
from mpl_toolkits.mplot3d import Axes3D

# Surface plot of temperature average and variance
if False:
   fig, axs = plt.subplots(1, 2, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(t, fig, axs[0])
   fig, axs[1] = xyplot(tt, fig, axs[1])
   fig.show()

# More surface plot
if False:
   fig, axs = plt.subplots(2, 2, subplot_kw={"projection": "3d"})
   fig, axs[0,0] = xyplot(uu, fig, axs[0,0])
   fig, axs[1,0] = xyplot(vv, fig, axs[1,0])
   fig, axs[0,1] = xyplot(ww, fig, axs[0,1])
   fig, axs[1,1] = xyplot(k, fig, axs[1,1])
   fig.show()

# Surface plot of grad(t)
if False:
   fig, axs = plt.subplots(1, 3, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(dtdx, fig, axs[0])
   fig, axs[1] = xyplot(dtdy, fig, axs[1])
   fig, axs[2] = xyplot(dtdz, fig, axs[2])
   fig.show()

