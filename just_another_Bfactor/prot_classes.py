
import sys
sys.path.append('Utilities/')
import file_utils as fu



class protein_atri:
    
    '''
    - this class is here to deal with the protein's attribute
    the argument it takes is:
    
    atri_file - the path to the attribute file
    place_holder denotes empy feilds in the atribute file
    '''
    
    def __init__(self, atri_file, place_holder='-'):
        #see above for atri_file
        
        records, ColourNames = fu.read_attributes(atri_file)
        self.atri = records
        self.record_names = ColourNames
        
        sticks, names = fu.read_sticks(atri_file)
        self.sticks = sticks
        self.stickNames = names
        
        
    def seperate_atributes(self, place_holder='-'):
    
        '''
        this function sorts out the attributes to those which effect
        chains, residues and single atoms
        
        
        '''
        
        #this function gives attirbutes whish are assigned to the whole chain
        chain = []
        res = []
        atoms = [] 
        
        print self.atri[0]

     
        for entry in self.atri:
            #this pulls out the entires with only chains
            if entry[1] == place_holder and entry[2] == place_holder and entry[3] == place_holder:
                chain.append(entry)
            
            #this pulls out entires with only residues
            if entry[1] != place_holder and entry[2] == place_holder and entry[3] == place_holder:
                res.append(entry)
            
            #this pulls our specific atoms
            if entry[3] != place_holder:
                atoms.append(entry)
            if entry[2] != place_holder:
                atoms.append(entry)
           
        return chain, res, atoms