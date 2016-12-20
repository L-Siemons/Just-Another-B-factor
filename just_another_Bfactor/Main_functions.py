from pymol import cmd
import sys
import file_utils as fu
import prot_classes as prot
import math
import numpy as np
import pkg_resources



def get_RGB_codes(min, max, scale):
    
    '''
    This function gets the RGB codes for the attributes
    min - the min colour rgb codes
    max is the max colour rgb codes
    scale is the scaled value 
    colour dict is the dictionary of defult RGB codes 
    
    note that here the colour bar is broken into two scales
    in the defult this is:
    
    blue -> white 
    and white -> red 
    
    this returns a scaled value rgb list [r,g,b]
    where each value is between 0 and 1
    '''
    
    scaled_rgb = []
    for indx, item in enumerate(max):
        range = max[indx] - min[indx]
        scaled_range = range*scale
        scaled_rgb.append(min[indx] + scaled_range)
    return scaled_rgb

def select_colouring(record, scale_min, scale_diff, rgb_min, rgb_mid,rgb_max, col):
    
    '''
    Since the colour bar we ae using has tso colour transitions this function adds some ligic to
    get_RGB_codes() to decide which colour transition we need and then returns the correct rgb code
    
    parameters
    record - entry from the input file 
    scale_min - lowest value of the scale 
    scale_diff - difference between the lowest and highest values 
    rgb_min - rgb code of the min colour
    rgb_mid - rgb code of the mid colour
    rgb_mix - rgb code of the mix colour

    '''
    
    atri = record[col]
    #print '----------'
    #here we have scaled the difference to be between 0 and 1
    scaled_atri = np.divide(atri - scale_min, scale_diff)
            
    #if less than the half way we colour between min and mid 
    #print scaled_atri
    if scaled_atri < 0.5:
        record_rgb = get_RGB_codes(rgb_min, rgb_mid, (scaled_atri*2))
            
    #bang on the mid value means we can just make it the mid colour
    if scaled_atri == 0.5:
        record_rgb = rgb_mid

    #if greater than the half way we colour between mid and max
    if scaled_atri > 0.5:
            
        #I think I can get rid of the line below
        scaled_atri = scaled_atri - 0.5
        record_rgb = get_RGB_codes(rgb_mid, rgb_max, (scaled_atri*2))  
    
    return record_rgb
        
    
def ColourAtri(prot_atri_file, col='4',model='', minColour='Blue', maxColour='Red', midColour='White',
                scale='auto', colour_path='defult', place_holder= '-'):
    
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

    col = int(col)   
    #get the dict of colours
    colours = fu.get_colours(colour_path)
    
    rgb_min  = colours[minColour]
    rgb_max  = colours[maxColour] 
    rgb_mid = colours[midColour] 
    
    prot_atri = prot.protein_atri(prot_atri_file)
    chain_atri, res_atri, atom_atri = prot_atri.seperate_atributes()
    
    #so here we get the range of the scale
    combined_list = chain_atri + res_atri + atom_atri 
    #print '============================'
    if scale == 'auto':
        #use floor and ceil to give interger bounds for the scale 
        scale_min = float(math.floor(min(item[col] for item in combined_list)))
        scale_max = float(math.ceil(max(item[col] for item in combined_list)))
    
    else:
        print 'scale given by user'
        scale_min = scale[0]
        scale_max = scale[1]
    
    scale_diff = scale_max - scale_min
    half_scale_diff = np.divide(scale_diff,2)
    
    colour_count = 0

    #print '-------------------------------'
    #colour the chains
    if chain_atri:
        for i in chain_atri:
            colour_count = colour_count + 1
            rgb_code = select_colouring(i, scale_min, scale_diff, rgb_min, rgb_mid,rgb_max,col)
            
            
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
            rgb_code = select_colouring(i, scale_min, scale_diff, rgb_min, rgb_mid,rgb_max,col)
                
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
            rgb_code = select_colouring(i, scale_min, scale_diff, rgb_min, rgb_mid,rgb_max, col)
            
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
        
def drawSticks(atri_file, name='name'):

    '''
    
    This takes the [sticks] seciotn of the atribute file and 
    and creates bonds between the specified atoms and draws sticks of the 
    specified width.
    
    note that the width takes alues between 0 and 1
    
    '''  
        
    protein = prot.protein_atri(atri_file)
    sticks = protein.sticks
    
    total_sticks = ''
    for i in sticks.keys():
        
        if i[0] == name:
            #make bond 
            #print i[1], i[2]
            cmd.bond(i[1], i[2])
            #set width 
            sel = '(' + i[1] + ') or (' + i[2]+')'
            if total_sticks != '':
                total_sticks = total_sticks  + ' or ' + sel
            else:
                total_sticks = sel   
            cmd.set('stick_radius', str(sticks[i]), sel)
            #then show
    
    cmd.show('sticks', total_sticks)
    
    
    