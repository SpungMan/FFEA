# 
#  This file is part of the FFEA simulation package
#  
#  Copyright (c) by the Theory and Development FFEA teams,
#  as they appear in the README.md file. 
# 
#  FFEA is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  FFEA is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with FFEA.  If not, see <http://www.gnu.org/licenses/>.
# 
#  To help us fund FFEA development, we humbly ask that you cite 
#  the research papers on the package.
#

from os import path
from time import sleep
import numpy as np

class FFEA_kinetic_rates:

	def __init__(self, fname = "", frame = 0):
	
		self.reset()

		try:
			self.load(fname)
		except:
			return

	def load(self, fname, findex = 0):

		print("Loading FFEA kinetic rates file...")

		# Test file exists
		if not path.exists(fname):
			print("\tFile '" + fname + "' not found.")
	
		# File format?
		base, ext = path.splitext(fname)
		if ext == ".rates":
			try:
				self.load_rates(fname)
			except:
				print("\tUnable to load FFEA_kinetic_rates from " + fname + ". Returning empty object...")

		else:
			print("\tUnrecognised file extension '" + ext + "'.")

	def load_rates(self, fname):

		# Open file
		try:
			fin = open(fname, "r")
		except(IOError):
			print("\tFile '" + fname + "' not found.")
			self.reset()
			raise

		# Test format
		line = fin.readline().strip()
		if line != "ffea kinetic rates file" and line != "walrus kinetic rates file":
			print("\tExpected 'ffea kinetic rates file' but found " + line)
			raise TypeError

		num_states = int(fin.readline().split()[1])

		fin.readline()

		# Read rates now
		while(True):
			sline = fin.readline().split()
			if len(sline) == 0:
				break

			# Get some rates (in matrix form)
			rate = [float(s) for s in sline]
			self.rate.append(rate)

		fin.close()
		self.num_states = len(self.rate)

		# Numpy it up, for speed
		self.rate = np.array(self.rate)

	def add_node(self, n, nodetype = 0):

		self.pos.append(n)
		self.num_nodes += 1
		
		if nodetype == 0:
			self.num_surface_nodes += 1
		else:
			self.num_interior_nodes += 1
		
	def print_details(self):

		print("num_states = %d" % (self.num_states))
		sleep(1)


		print("Rates:\n")
		outline = ""
		for i in range(self.num_states):
			
			outline += "\t\t" + str(i)

		print(outline)

		for i in range(self.num_states):
			outline = str(i) + "\t"
			for j in range(self.num_states):
				outline += "%6.3e\t" % (self.rate[i][j])

			print(outline)
	
	def reset(self):

		self.num_states = 0
		self.rate = []
