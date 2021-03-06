Visualising FFEA {#FFEAviewertut}
=============================

## Installation

The FFEA viewer is available as a plugin for the [PyMOL molecular graphics system](https://www.pymol.org/). It requires PyMOL 1.6.x or above, and Python 2.6.x or above.

After installing FFEA, the plugin ` FFEAplugin.tar.gz ` will be found in ` $FFEA_HOME/share/ffea/plugins/pymol `.
 (If that were not the case, the files can be found under the build folder in `/ffeatools/analysis/pymol_plugin`. 
 One would need then to add this folder to a .zip or tar.gz archive).
 In order to install the plugin, 
  open PyMOL, and click 'Plugin' on the top menu bar, then 'Plugin Manager'. Select the 'install new plugin' tab, and click 'choose file'. Then, locate the .tar.gz archive.

![Installing the PyMOL viewer plugin](viewer_1_installation_II.png "Installing the PyMOL viewer plugin")

<!-- If you encounter frequent PyMOL crashes or ominous warnings on the console such as `main thread is not in main loop` or `Tcl_AsyncDelete: async handler deleted by the wrong thread`, you may want to install the thread safe version of Tkinter, called [mtTkinter](http://tkinter.unpythonic.net/wiki/mtTkinter). --> 

## Loading your system

When PyMOL loads, open the ` Plugin ` menu, and you should see a new option called
  `FFEA loader`. This has a file menu that will allow you to select an FFEA script
  and load the FFEA script file, but before doing that, review the options.
  Currently, the model needs to be reloaded every time these settings are changed.

![FFEA Viewer settings](viewer_2_settings_IV.png "FFEA Viewer settings")

The FFEA viewer settings are:
* ` System name `: arbitrary, used to identify the system in the PyMOL sidebar.
* ` Display `: displays spring objects and pinned nodes if checked.
* ` Show solid `:
  * ` Plain solid ` renders the mesh in flat colours.
  * ` Density ` colours the mesh different depending its density, as read in the material file. 
  * ` Shear Viscosity ` colours the mesh different depending its shear viscosity, as read in the material file. 
  * ` Bulk Viscosity ` colours the mesh different depending its bulk viscosity, as read in the material file. 
  * ` Shear Modulus ` colours the mesh different depending its shear modulus, as read in the material file. 
  * ` Bulk Modulus ` colours the mesh different depending its bulk modulus, as read in the material file. 
  * ` VdW ` colours the mesh different depending the van der Waals face type of the faces, as read in the vdw file. 
  * ` No Solid ` does not display a solid mesh.
* ` Show Mesh `:
  * ` Surface Mesh ` renders a wire-frame of the surface.
  * ` Whole Mesh ` renders a wire frame that includes the internal elements.
  * ` No mesh ` does not display a wire frame mesh.
* ` Show Indices `: displays the indices as labels. Alternatively, one could use ` Add Atoms `.
  * ` Node Indices ` displays the indices of all the nodes, including the 2nd-order nodes.
  * ` Node Indices (Linear)` only displays the indices of the linear elements. In most cases, this is more useful, as displaying second-order nodes can make the image hard to read.
  * ` Element Indices ` displays the indices of the elements.
  * ` Face Indices ` displays the indices of the faces (surface elements) only.
  * ` No indices ` does not display indices.
* ` Show Box `:
  * ` Simulation Box (outline) ` draws an outline of the simulation box - the simulation box is the volume which objects in the simulation can occupy.
  * ` Simulation Box (whole)`  draws the entire box.
  * ` No Box ` will draw no box. 
* ` Load `:
  * ` Trajectory ` is the loading type to use if you have a finished trajectory (.ftj file) that has been generated by the runner. It will load each frame of the trajectory into PyMOL. If the trajectory is not found the system will be loaded (into box).
  * ` System (Into box)` will load the starting state of the system, and it will show how the system will be initialised relative to the box. It can be used to check the size of your molecule(s) compared to the simulation box and check that their position is correct.
  * ` System (Plainly) ` will load the system plainly, using the same coordinates that appear in the `.node` file, rotating and translating according to keywords `rotation` and `translation`, but not centering the system onto the simulation box.
  Depending on the way the models have been generated, 
  this may be the best way to visualise the models before starting the simulation. This is specially useful when 
  checking that the model has been set up correctly, as one can load the FFEA system alongside a (number of) PDB file(s),
  thus checking that both share origin and scale.
  * ` CGO  ` will load the trajectory and cache the calls to PyMOL's API directly to the hard drive. This results in a slower initial load, but faster subsequent loads.
<!-- * Clicking the ` Add node pseudoatoms ` button after the simulation is loaded will cause PyMOL to load a pseudoatom at the location of each node. Pseudoatoms can be targeted by all of PyMOL's regular analysis tools. For example, you can type `label all, name` into the PyMOL console. -->
* ` Add Atoms `: will add create a PyMOL object, or molecule, with a number of CA atoms.
  * ` None ` does not load anything
  * ` Onto Linear Nodes ` will add atoms on every first order node, where PyMOL attribute ` resi ` will match the corresponding FFEA node number. 
  * ` Onto Nodes ` will add atoms on every node, where PyMOL attribute ` resi ` will match the corresponding FFEA node number. 
  * ` Onto Faces ` will add atoms on every face, where PyMOL attributes ` resi ` will match the corresponding FFEA face number.
      Notice that FFEA uses second order faces in 
  [short range forces](\ref shortRange), and so one will find 4 nodes on every 
    triangle if loads ` Whole Mesh ` (but only one if loading ` Surface Mesh `). 
  * ` Onto Elements ` will add atoms at the centre of every element, where PyMOL attribute ` resi ` will match the corresponding FFEA node number. 

## Viewing models

![FFEA viewer interface](viewer_3_interface_II.png "FFEA viewer interface")

The PyMOL viewer interface is relatively straightforward. A list of loaded objects appears on the right-hand side. The 'action' menu (A) allows you to rename, centre and delete objects. The S, H and L menus let you show, hide and label elements that only appear on other formats. The C button allows you to recolour the object. Clicking on the objects name shows and hides that object. At the bottom-right, there are camera controls, and playback controls.

## Exporting images and videos

To export a still image, click the file menu, and click ` Save Image As `. For higher-quality images, you may wish to resize the viewport, as images are exported at the same resolution they are displayed  Also consider right-clicking the viewing area and clicking ` ray `, which will generate a (higher-quality) ray-traced frame.

PyMOL does not export videos by default, although installing the FreeMOL addons and an MPEG encoder will all you to do so.

To get higher-quality videos in a more modern format, select `File`->`Save Movie As `->`PNG Images`. This will save each frame as a still image, organised by file name. For example, saving with the file name 'test' for a 100-frame trajectory will produce 100 PNG files, called `test0001.png` to `test0100.png`.

To stitch these together into a video, you can use ffmpeg, a command-line tool. Install ffmpeg and call it using the following arguments:

	ffmpeg -r 60 -i name%04d.png -c:v libx264 -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" out.mp4

The arguments are
* `-r`, the framerate
* `-i`, the input. The `%04d` means that FFMpeg will compile together any frames matching that format (e.g. `name0001.png`, `name0002.png`).
* `-c:v`, the codec
* `-pix_fmt`, the pixel format
* -`vf`, user-configurable filter. PyMOL can often output files with very awkward dimensions, which are hard to encode - this filter fixes that.

Finally, the output file name is a positional argument.

