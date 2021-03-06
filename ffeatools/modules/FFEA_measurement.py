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

import sys
from os import path
import numpy as np

# MatPlotLib conflicts with PyMOL horribly:
plt = False
modules = sys.modules.keys()
if not "pymol" in modules:
  try:
    import matplotlib.pyplot as plt
  except:
    pass
else:
  print("FFEA_measurement will not load matplotlib, as it conflicts with PyMOL")

class FFEA_measurement:

	def __init__(self, fname = "", frame_rate = 1, num_frames_to_read = 1000000):

		self.reset()

		# Return empty object if fname not initialised
		if fname == "" or fname == None:
			self.valid = True
			sys.stdout.write("done! Empty object initialised.\n")
			return

		# Test what type of file it is
		if not path.exists(fname):
			print("\tFile '" + fname + "' not found.")
			raise IOError
		
		fin = open(fname, "r")
		line = fin.readline().strip()
		fin.close()
		try:
			if line == "FFEA Global Measurement File":
				self.load_global(fname, frame_rate = frame_rate, num_frames_to_read = num_frames_to_read)
			else:		
				print("\tPlease supply us with the global measurement file, not the '-d' .fdm file")				
				return

			# Get num frames for quick access
			self.num_frames = len(self.global_meas["Time"])

			dfname = path.splitext(fname)[0] + ".fdm"
			if path.exists(dfname):
				self.load_detailed(dfname, frame_rate = frame_rate, num_frames_to_read = num_frames_to_read)
			
		except:
			raise
	
		self.valid = True
		self.empty = False
		sys.stdout.write("done!\n")

	def load_global(self, fname, frame_rate = 1, num_frames_to_read = 1000000):

		print("Loading FFEA Global Measurement file...")
	
		# Open file
		try:
			fin = open(fname, "r")
		except(IOError):
			print("\tFile '" + fname + "' not found.")
			self.reset()
			raise
		
		# Details first
		line = fin.readline()
		while(line.strip() != "Simulation Details:"):	
			line = fin.readline()

		while(line.strip() != "Parameters:"):
			self.detail_string += line
			line = fin.readline()

		# Now params
		while(line.strip() != "Measurements:"):
			if "num_blobs" in line:
				self.num_blobs = int(line.split("=")[1])

			self.param_string += line
			line = fin.readline()

		# Build a dictionary of possible variables and a map to those
		self.global_meas = {'Time': None, 'KineticEnergy': None, 'StrainEnergy': None, 'SpringEnergy': None, 'VdWEnergy': None, 'PreCompEnergy': None, 'Centroid.x': None, 'Centroid.y': None, 'Centroid.z': None, 'Centroid': None, 'RMSD': None}
		sline = fin.readline().strip().split()
		measmap = ["" for i in range(len(sline))]		
		i = -1
		for title in sline:
			i += 1
			measmap[i] = title.strip()
			self.global_meas[measmap[i]] = []

		num_meas = len(measmap)

		# Read measurements
		line = fin.readline()
		frames_read = 0
		all_frames = 0
		while(line != "" and all_frames < num_frames_to_read):
			#print(all_frames, num_frames_to_read)
			if line.strip() == "#==RESTART==":
				line = fin.readline()
				continue

			if all_frames % frame_rate == 0:
				sline = line.split()
				for i in range(num_meas):
					self.global_meas[measmap[i]].append(float(sline[i]))
				frames_read += 1

			line = fin.readline()
			all_frames += 1

			sys.stdout.write("\rFrames read = %d, Frames skipped = %d" % (frames_read, all_frames - frames_read))
			sys.stdout.flush()

		print("\ndone! Successfully read " + str(frames_read) + " frame/s from '" + fname + "'.")

		# Move centroid into more useful format
		self.global_meas["Centroid"] = []
		for i in range(len(self.global_meas['Time'])):
			self.global_meas["Centroid"].append([self.global_meas["Centroid.x"][i], self.global_meas["Centroid.y"][i], self.global_meas["Centroid.z"][i]])

		del self.global_meas["Centroid.x"]
		del self.global_meas["Centroid.y"]
		del self.global_meas["Centroid.z"]
	
		for key in self.global_meas:
			if self.global_meas[key] != None:
				self.global_meas[key] = np.array(self.global_meas[key])

	def load_detailed(self, fname, frame_rate = 1, num_frames_to_read = 1000000):

		print("Loading FFEA Detailed Measurement file...")
	
		# Open file
		try:
			fin = open(fname, "r")
		except(IOError):
			print("\tFile '" + fname + "' not found.")
			self.reset()
			raise

		line = fin.readline().strip()
		while(line != "Measurements:"):
			line = fin.readline().strip()

		# Get column title line and build maps to the required stuff
		line = fin.readline()
		sline = line.split("|")[1:]
		localsline = sline[:self.num_blobs]
		globalsline = sline[self.num_blobs:]

		# Build dictionaries ans maps to variables
		
		# Local to blobs first
		# Initialise arrays (measmap and indexmap are of unknown length initially)
		self.blob_meas = [{'KineticEnergy': None, 'StrainEnergy': None, 'Centroid.x': None, 'Centroid.y': None, 'Centroid.z': None, 'Centroid': None, 'RMSD': None} for i in range(self.num_blobs)]
		indexmap = []
		measmap = []

		for i in range(self.num_blobs):
			ssline = localsline[i].split()[1:]
			for title in ssline:
				indexmap.append(i)
				measmap.append(title.strip())
				self.blob_meas[i][title.strip()] = []

		# Now the global one
		# Initialise arrays
		self.interblob_meas = [[{"VdWEnergy": None, "SpringEnergy": None, "PreCompEnergy": None} for i in range(self.num_blobs)] for j in range(self.num_blobs)]
		iindexmap = []
		imeasmap = []

		for i in range(len(globalsline)):

			# Get the pair of indices
			ssline = globalsline[i].split()
			indexpair = [int(j) for j in ssline[0][1:].split("B")]
			ssline = ssline[1:]
			for title in ssline:
				iindexmap.append(indexpair)
				imeasmap.append(title.strip())
				self.interblob_meas[indexpair[0]][indexpair[1]][title.strip()] = []

		# Now, read measurements and fill the relevent arrays
		line = fin.readline()
		frames_read = 0
		all_frames = 0
		while(line != "" and all_frames < num_frames_to_read):
			if line.strip() == "#==RESTART==":
				line = fin.readline()
				continue

			if all_frames % frame_rate == 0:

				sline = line.split()[1:]

				localsline = sline[:len(indexmap)]
				globalsline = sline[len(indexmap):]

				# Local to blobs first!
				for i in range(len(localsline)):
					self.blob_meas[indexmap[i]][measmap[i]].append(float(localsline[i]))

				# Now global
				for i in range(len(globalsline)):
					self.interblob_meas[iindexmap[i][0]][iindexmap[i][1]][imeasmap[i]].append(float(globalsline[i]))
				frames_read += 1

			line = fin.readline()
			all_frames += 1

			sys.stdout.write("\rFrames read = %d, Frames skipped = %d" % (frames_read, all_frames - frames_read))
			sys.stdout.flush()

		print("\ndone! Successfully read " + str(frames_read) + " frame/s from '" + fname + "'.")

		# Move centroid into more useful format, make interblob array symmetric and turn stuff to numpy
		for i in range(self.num_blobs):
			self.blob_meas[i]["Centroid"] = []

			for j in range(len(self.global_meas['Time'])):
				self.blob_meas[i]["Centroid"].append([self.blob_meas[i]["Centroid.x"][j], self.blob_meas[i]["Centroid.y"][j], self.blob_meas[i]["Centroid.z"][j]])

			del self.blob_meas[i]["Centroid.x"]
			del self.blob_meas[i]["Centroid.y"]
			del self.blob_meas[i]["Centroid.z"]

			for key in self.blob_meas[i]:
				if self.blob_meas[i][key] != None:
					self.blob_meas[i][key] = np.array(self.blob_meas[i][key])

			for j in range(i, self.num_blobs):
				for key in self.interblob_meas[i][j]:
					if self.interblob_meas[i][j][key] != None:
						self.interblob_meas[i][j][key] = np.array(self.interblob_meas[i][j][key])
				self.interblob_meas[j][i] = self.interblob_meas[i][j]


	def add_empty_blob(self):
		
		if self.global_meas == None:
			self.global_meas = self.global_meas = {'Time': None, 'KineticEnergy': None, 'StrainEnergy': None, 'SpringEnergy': None, 'VdWEnergy': None, 'PreCompEnergy': None, 'Centroid.x': None, 'Centroid.y': None, 'Centroid.z': None, 'Centroid': None, 'RMSD': None}
		self.blob_meas.append({'KineticEnergy': None, 'StrainEnergy': None, 'Centroid.x': None, 'Centroid.y': None, 'Centroid.z': None, 'Centroid': None, 'RMSD': None})
		for i in range(self.num_blobs):
			self.interblob_meas[i].append([{"VdWEnergy": None, "SpringEnergy": None, "PreCompEnergy": None}])
		self.interblob_meas.append([{"VdWEnergy": None, "SpringEnergy": None, "PreCompEnergy": None} for i in range(self.num_blobs + 1)])
		self.num_blobs += 1

	def write_to_file(self, fname, script = None):

		# Get filenames first
		globalfname = fname
		blobfname = path.splitext(fname)[0] + ".fdm"

		print("Writing Measurements to file:\n\tGlobal Will be written to %s" % (globalfname))
		if self.blob_meas != []:
			print("\tDetailed will be written to %s\n" % (blobfname))


		#
		# Global first
		#
		
		fout = open(globalfname, "w")
		fout.write("FFEA Global Measurement File\n\nSimulation Details:\n")
		#fout.write("\tSimulation Began on %d/%d/%d at %d:%d:%d\n" % (self.date[0],self.date[1], self.date[2], self.time[0], self.time[1], self.time[2]))
		#fout.write("\tScript Filename = %s\n" % (self.script_fname))
		#fout.write("\tSimulation Type = %s\n\n" % (self.simtype))
		fout.write(self.detail_string)
		fout.write("Parameters:\n")

		# Params, maybe		
		#if script != None:
		#	script.params.write_to_file(fout, self.script_fname)
		fout.write(self.param_string)
			
		#
		# Measurements
		#

		# These params are written in the same order as they are written out in the main code. They don't have to be for this module to work, but consistency is nice
		# Rough fix to test for None in numpy arrays
		keys_to_write = ["Time"]
		try:
			if self.global_meas["KineticEnergy"] != None:
				keys_to_write.append("KineticEnergy")
		except(ValueError):
			keys_to_write.append("KineticEnergy")

		keys_to_write.append("StrainEnergy")
		keys_to_write.append("Centroid")
		keys_to_write.append("RMSD")

		try:
			if self.global_meas["SpringEnergy"] != None:
				keys_to_write.append("SpringEnergy")
		except(ValueError):
			keys_to_write.append("SpringEnergy")

		try:
			if self.global_meas["VdWEnergy"] != None:
				keys_to_write.append("VdWEnergy")
		except(ValueError):
			keys_to_write.append("VdWEnergy")

		try:
			if self.global_meas["PreCompEnergy"] != None:
				keys_to_write.append("PreCompEnergy")
		except(ValueError):
			keys_to_write.append("PreCompEnergy")

		fout.write("Measurements:\n")
		for key in keys_to_write:
			if key == "Centroid":
				fout.write("%-14s%-14s%-14s" % ("Centroid.x", "Centroid.y", "Centroid.z"))
			else:
				fout.write("%-14s" % (key))
		fout.write("\n")
		for i in range(self.num_frames):
			for key in keys_to_write:
				if key == "Centroid":
					fout.write("%-14.6e%-14.6e%-14.6e" % (self.global_meas[key][i][0],self.global_meas[key][i][1], self.global_meas[key][i][2]))
				else:
					fout.write("%-14.6e" % (self.global_meas[key][i]))
			fout.write("\n")
		fout.close()
		
		#
		# Now detailed bit
		#

		if self.blob_meas != []:
			fout = open(blobfname, "w")
			fout.write("FFEA Detailed Measurement File\n\nMeasurements:\n")

			# We need a keys_to_write for each blob (might be able to make these triangular arrays in future)
			keys_to_write = [[] for i in range(self.num_blobs)]
			pair_keys_to_write = [[[] for j in range(self.num_blobs)] for i in range(self.num_blobs)]
			do_interblob = [[False for j in range(self.num_blobs)] for i in range(self.num_blobs)]
			for i in range(self.num_blobs):
				try:
					if self.blob_meas[i]["KineticEnergy"] != None:
						keys_to_write[i].append("KineticEnergy")
				except(ValueError):
					keys_to_write[i].append("KineticEnergy")
	
				keys_to_write[i].append("StrainEnergy")
				keys_to_write[i].append("Centroid")
				keys_to_write[i].append("RMSD")
				for j in range(i, self.num_blobs):

					try:
						if self.interblob_meas[i][j]["VdWEnergy"] != None:
							pair_keys_to_write[i][j].append("VdWEnergy")
					except(ValueError):
						pair_keys_to_write[i][j].append("VdWEnergy")
					except(KeyError):
						pass

					try:
						if self.interblob_meas[i][j]["SpringEnergy"] != None:
							pair_keys_to_write[i][j].append("SpringEnergy")
					except(ValueError):
						pair_keys_to_write[i][j].append("SpringEnergy")
					except(KeyError):
						pass
					try:
						if self.interblob_meas[i][j]["PreCompEnergy"] != None:
							pair_keys_to_write[i][j].append("PreCompEnergy")
					except(ValueError):
						pair_keys_to_write[i][j].append("PreCompEnergy")
					except(KeyError):
						pass
		

			# Time first
			fout.write("%-14s" % ("Time"))
		
			# Then local to blobs
			for i in range(self.num_blobs):
				fout.write("| B%d " % (i))
				for key in keys_to_write[i]:
					if key == "Centroid":
						fout.write("%-14s%-14s%-14s" % ("Centroid.x", "Centroid.y", "Centroid.z"))
					else:
						fout.write("%-14s" % (key))

			# Then interblob stuff
			if do_interblob:
				for i in range(self.num_blobs):
					for j in range(i, self.num_blobs):
						if do_interblob[i][j]:
							fout.write("| B%dB%d " % (i, j))
							for key in pair_keys_to_write[i][j]:
								fout.write("%-14s" % (key))
			fout.write("\n")

			for i in range(self.num_frames):
				fout.write("%-14.6e" % (self.global_meas["Time"][i]))
				for j in range(self.num_blobs):
					fout.write("     ")
					for key in keys_to_write[j]:
						if key == "Centroid":
							fout.write("%-14.6e%-14.6e%-14.6e" % (self.blob_meas[j][key][i][0],self.blob_meas[j][key][i][1], self.blob_meas[j][key][i][2]))
						else:
							fout.write("%-14.6e" % (self.blob_meas[j][key][i]))

				for j in range(self.num_blobs):
					for k in range(j, self.num_blobs):
						if do_interblob[j][k]:
							fout.write("       ")
							for key in pair_keys_to_write[j][k]:
								fout.write("%-14.6e" % (self.interblob_meas[j][k][key][i]))
				fout.write("\n")

			fout.close()

	def reset(self):
		self.valid = False
		self.empty = True
		self.detail_string = ""
		self.param_string = ""	# Use this in future perhaps? Just store for now
		self.num_blobs = 0
		self.num_frames = 0
		self.global_meas = None
		self.blob_meas = []
		self.interblob_meas = []
