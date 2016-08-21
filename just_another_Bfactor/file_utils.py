import os

def compile_record_list_message(base_messgae, list):
    
    '''
    this function creates a string which goes 
    
    messgae of some type ...
    record 1 
    record 2 
    etc ...
    
    '''
    base = base_messgae
    for i in list:

        base = base + str(i)
    return base
    
#--------------------------------------------------------------

def remove_comments(line, comment_ind='#'):
    
    '''
    This function removes the comments in a line denoted by #
    '''
    
    read_in = line.split(comment_ind)[0]
    return read_in

#--------------------------------------------------------------

def read_attributes(file_name, place_holder='-'):
    
    ''' 
    This funtion reads in the Attribute file and returns a list 
    protein = [ [chain,residue,atom_name, id, atribute], ... ] is the structure of the 
    list
    
     place_holder - denotes empty feilds in the input file
     file_name - path to the file + name
        
    ''' 
        
    atri_file = open(file_name, 'r')
    
    #this is where the protein/complex of proteins will be kept
    protein = []
    empty_records = []
    ambig = []
    
    for line in atri_file:
        try:
            #this removes the comments 
            info = remove_comments(line)
        
            #this gives the difference fields
            fields = info.split()        
            chain = fields[0]
            res = fields[1]
            atom_name = fields[2]
            atom_id = fields[3]
            atri = fields[4]

            if atom_id == place_holder:
                if res == place_holder:
                    if atom_name != place_holder:
                        #this checks for records which have an atom name but no res
                        ambig.append(line)
                

                if chain == place_holder:
                    if res == place_holder:
                        if atom_name == place_holder:
                            #collects the empty records
                            empty_records.append(line)
            
            protein.append([chain, res, atom_name, atom_id, float(atri)])
        
        except IndexError:
            pass
        
    if empty_records :
        if empty_records:
            empty_message  = compile_record_list_message('These records are empty: \n',empty_records)
        else:
            empty_message = 'No Empty records'

        if ambig:
            ambig_message = compile_record_list_message('These records are ambiguous as many atoms have the same name : \n', ambig)
        else:
            ambig_message = 'No ambiguous records'
        
        error_msg = empty_message + '\n' + ambig_message
        raise Exception(error_msg)
    
    atri_file.close()
    return protein
    
#--------------------------------------------------------------

def get_colours(colour_file):
    
    '''
    This function reads in all the colours and their RGB codes
    and makes a dictionary 
    
    colour[name] = (r,g,b)
    
    colour_file - path to the file
    
    '''
    #this should give the right path to the resource file
    if colour_file == 'defult':
        data_path = os.path.join(os.path.dirname(__file__),'resources')
        data = open(os.path.join(data_path,'colours.dat'), 'r')
    else:
        data = open(colour_file, 'r')
        
    colours = {}
    for line in data.readlines():
        if line[0] != '#':
            line = line.split()
            #do the conversion here because pymol RGB values go form 0 to 1
            r = float(line[-3])/255.0
            g = float(line[-2])/255.0
            b = float(line[-1])/255.0
            
            #removes the rgb vlaues from the list so we can make the name
            line.remove(line[-3])
            line.remove(line[-2])
            line.remove(line[-1])
            name = ' '.join(line)
            rgb = (r,g,b)
            colours[name] = rgb
    data.close
    return colours