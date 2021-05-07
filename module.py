#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from os.path import join as ospjoin

#
# Small function to read one binary field
# Returns a 2D array of size (nx, ny)
#
def read_one(case, file):
   output = np.fromfile(ospjoin(case.folder, file)).reshape((case.ny, case.nx))
   return output.transpose()

#
# Small function to extract the scaling parameter
# Returns a float
#
def get_scaling(case, term):
   # Try to read a float
   try:
      scaling = np.float(term)
      return scaling
   except ValueError:
      if term=="pr" or term=="Pr":
         return case.pr
      elif term=="ra" or term=="Ra":
         return case.ra
      elif term=="rapr" or term=="RaPr" or term=="prra" or term=="PrRa":
         return case.ra * case.pr
      if term=="dt" or term=="Dt" or term=="DT":
         return case.dt
      else:
         print("Error when reading the scaling factor")
         return 1.

#
# Create a class for the setup of the case
#
class setup:
   #
   # Initialize with a config file
   #
   def __init__(self, config):
      self.config = np.str(config)
      #
      # Read the config file
      #   Comment line(s) start with '#'
      #   Followed by some mandatory fields
      #     nx
      #     ny
      #     dt
      #     Ra
      #     Pr
      #     Sub-folder with the results
      #
      [nx, ny, dt, ra, pr, data_folder] = np.loadtxt(self.config, dtype=str)
      self.nx = np.int(nx)
      self.ny = np.int(ny)
      self.dt = np.float(dt)
      self.ra = np.float(ra)
      self.pr = np.float(pr)
      self.folder = np.str(data_folder)
      # Here, the size of the domain in X is hard-coded
      self.xx = np.linspace(0., 1., nx)
      # Read the Y grid, the name of the file is hard-coded
      self.yy = np.loadtxt(ospjoin(self.folder, "yp.dat"), dtype=float)[:,1]
   
   #
   # Add basic and detailed description
   #
   def __repr__(self):
      return self.config
   def __str__(self):
      return "Setup of the case :" + "\n" \
             "   Config file : " + self.config + "\n" \
             "   (nx, ny) : (" + np.str(self.nx) + ", " + np.str(self.ny) + ")\n" \
             "   Time step : " + np.str(self.dt) + "\n" \
             "   Rayleigh number : " + np.str(self.ra) + "\n" \
             "   Prandtl number : " + np.str(self.pr) + "\n" \
             "   Data folder : " + self.folder

#
# Create a class for a given quantity
#
class quantity:
   #
   # Initialize with a config file
   #
   def __init__(self, case, config):
      # Corresponding setup
      self.case = case
      # Name of the config file
      self.config = np.str(config)
      # Value of the quantity on the 2D grid
      self.data = np.zeros((case.nx, case.ny))
      #
      # Read the config file
      #
      tmp = []
      for line in open(self.config,"r").read().splitlines():
         if line[0] != "#":
            tmp.append(line)
      
      # Name of the quantity for legends
      self.name = np.str(tmp[0])
      # Number of terms in the quantity
      self.nterms = np.abs(np.int(tmp[1]))
      # Build from binary files ?
      self.build_from_binary = (np.int(tmp[1]) > 0)
      # Put each term inside data
      for iterm in range(np.abs(self.nterms)):
         term = np.ones((case.nx, case.ny))
         list_term = tmp[iterm+2].split()
         for item in range(len(list_term)-1):
            if self.build_from_binary:
               term = term * read_one(case, np.str(list_term[item]))
            else:
               term = term * quantity(case, np.str(list_term[item])).data
         
         self.data = self.data + term * get_scaling(case, list_term[-1])
      
      self.data = self.data * get_scaling(case, tmp[self.nterms+2])
      # Some basic metrics
      self.min = np.min(self.data)
      self.max = np.max(self.data)
      self.absmax = np.max(np.abs(self.data))
      
      # Optional parameters for 1D plots
      if len(tmp) > self.nterms+3:
         self.clr = np.str(tmp[self.nterms+3])
         self.mrkedgeclr = np.str(tmp[self.nterms+4])
         self.mrkfaceclr = 'none'
         self.markevery = np.int(tmp[self.nterms+5])
      else :
         self.clr = None
         self.mrkedgeclr = 'none'
         self.mrkfaceclr = 'none'
         self.markevery = 'none'
   
   #
   # Add basic and detailed description
   #
   def __repr__(self):
      return self.config
   def __str__(self):
      return np.str(self.case) + "\n" \
             "Setup of the quantity :" + "\n" \
             "   Config file : " + self.config + "\n" \
             "   Name of the quantity : " + self.name + "\n" \
             "   Constructed from binary files : " + np.str(self.build_from_binary) + "\n" \
             "   Number of terms : " + np.str(self.nterms) + "\n" \
             "   Min / Max : " + np.str(self.min) + " / " + np.str(self.max) + "\n" \
             "   clr : " + np.str(self.clr) + "\n" \
             "   mrkedgeclr : " + np.str(self.mrkedgeclr) + "\n" \
             "   mrkfaceclr : " + np.str(self.mrkfaceclr) + "\n" \
             "   markevery : " + np.str(self.markevery)

#
# Create a class for a given budget TODO
#
class budget:
   #
   # Initialize with a config file
   #
   def __init__(self, case, config, title = "", xlab = "", ylab = ""):
      # Corresponding setup
      self.case = case
      # Name of the config file
      self.config = np.str(config)
      # Default title for plots
      self.title = title
      # Default xlabel for 2D plots
      self.xlab = xlab
      # Default ylabel for 2D plots
      self.ylab = ylab
      #
      # Read the config file
      #   Comment line(s) start with '#'
      #   Followed by some mandatory fields
      #     number of terms in the budget
      #     the config file for each term (one config file per line)
      #   And some optional fields
      #      title
      #      xlab
      #      ylab
      #
      tmp = np.loadtxt(self.config, dtype=str)
      # Number of terms in the budget
      self.nterms = np.int(tmp[0])
      # List of the terms
      self.qty_list = tmp[1:self.nterms+1]
      # Build each term in the budget
      self.terms = []
      for term in self.qty_list:
         terms.append(quantity(case, term))
      
      # Config file can provide title, xlab and ylab if they are not provided in python
      if self.title == "" and len(tmp)==self.nterms+4:
         self.title = config_title
      
      if self.xlab == "" and len(tmp)==self.nterms+4:
         self.xlab = config_xlab
      
      if self.ylab == "" and len(tmp)==self.nterms+4:
         self.ylab = config_ylab
   
   #
   # Add basic and detailed description
   #
   def __repr__(self):
      return self.config
   def __str__(self):
      return "Setup of the case associated with the budget : \n" + \
             np.str(self.case) + "\n" \
             "Setup of the budget :" + "\n" \
             "   Config file : " + self.config + "\n" \
             "   nterms : " + np.str(self.nterms) + "\n" \
             "   terms are defined in : " + self.qty_list + "\n" \
             "   Title : " + self.title + "\n" \
             "   xlabel : " + self.xlabel + "\n" \
             "   ylabel : " + self.ylabel

#
# Plot given quantity at given location x_i for all y
#
def iplot(i, qty, fig = None, ax = None):
   #
   # Safety check
   #
   if i<0 or i>qty.case.nx-1:
      print("Incorrect value for i in iplot : " + np.str(i))
      return None
   # New figure and axes if none provided
   if fig == None or ax == None:
      fig, ax = plt.subplots()
   if qty.clr == None:
      ax.plot(qty.case.yy, qty.data[i,:], label=qty.name)
   else:
      ax.plot(qty.case.yy, qty.data[i,:], label=qty.name, \
                                          fmt=qty.clr, \
                                          markeredgecolor=qty.mrkedgeclr, \
                                          markerfacecolor=qty.mrkfaceclr, \
                                          markevery=qty.markevery)
   ax.set_title("At x = " + np.str(qty.case.xx[i]))
   ax.set_ylabel(qty.name)
   ax.set_xlabel(r'$y$')
   return fig, ax

#
# Plot given quantity at given location y_j for all x
#
def jplot(j, qty, fig = None, ax = None):
   #
   # Safety check
   #
   if j<0 or j>qty.case.ny-1:
      print("Incorrect value for j in jplot : " + np.str(j))
      return None
   # New figure and axes if none provided
   if fig == None or ax == None:
      fig, ax = plt.subplots()
   if qty.clr == None :
      ax.plot(qty.case.xx, qty.data[:,j], label=qty.name)
   else:
      ax.plot(qty.case.xx, qty.data[:,j], label=qty.name, \
                                          fmt=qty.clr, \
                                          markeredgecolor=qty.mrkedgeclr, \
                                          markerfacecolor=qty.mrkfaceclr, \
                                          markevery=qty.markevery)
   ax.set_title("At y = " + np.str(qty.case.yy[j]))
   ax.set_ylabel(qty.name)
   ax.set_xlabel(r'$x$')
   return fig, ax

#
# Plot given quantity at given location x for all y
#
def xplot(x, qty, fig = None, ax = None):
   #
   # Safety check
   #
   if x<0. or x>1.:
      print("Incorrect value for x in xplot : " + np.str(x))
      return None
   #
   # Locate node i
   #
   i = np.where(np.abs(qty.case.xx-x) == np.amin(np.abs(qty.case.xx-x)))[0][0]
   return iplot(i, qty, fig, ax)

#
# Plot given quantity at given location y for all x
#
def yplot(y, qty, fig = None, ax = None):
   #
   # Safety check
   #
   if y<0. or y>1.:
      print("Incorrect value for y in yplot : " + np.str(y))
      return None
   #
   # Locate node j
   #
   j = np.where(np.abs(qty.case.yy-y) == np.amin(np.abs(qty.case.yy-y)))[0][0]
   return jplot(j, qty, fig, ax)

#
# Extract given quantity at given location x_i, y-j
#
def ijval(i, j, qty):
   #
   # Safety check
   #
   if i<0 or i>qty.case.nx-1:
      print("Incorrect value for i in ijval : " + np.str(i))
      return None
   
   if j<0 or j>qty.case.ny-1:
      print("Incorrect value for j in ijval : " + np.str(j))
      return None
   
   return qty.data[i, j]

#
# Extract given quantity at given location x, y
#
def xyval(x, y, qty):
   #
   # Safety check
   #
   if x<0. or x>1.:
      print("Incorrect value for x in xyval : " + np.str(x))
      return None
   
   if y<0. or y>1.:
      print("Incorrect value for y in xyval : " + np.str(y))
      return None
   
   # Locate i, j
   i = np.where(np.abs(qty.case.xx-x) == np.amin(np.abs(qty.case.xx-x)))[0][0]
   j = np.where(np.abs(qty.case.yy-y) == np.amin(np.abs(qty.case.yy-y)))[0][0]
   return ijval(i, j, qty)

#
# Surface plot of given quantity
#
def xyplot(qty, fig = None, ax = None):
   from mpl_toolkits.mplot3d import Axes3D
   # New figure and axes if none provided
   if fig == None or ax == None:
      fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
   xxx, yyy = np.meshgrid(qty.case.xx, qty.case.yy)
   ps = ax.plot_surface(xxx, yyy, np.transpose(qty.data[:,:]))
   #cb = fig.colorbar(ps)
   ax.set_zlabel(qty.name)
   ax.set_ylabel(r'$y$')
   ax.set_xlabel(r'$x$')
   return fig, ax

#
# Contour plot of given quantity
#
def xyctr(qty, fig = None, ax = None):
   # New figure and axes if none provided
   if fig == None or ax == None:
      fig, ax = plt.subplots()
   xxx, yyy = np.meshgrid(qty.case.xx, qty.case.yy)
   ct = ax.contour(xxx, yyy, np.transpose(qty.data[:,:]))
   ax.clabel(ct, ct.levels, inline=True, fontsize=10)
   #cb = fig.colorbar(ct)
   ax.set_title(qty.name)
   ax.set_ylabel(r'$y$')
   ax.set_xlabel(r'$x$')
   return fig, ax


