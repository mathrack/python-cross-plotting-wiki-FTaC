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

u = quantity(case, "qty_u.dat")
v = quantity(case, "qty_v.dat")
w = quantity(case, "qty_w.dat")
p = quantity(case, "qty_p.dat")
t = quantity(case, "qty_t.dat")

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

u_buoy = quantity(case, "qty_bud_u_buoy.dat")
u_conv = quantity(case, "qty_bud_u_conv.dat")
u_diff = quantity(case, "qty_bud_u_diff.dat")
u_gradp = quantity(case, "qty_bud_u_gradp.dat")
u_turb = quantity(case, "qty_bud_u_turb.dat")
bud_u = budget(case, "bud_u.dat")

v_conv = quantity(case, "qty_bud_v_conv.dat")
v_diff = quantity(case, "qty_bud_v_diff.dat")
v_gradp = quantity(case, "qty_bud_v_gradp.dat")
v_turb = quantity(case, "qty_bud_v_turb.dat")
bud_v = budget(case, "bud_v.dat")

w_conv = quantity(case, "qty_bud_w_conv.dat")
w_diff = quantity(case, "qty_bud_w_diff.dat")
w_gradp = quantity(case, "qty_bud_w_gradp.dat")
w_turb = quantity(case, "qty_bud_w_turb.dat")
bud_w = budget(case, "bud_w.dat")

t_conv = quantity(case, "qty_bud_t_conv.dat")
t_diff = quantity(case, "qty_bud_t_diff.dat")
t_turb = quantity(case, "qty_bud_t_turb.dat")
bud_t = budget(case, "bud_t.dat")

if False:
   x = 0.1
   fig, ax = k.xplot(x)
   fig, ax = uu.xplot(x, fig, ax)
   fig, ax = vv.xplot(x, fig, ax)
   fig, ax = ww.xplot(x, fig, ax)
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

# Check budget of <U>
if False:
   x=0.1
   fig, ax = xplot(x, u_conv)
   fig, ax = xplot(x, u_gradp, fig, ax)
   fig, ax = xplot(x, u_diff, fig, ax)
   fig, ax = xplot(x, u_turb, fig, ax)
   fig, ax = xplot(x, u_buoy, fig, ax)
   ax.set_ylabel(r"Budget of $\overline{U}$")
   ax.legend()
   fig.show()
   fig, ax = bud_u.xplot(x)
   fig.show()
   fig, ax = bud_u.xypie(x, 0.1)
   fig.show()
   fig, ax = bud_u.ijpie(10, 40)
   fig.show()

# Check budget of <V>
if False:
   x=0.1
   fig, ax = xplot(x, v_conv)
   fig, ax = xplot(x, v_gradp, fig, ax)
   fig, ax = xplot(x, v_diff, fig, ax)
   fig, ax = xplot(x, v_turb, fig, ax)
   ax.set_ylabel(r"Budget of $\overline{V}$")
   ax.legend()
   fig.show()
   fig, ax = bud_v.xplot(x)
   fig.show()

# Check budget of <W>
if False:
   x=0.1
   fig, ax = xplot(x, w_conv)
   fig, ax = xplot(x, w_gradp, fig, ax)
   fig, ax = xplot(x, w_diff, fig, ax)
   fig, ax = xplot(x, w_turb, fig, ax)
   ax.set_ylabel(r"Budget of $\overline{W}$")
   ax.legend()
   fig.show()
   fig, ax = bud_w.xplot(x)
   fig.show()

# Check budget of <T>
if False:
   x=0.1
   fig, ax = xplot(x, t_conv)
   fig, ax = xplot(x, t_diff, fig, ax)
   fig, ax = xplot(x, t_turb, fig, ax)
   ax.set_ylabel(r"Budget of $\overline{T}$")
   ax.legend()
   fig.show()
   fig, ax = bud_t.xplot(x)
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
if False:
   fig, axs = plt.subplots(1, 3, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(dudx, fig, axs[0])
   fig, axs[1] = xyplot(dudy, fig, axs[1])
   fig, axs[2] = xyplot(dudz, fig, axs[2])
   fig.show()

# Check grad(v)
if False:
   fig, axs = plt.subplots(1, 3, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(dvdx, fig, axs[0])
   fig, axs[1] = xyplot(dvdy, fig, axs[1])
   fig, axs[2] = xyplot(dvdz, fig, axs[2])
   fig.show()

# Check grad(w)
if False:
   fig, axs = plt.subplots(1, 3, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(dwdx, fig, axs[0])
   fig, axs[1] = xyplot(dwdy, fig, axs[1])
   fig, axs[2] = xyplot(dwdz, fig, axs[2])
   fig.show()

# Check grad(p)
if False:
   fig, axs = plt.subplots(1, 3, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(dpdx, fig, axs[0])
   fig, axs[1] = xyplot(dpdy, fig, axs[1])
   fig, axs[2] = xyplot(dpdz, fig, axs[2])
   fig.show()

# Check grad(t)
if False:
   fig, axs = plt.subplots(1, 3, subplot_kw={"projection": "3d"})
   fig, axs[0] = xyplot(dtdx, fig, axs[0])
   fig, axs[1] = xyplot(dtdy, fig, axs[1])
   fig, axs[2] = xyplot(dtdz, fig, axs[2])
   fig.show()

