import sys, os
import numpy as np
import FFEA_topology

if len(sys.argv) != 5:
	sys.exit("Usage: python " + sys.argv[0] + " [INPUT .pcz file] [INPUT reference topology (_frame0.pdb)] [num_animations] [ffea scale]")

inpcz = sys.argv[1]
inref = sys.argv[2]
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
num_anim = int(sys.argv[3])
anim_basename = inpcz.split(".")[0]
ffea_scale = float(sys.argv[4])

# Get number of nodes for FFEA_stuff
print("Calculating Eigenvector Animations...")
for i in range(num_anim):
	anim_outfname = anim_basename + "_anim" + str(i) + ".pdb"
	anim_outfname_ffea = anim_basename + "_anim" + str(i) + ".out"
	print("\tEigenvector " + str(i) + ": Writing to " + os.path.splitext(os.path.basename(anim_outfname))[0] + ".pdb/.out ...")
	os.system("pyPczdump -i " + inpcz + " -m " + str(i) + " --pdb " + inref + " -o " + anim_outfname)
	os.system("python " + script_dir + "/../../FFEA_initialise/PDB_tools/PDB_convert_to_FFEA_trajectory/PDB_convert_to_FFEA_trajectory.py " + anim_outfname + " " + anim_outfname_ffea + " " + str(ffea_scale))
	print("\tdone!")
print("done!")