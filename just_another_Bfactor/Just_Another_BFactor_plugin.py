
import sys
from pymol import cmd
from just_another_Bfactor import file_utils as fu
from just_another_Bfactor import prot_classes as prot
import math
import numpy as np
import pkg_resources
from just_another_Bfactor import Main_functions as M
    
def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command',
                             'Just_Another_BFractor',
                             label = 'Just_Another_BFractor',
                             command = lambda s=self : ColourAtri)
    

def ColourAtri(prot_atri_file, model='', minColour='Blue', maxColour='Red', midColour='White',scale='auto', colour_path='defult', place_holder= '-'):
    
    '''
    this functoion take the protein attribute class and plots the attributes on a structure
    this is prot_atri
    
    prot_atri_file - path to the attribute file
    
    model - name of the structure you want to colour in pymol 
    minColour - colour of the low values 
    maxColour - colour of the high values 
    scale - sets the range of the colouring: if you want to set yout own scale then do it as (10,30)
    colour_path - used to get all the colour definitions in rgb codes
    
    Here the scale goes from the minColour -> white -> maxColour
    
    Note this function colours in the following order:
    1) colour chains 
    2) colour residues
    3) colour atoms
    
    this is to avoid the larger selections colouring over the smaller selections
    
    
    '''

        
    #get the dict of colours
    colours = fu.get_colours(colour_path)
    
    rgb_min  = colours[minColour]
    rgb_max  = colours[maxColour] 
    rgb_mid = colours[midColour] 
    
    prot_atri = prot.protein_atri(prot_atri_file)
    chain_atri, res_atri, atom_atri = prot_atri.seperate_atributes()
    
    #so here we get the range of the scale
    combined_list = chain_atri + res_atri + atom_atri 
    
    if scale == 'auto':
        #use floor and ceil to give interger bounds for the scale 
        scale_min = float(math.floor(min(item[4] for item in combined_list)))
        scale_max = float(math.ceil(max(item[4] for item in combined_list)))
    
    else:
        print 'scale given by user'
        scale_min = scale[0]
        scale_max = scale[1]
    
    scale_diff = scale_max - scale_min
    half_scale_diff = np.divide(scale_diff,2)
    
    colour_count = 0


   #colour the chains
    if chain_atri:
        for i in chain_atri:
            colour_count = colour_count + 1
            rgb_code = M.select_colouring(i, scale_min, scale_diff, rgb_min, rgb_mid,rgb_max)
            
            
            if model != '':
                chain_name = model + 'and chain '+i[0]
            else:
                chain_name =  'chain '+i[0]
            
            #apparently we need to name the colour before we can use it
            cmd.set_color('work'+str(colour_count),rgb_code)
            cmd.color('work'+str(colour_count), chain_name)

            
    if res_atri:
        for i in res_atri:
            colour_count = colour_count + 1
            rgb_code = M.select_colouring(i, scale_min, scale_diff, rgb_min, rgb_mid,rgb_max)
                
            name = ''
                
            #add the model name to the selection        
            if model != '':
                name = model + ' and ' 
                    
            #add the chain name to the selection 
            if i[0] != place_holder:
                name = name + 'chain ' + i[0] + ' and '
                
            #select the residue
            if i[1] != place_holder:
                name = name + 'resi ' + i[1]

            cmd.set_color('work'+str(colour_count),rgb_code)
            cmd.color(str('work'+str(colour_count)), name)
    
    if atom_atri:
        for i in atom_atri:
            colour_count = colour_count + 1
            rgb_code = M.select_colouring(i, scale_min, scale_diff, rgb_min, rgb_mid,rgb_max)
            
            name = ''
            
            #this is unique so we should never need to add to it 
            if i[3] != place_holder:
                name = ' id '+ i[3]    
            else:
                #add the model name to the selection        
                if model != '':
                    name = model + ' and ' 
                    
                #add the chain name to the selection 
                if i[0] != place_holder:
                    name = name + ' chain ' + i[0] + ' and '
                
                #select the residue
                if i[1] != place_holder:
                    name = name + 'resi ' + i[1] + ' and '
            
                #select the residue
                if i[2] != place_holder:
                    name = name + ' name ' + i[2]    
            print name
            cmd.set_color('work'+str(colour_count),rgb_code)
            cmd.color('work'+str(colour_count), name)
        
cmd.extend("ColourAtri",ColourAtri)     
        

 