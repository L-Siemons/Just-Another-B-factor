
import sys
from pymol import cmd
from just_another_Bfactor import file_utils as fu
from just_another_Bfactor import prot_classes as prot
import math
import numpy as np
import pkg_resources
from just_another_Bfactor import Main_functions as M


# -----------------------------------------------------------
# Colour section 
# -----------------------------------------------------------

#this function colours the structure according to the atri        
cmd.extend("ColourAtri", M.ColourAtri)

#this gives the atribute a name
def ColourNames(file, first_col=4):

    '''
    
    This function is for the user to see what titles were given in the 
    Atribute file for the colour atributes. 
    
    File is the atribute file
    first col is the coloumn of the first defines atribute.
    
    Note that this creates bonds in the models in order to create the sticks
    
    '''

    prot_atri = prot.protein_atri(file)
    names = prot_atri.record_names
    print 'col     Atribute'
    col = first_col 
    for i in names:
        print col, '   ', i 
        col = col + 1
    
cmd.extend("CAtriNames", ColourNames)   

# -----------------------------------------------------------
# Sticks
# -----------------------------------------------------------

cmd.extend("drawSticks", M.drawSticks)   

def stickNames(file):
    '''
    
    This prints out the list of possible stick groups 
    defined in the atribute file.
    
    '''
    
    prot_atri = prot.protein_atri(file)
    sticks = prot_atri.stickNames
    #print sticks
    print 'stick group names:'
    for i in sticks:
        print i

cmd.extend("stickNames", stickNames)   







#


