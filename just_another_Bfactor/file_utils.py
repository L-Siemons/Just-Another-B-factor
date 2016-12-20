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

def determine_section(line, section_start, section_end, message,mark):
    ''' 
    This gives true or false depending on whether you are between the headers or not
    section_start - the line that denotes the start of a section
    section_end - the line that denotes the end of a section
    messgae - a printed message.
    '''
    
    if section_start in line:
        mark = True
        print message
    elif line == section_end:
        mark = False
    else:
        mark = mark
    return mark

 
#--------------------------------------------------------------

def get_titles(line, section_header):

    '''
    This function takes the line with the [section_title]
    and returns the user defined titles. 
    
    These are only there for reference
    
    line - line currently being parsed
    seciton_header - denotes the seciotn se want to look at
    
    note there should be no white space within a title
    
    '''
    if section_header in line:
        split = line.split(section_header)
        names = split[1].split()
        return names

#--------------------------------------------------------------

def read_attributes(file_name, place_holder='-'):
    
    ''' 
    This funtion reads in the Attribute file and returns a list 
    protein = [ [chain,residue,atom_name, id, atribute1, atribute2, ...], ... ] is the structure of the 
    list
    
    also returns the names of the atributes
    
    place_holder - denotes empty feilds in the input file
    file_name - path to the file + name
        
    ''' 
        
    atri_file = open(file_name, 'r')
    
    #this is where the protein/complex of proteins will be kept
    protein = []
    empty_records = []
    ambig = []
    
    #define the markers for reading in sections of the input file
    reading_colour_section = False
    
    for line in atri_file:
        try:
            #this removes the comments 
            info = remove_comments(line)
            
            #this bit of logic tells us if we are in the 'colour section'
            reading_colour_section = determine_section(line,'[colour]','[colour_end]\n', 
                                                       'reading in atributes for colouring',
                                                       reading_colour_section)
            if '[colour]' in line:
                headers = get_titles(line, '[colour]')
            
            
            if reading_colour_section == True:
                #this gives the difference fields

                fields = info.split()        
                chain = fields[0]
                res = fields[1]
                atom_name = fields[2]
                atom_id = fields[3]
                atri = []
                record = []
                #now we dont know how many atributes there are
                for entry in range(4,len(fields),1):
                    atri.append(float(fields[entry]))
                    
                
                
                
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
            
                record.extend([chain, res, atom_name, atom_id])
                #multiple atri values to append now
                for i in atri:
                    record.append(i)
                    
                #add the record to the entires
                protein.append(record)
                
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
    return protein, headers

def read_sticks(file):

    '''
    This function reads in the stics section 
    of the atribute file. This is marked by 
    
    [sticks] and [sticks_end]
    
    it resturns the dict atom_pairs[atom1, atom2] = width
    and the names of the different possible selections
    
    '''

    atri_file = open(file, 'r')
    names = []
    atom_pairs = {}
    reading_sticks_section = False
    headers = 'N/A'
    for i in atri_file.readlines():
        #this bit of logic tells us if we are in the 'colour section'
        reading_sticks_section = determine_section(i,'[sticks]','[sticks_end]\n', 
                                                       'reading in sticks for colouring',
                                                       reading_sticks_section)
        if '[sticks]' in i:
            headers = get_titles(i, '[sticks]')
        
        if reading_sticks_section == True:
            if 'sticks' not in i:
                feilds = i.split(':')
                name = feilds[0].split("'")[1]
                
                if name not in names:
                    names.append(name)
                atom1 = feilds[1]
                atom2 = feilds[2]
                width = feilds[3]
                atom_pairs[name, atom1, atom2] = width

        
    return atom_pairs, names

#--------------------------------------------------------------

def get_colours(colour_file):
    
    '''
    This function reads in all the colours and their RGB codes
    and makes a dictionary from the resoure file resources/colours.dat
    
    colour[name] = (r,g,b)
    
    colour_file or data_path - path to the file
    
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