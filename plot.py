#! /usr/bin/env python3

# Import various modules
import argparse
import numpy as np
import matplotlib.pyplot as plt
from os.path import join as opjoin

# Import local modules from the file module.py in the current directory
from module import *

# Small function to show and / or save a Figure
def show_and_save(fig, name):
   if args.show:
      fig.show()
   if args.save:
      fig.savefig(opjoin(case.figfolder, name+".png"))

# Small function to plot and extract values for a given budget / quantity
def plot_and_save(qty, name):
   if args.x:
      for x in args.x:
         fig, ax = qty.xplot(x)
         show_and_save(fig, name[:-4]+"_xplot_x_"+np.str(x))
   if args.y:
      for y in args.y:
         fig, ax = qty.yplot(y)
         show_and_save(fig, name[:-4]+"_yplot_y_"+np.str(y))
   if args.i:
      for i in args.i:
         fig, ax = qty.iplot(i)
         show_and_save(fig, name[:-4]+"_iplot_i_"+np.str(i))
   if args.j:
      for j in args.j:
         fig, ax = qty.jplot(j)
         show_and_save(fig, name[:-4]+"_jplot_j_"+np.str(j))
   if args.xyval:
      print(name[:-4] + ", xyval: " + np.str(qty.xyval(args.xyval[0], args.xyval[1])))
   if args.ijval:
      print(name[:-4] + ", ijval: " + np.str(qty.ijval(args.ijval[0], args.ijval[1])))

# Define and read arguments for the script
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("--show", help="Show figures", action="store_true")
parser.add_argument("--save", help="Save figures", action="store_true")
parser.add_argument("-c", "--case", help="Parameter file for the case")
parser.add_argument("-b", "--budget", nargs='+', help="Parameter file(s) for each budget to process")
parser.add_argument("-q", "--quantity", nargs='+', help="Parameter file(s) for each quantity to process")
parser.add_argument("-x", "--x", nargs='+', type=float, help="Plot budgets / quantities at given x location(s)")
parser.add_argument("-y", "--y", nargs='+', type=float, help="Plot budgets / quantities at given y location(s)")
parser.add_argument("-i", "--i", nargs='+', type=int, help="Plot budgets / quantities at given i location(s)")
parser.add_argument("-j", "--j", nargs='+', type=int, help="Plot budgets / quantities at given j location(s)")
parser.add_argument("-xyv", "--xyval", nargs=2, type=float, help="Print budgets / quantities values at given x,y location")
parser.add_argument("-ijv", "--ijval", nargs=2, type=int, help="Print budgets / quantities values at given i,j location")
parser.add_argument("-xyp", "--xypie", nargs=2, type=float, help="Plot budgets pie chart at given x,y location")
parser.add_argument("-ijp", "--ijpie", nargs=2, type=int, help="Plot budgets pie chart at given i,j location")
args = parser.parse_args()

# User must provide the case parameter file
if not args.case:
   print("Error: a case parameter file must be provided.")

# User must provide at least one quantity or budget
if not (args.budget or args.quantity):
   print("Error: at least one quantity or budget must be provided.")

# Print in case of verbosity
if args.verbose:
   print("\n")
   print("Script designed to extract and plot turbulent quantities.")
   print("Verbose turned on")
   print("Parameter file for the case: " + args.case)
   if args.budget:
      print("Provided budget file(s): " + np.str(args.budget))
   else:
      print("No budget file provided")
   if args.quantity:
      print("Provided quantity file(s): " + np.str(args.quantity))
   else:
      print("No quantity file provided")
   if args.x:
      print("Plot Y profiles at provided positions x : " + np.str(args.x))
   if args.y:
      print("Plot X profiles at provided positions y : " + np.str(args.y))
   if args.i:
      print("Plot Y profiles at provided grid nodes i : " + np.str(args.i))
   if args.y:
      print("Plot X profiles at provided grid nodes j : " + np.str(args.j))
   if args.xyval:
      print("Extract values at position (x,y) : " + np.str(args.xyval))
   if args.ijval:
      print("Extract values at node (i,j) : " + np.str(args.ijval))
   if args.budget and args.xypie:
      print("Plot budget pie chart at position (x,y) : " + np.str(args.xypie))
   if args.budget and args.ijpie:
      print("Plot budget pie chart at node (i,j) : " + np.str(args.ijpie))
   print("\n")

# Load the case
case = setup(args.case)

# Process the provided budget(s):
if args.budget:
   if args.verbose:
      print("Number of budget(s): " + np.str(len(args.budget)))
   for sbud in args.budget:
      if args.verbose:
         print("   Processing " + sbud)
      bud = budget(case, sbud)
      # Plot profiles and extract values
      plot_and_save(bud, sbud)
      # Plot pie chart
      if args.xypie:
         fig, ax = bud.xypie(args.xypie[0], args.xypie[1])
         show_and_save(fig, sbud[:-4]+"_xypie_x_"+np.str(args.xypie[0])+"_y_"+np.str(args.xypie[1]))
      if args.ijpie:
         fig, ax = bud.ijpie(args.ijpie[0], args.ijpie[1])
         show_and_save(fig, sbud[:-4]+"_ijpie_i_"+np.str(args.xypie[0])+"_j_"+np.str(args.xypie[1]))

# Process the provided quantitie(s):
if args.quantity:
   if args.verbose:
      print("Number of quantitie(s): " + np.str(len(args.quantity)))
   for sqty in args.quantity:
      if args.verbose:
         print("   Processing " + sqty)
      qty = quantity(case, sqty)
      # Plot profiles and extract values
      plot_and_save(qty, sqty)

# Wait for input at the end
if args.show:
   print("Input some random text to close all figures")
   input()
