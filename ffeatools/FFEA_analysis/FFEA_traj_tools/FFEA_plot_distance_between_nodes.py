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

import sys, os
import FFEA_trajectory
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 4:
	sys.exit("Usage: python FFEA_plot_distance_between_nodes.py [INPUT trajectory (.out)] [Node 1] [Node 2]")
	
# Get args
trajfname = sys.argv[1]
node_index = [int(sys.argv[2]), int(sys.argv[3])]

# Open trajectory
traj = FFEA_trajectory.FFEA_trajectory(trajfname)

# Get some node position arrays
xsep = []
ysep = []
zsep = []
abssep = []

step = range(traj.num_frames)

for f in traj.blob[0][0].frame:
	r = f.pos[node_index[1]] - f.pos[node_index[0]]
	xsep.append(r[0])
	ysep.append(r[1])
	zsep.append(r[2])
	
	abssep.append(np.linalg.norm(r))
	
# Convert to numpy
xsep = np.array(xsep)
ysep = np.array(ysep)
zsep = np.array(zsep)
abssep = np.array(abssep)

# Plot stuff
plt.plot(step, abssep)
plt.ylabel("Distance (m)")
plt.xlabel("Frame")
plt.title("Node " + str(node_index[0]) + " to node " + str(node_index[1]) + " distance trajectory")
plt.show()
plt.savefig("output.png")
	