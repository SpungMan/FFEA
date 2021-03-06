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
import FFEA_pdb, FFEA_traj, FFEA_kinetic_map
import time

if len(sys.argv) != 6:
	sys.exit("Usage python [INPUT FFEA .traj fname] [INPUT original .pdb fname] [OUTPUT .pdb fname] [Traj to PDB .map (sparse)] [scale]")

# Get args
trajfname = sys.argv[1]
ipdbfname = sys.argv[2]
opdbfname = sys.argv[3]
sparsemapfname = sys.argv[4]
scale = float(sys.argv[5])

# Open up stuff
traj = FFEA_traj.FFEA_traj(trajfname, 1000, 0, 999, 1)
ipdb = FFEA_pdb.FFEA_pdb(ipdbfname)
ipdb.scale(scale)

opdb = []
sparsemap = FFEA_kinetic_map.FFEA_kinetic_map(sparsemapfname)
#densemap = FFEA_kinetic_map.FFEA_kinetic_map(sparsemapfname)

# Update frames 1 by 1 by applying map to the FFEA_trajectory
for i in range(traj.num_frames):
	if traj.num_frames > 10:
		if i % 10 == 0:
			print "Converted %d frames out of %d" % (i, traj.num_frames)
	#start = time.clock()
	frame = sparsemap.apply_to_traj_frame(traj.blob[0][0].frame[i])
	#print "Applying map took %fs" % (time.clock() - start)
	#frame = densemap.apply_to_traj_frame(traj.blob[0][0].frame[i])
	#start = time.clock()
	opdb.append(frame.convert_to_pdb(ipdb, 1.0 / scale))
	#print "Converting frame took %fs" % (time.clock() - start)
FFEA_pdb.write_frames_to_file(opdb, opdbfname)
	


