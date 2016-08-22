===========
Project: just_another_Bfactor
===========

The aim of this project is to use a attribute file, see examples, 
to colour a protein in pymol.

Currently the main function can be used from the pymol 
command line as follows 

> fetch 5k9p
> ColourAtri path/examples/Attribute_file.txt

License information can be found in LICENSE.txt
If you have an issue please report it at zcbtla0@ucl.ac.uk

Install
===========

1) install the python module

python setup.py build
python setup.py install

2) install Just_Another_BFactor_plugin.py as a pymol plugin 
	i)    Plugin > Plugin Manager
	ii)   Install New Plugin > Choose file 
	iii)  Navigate to Just_Another_BFactor_plugin.py > open

author
Lucas Siemons

