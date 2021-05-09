#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from os.path import join as ospjoin

#
# Small function to read one field
# Returns a 2D array of size (nx, ny)
#
# If file starts with "qty_", the quantity constructor is used
#
# Otherwise, a binary file is read
#
def read_one(case, file):
   if file[:4]=="qty_":
      output = quantity(case, file).data
   else:
      output = (np.fromfile(ospjoin(case.folder, file)).reshape((case.ny, case.nx))).transpose()
   return output

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
      if term=="pr" or term=="Pr" or term=="PR":
         return case.pr
      elif term=="ra" or term=="Ra" or term=="RA":
         return case.ra
      elif term=="sqrtra" or term=="sqrtRa" or term=="sqrtRA":
         return np.sqrt(case.ra)
      if term=="re" or term=="Re" or term=="RE":
         return np.sqrt(case.ra) / case.pr
      elif term=="rapr" or term=="RaPr" or term=="RAPR" or term=="prra" or term=="PrRa" or term=="PRRA":
         return case.ra * case.pr
      if term=="dt" or term=="Dt" or term=="DT":
         return case.dt
      if term=="invdt" or term=="invDt" or term=="invDT":
         return 1./case.dt
      if term=="-invdt" or term=="-invDt" or term=="-invDT":
         return - 1./case.dt
      if term=="invdt2" or term=="invDt2" or term=="invDT2":
         return 1./case.dt**2
      if term=="-invdt2" or term=="-invDt2" or term=="-invDT2":
         return -1./case.dt**2
      if term=="invre" or term=="invRe" or term=="invRE":
         return case.pr / np.sqrt(case.ra)
      if term=="-invre" or term=="-invRe" or term=="-invRE":
         return - case.pr / np.sqrt(case.ra)
      elif term=="invsqrtra" or term=="invsqrtRa" or term=="invsqrtRA":
         return 1./np.sqrt(case.ra)
      elif term=="-invsqrtra" or term=="-invsqrtRa" or term=="-invsqrtRA":
         return - 1./np.sqrt(case.ra)
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
      # Here, RK3 final time step is hard-coded
      self.dt = (4./12.) * self.dt # 3./4. - 5./12.
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
      self.nterms = np.int(tmp[1])
      # Put each term inside data
      for iterm in range(np.abs(self.nterms)):
         term = np.ones((case.nx, case.ny))
         list_term = tmp[iterm+2].split()
         for item in range(len(list_term)-1):
            term = term * read_one(case, np.str(list_term[item]))
         
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
   # Add post-processing
   #
   def iplot(self, i, fig = None, ax = None):
      return iplot(i, self, fig, ax)
   def jplot(self, j, fig = None, ax = None):
      return jplot(j, self, fig, ax)
   def xplot(self, x, fig = None, ax = None):
      return xplot(x, self, fig, ax)
   def yplot(self, y, fig = None, ax = None):
      return yplot(y, self, fig, ax)
   def ijval(self, i, j):
      return ijval(i, j, self)
   def xyval(self, x, y):
      return xyval(x, y, self)
   def xyplot(self, fig = None, ax = None):
      return xyplot(self, fig, ax)
   def xyctr(self, fig = None, ax = None):
      return xyctr(self, fig, ax)
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
             "   Number of terms : " + np.str(self.nterms) + "\n" \
             "   Min / Max : " + np.str(self.min) + " / " + np.str(self.max) + "\n" \
             "   clr : " + np.str(self.clr) + "\n" \
             "   mrkedgeclr : " + np.str(self.mrkedgeclr) + "\n" \
             "   mrkfaceclr : " + np.str(self.mrkfaceclr) + "\n" \
             "   markevery : " + np.str(self.markevery)

#
# Create a class for a given budget
#
class budget:
   #
   # Initialize with a config file
   #
   def __init__(self, case, config):
      # Corresponding setup
      self.case = case
      # Name of the config file
      self.config = np.str(config)
      #
      # Read the config file
      #   Comment line(s) start with '#'
      #   Followed by some mandatory fields
      #     Name of the budget
      #     the quantity file for each term
      #     "Y" or "N" to compute the error
      #
      tmp = []
      for line in open(self.config,"r").read().splitlines():
         if line[0] != "#":
            tmp.append(line)
      # Name
      self.name = np.str(tmp[0])
      # Number of terms in the budget
      self.nterms = np.int(len(tmp)-2)
      # List of the terms
      self.qty_list = tmp[1:self.nterms+1]
      # Build each term in the budget
      self.terms = []
      for term in self.qty_list:
         self.terms.append(quantity(case, term))
      
      # Compute the error ?
      if tmp[-1]=="Y" or tmp[-1]=="y":
         self.nterms = self.nterms + 1
         error = quantity.__new__(quantity)
         error.case = case
         error.config = "Auto"
         error.name = "Error"
         error.nterms = self.nterms - 1
         error.data = np.zeros((case.nx, case.ny))
         for term in self.terms:
            error.data = error.data + term.data
         error.min = np.min(error.data)
         error.max = np.max(error.data)
         error.absmax = np.max(np.abs(error.data))
         error.clr = ":k"
         error.mrkedgeclr = 'none'
         error.mrkfaceclr = 'none'
         error.markevery = 'none'
         self.terms.append(error)
   
   #
   # Add post-processing
   #
   def iplot(self, i, fig = None, ax = None):
      # New figure and axes if none provided
      if fig == None or ax == None:
         fig, ax = plt.subplots()
      # Plot all terms
      for term in self.terms:
         fig, ax = term.iplot(i, fig, ax)
      ax.set_ylabel(self.name)
      ax.legend()
      return [fig, ax]
   def jplot(self, j, fig = None, ax = None):
      # New figure and axes if none provided
      if fig == None or ax == None:
         fig, ax = plt.subplots()
      # Plot all terms
      for term in self.terms:
         fig, ax = term.jplot(j, fig, ax)
      ax.set_ylabel(self.name)
      ax.legend()
      return [fig, ax]
   def xplot(self, x, fig = None, ax = None):
      # New figure and axes if none provided
      if fig == None or ax == None:
         fig, ax = plt.subplots()
      # Plot all terms
      for term in self.terms:
         fig, ax = term.xplot(x, fig, ax)
      ax.set_ylabel(self.name)
      ax.legend()
      return [fig, ax]
   def yplot(self, y, fig = None, ax = None):
      # New figure and axes if none provided
      if fig == None or ax == None:
         fig, ax = plt.subplots()
      # Plot all terms
      for term in self.terms:
         fig, ax = term.yplot(y, fig, ax)
      ax.set_ylabel(self.name)
      ax.legend()
      return [fig, ax]
   def ijval(self, i, j):
      return np.array([term.ijval(i,j) for term in self.terms])
   def xyval(self, x, y):
      return np.array([term.xyval(x,y) for term in self.terms])
   # Pie chart of the budget
   def pie(self, array, fig = None, ax = None):
      # Sort given labels and values
      tmptype = [('label', '<U32'), ('val', np.float)]
      data = np.sort(np.array(array, dtype=tmptype), order='val')
      # Get sum(abs()) for scaling
      scaling = np.sum(np.abs([dat[1] for dat in data]))
      # Rescale
      data2 = [(dat[0], np.abs(dat[1])/scaling) for dat in data]
      # Extract labels, values and explode error
      labels = [dat[0] for dat in data2]
      values = [dat[1] for dat in data2]
      explode = np.array([label=="Error" for label in labels])*0.15
      # New figure and axes if none provided
      if fig == None or ax == None:
         fig, ax = plt.subplots()
      ax.pie(values, labels=labels, explode=explode, autopct='%1.1f%%', pctdistance=0.8, startangle=90.)
      ax.set_title("Left: negative contributions. Right: positive contributions.")
      return fig, ax
   # Pie chart of the budget at given location (i, j)
   def ijpie(self, i, j, fig = None, ax = None):
      # Plot
      fig, ax = self.pie([(term.name, term.ijval(i,j)) for term in self.terms], fig, ax)
      # Add suptitle
      fig.suptitle(np.str(self.name) + " at (i,j)=(" + np.str(i) + "," + np.str(j) + ").")
      return fig, ax
   # Pie chart of the budget at given location (x,y)
   def xypie(self, x, y, fig = None, ax = None):
      # Plot
      fig, ax = self.pie([(term.name, term.xyval(x,y)) for term in self.terms], fig, ax)
      # Locate (x,y) and add suptitle
      i = np.where(np.abs(self.case.xx-x) == np.amin(np.abs(self.case.xx-x)))[0][0]
      j = np.where(np.abs(self.case.yy-y) == np.amin(np.abs(self.case.yy-y)))[0][0]
      fig.suptitle(np.str(self.name) + " at (x,y)=(" + np.str(self.case.xx[i]) + "," + np.str(self.case.yy[j]) + ").")
      return fig, ax
   #
   # Add basic and detailed description
   #
   def __repr__(self):
      return self.config
   def __str__(self):
      return np.str(self.case) + "\n" \
             "Setup of the budget :" + "\n" \
             "   Config file : " + self.config + "\n" \
             "   Name : " + self.name + "\n" \
             "   nterms : " + np.str(self.nterms)

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
      ax.plot(qty.case.yy, qty.data[i,:], qty.clr, \
                                          label=qty.name, \
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
      ax.plot(qty.case.xx, qty.data[:,j], qty.clr, \
                                          label=qty.name, \
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


