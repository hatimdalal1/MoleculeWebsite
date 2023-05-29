import molecule
import re

radius = {
    # 'H': 25,
    # 'C': 40,
    # 'O': 40,
    # 'N': 40,
}

element_name = {
    # 'H': 'grey',
    # 'C': 'black',
    # 'O': 'red',
    # 'N': 'blue',
}

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">\n"""
footer = """</svg>"""
offsetx = 500
offsety = 500

class Atom():

    def __init__(self, c_atom):
        self.atom = c_atom
        self.z = c_atom.z

    def __str__(self):
        element = self.atom.element
        x, y, z = self.atom.x, self.atom.y, self.atom.z
        return f'Element: {element}, X: {x:.4f} Y: {y:.4f}, Z {z:.4f}\n'
    
    def svg(self):
        element = self.atom.element
        x, y, z = self.atom.x, self.atom.y, self.atom.z
        if element not in element_name:
            element = "gg"
        rad = radius[element]
        fill = element_name[element]
        cx = x * 100.0 + offsetx
        cy = y * 100.0 + offsety
        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % ( cx, cy, rad, fill)
        

class Bond():

    def __init__(self, c_bond):
        self.bond = c_bond
        self.z = c_bond.z
        
    def __str__(self):
        a1, a2 = self.bond.a1, self.bond.a2
        return f'Bond ({a1}, {a2})\n'     #used for debugging, add info about atoms it contains and their vals?
    
    def svg(self):
        
        x1 = (self.bond.x1 * 100.0) + offsetx       #calculate coordinate values as per requirements
        y1 = (self.bond.y1 * 100.0) + offsety

        x2 = (self.bond.x2 * 100.0) + offsetx
        y2 = (self.bond.y2 * 100.0) + offsety
        points = [
            x1 - (self.bond.dy*10), y1 + (self.bond.dx*10),         #calculate coordinate values for the polygon shape
            x1 + (self.bond.dy*10), y1 - (self.bond.dx*10),
            x2 + (self.bond.dy*10), y2 - (self.bond.dx*10),
            x2 - (self.bond.dy*10), y2 + (self.bond.dx*10)
        ]
        return f'  <polygon points="{points[0]:.2f},{points[1]:.2f} {points[2]:.2f},{points[3]:.2f} {points[4]:.2f},{points[5]:.2f} {points[6]:.2f},{points[7]:.2f}" fill="green"/>\n'
    


class Molecule(molecule.molecule):

    # def __init__(self):
    #     super().__init__()


    def __str__(self):
        s = ""
        for i in range(self.atom_no):
            s +=  Atom(self.get_atom(i)).__str__()
        for i in range(self.bond_no):
            s += Bond(self.get_bond(i)).__str__()
        return s

    def svg(self):
        molsvg = header
        i = 0
        j = 0

        while i<self.atom_no and j<self.bond_no:        #while both the lists have not been gone thru
            if Atom(self.get_atom(i)).z < Bond(self.get_bond(j)).z:     #check which one has a smaller z value and add their svg to molsvg
                molsvg += Atom(self.get_atom(i)).svg()
                i += 1
            else:
                molsvg += Bond(self.get_bond(j)).svg()
                j += 1
        
        while j < self.bond_no:     #add remaining elements from atoms and bonds into molsvg
            molsvg += Bond(self.get_bond(j)).svg()
            j += 1
        while i < self.atom_no:
            molsvg += Atom(self.get_atom(i)).svg()
            i += 1
        
        molsvg += footer
        return molsvg
        

    def parse(self, fileObject):
        sdf_text = fileObject.read()
        lines = sdf_text.strip().split('\n')

        # lines = [line for line in lines if line.strip() != '']

        # # get number of atoms and bonds from first line
        line3 = re.split("\s+", lines[3], 3)            #was just "\s before"
        num_atoms = int(line3[1])
        num_bond = int(line3[2])

        # # extract atom information from lines 4 to 4 + num_atoms
        for i in range(4, 4+num_atoms):
            atom_info = lines[i].split()
            x = float(atom_info[0])
            y = float(atom_info[1])
            z = float(atom_info[2])
            element =  atom_info[3]
            self.append_atom(element,x ,y ,z)

        # # extract bond information from lines 4 + num_atoms to end of file
        for i in range(4+num_atoms, 4+num_bond+num_atoms):
            bond_info = lines[i].split()
            a1 = int(bond_info[0]) - 1
            a2 = int(bond_info[1]) - 1
            epairs = int(bond_info[2])
            self.append_bond(a1, a2, epairs)

        fileObject.close()

    def parser(self, fileObject):

        for i in range(0,8):            #skip the initial lines
            sdf_text = fileObject.readline()
        
        line4 = re.split("\s+", sdf_text, 4)        #split the line to get atom_no and bond_no
        num_atoms = int(line4[1])
        num_bond = int(line4[2])

        for i in range(4, 4+num_atoms):     #populate all the atoms
            sdf_text = fileObject.readline()
            atom_info = sdf_text.split()
            x =float(atom_info[0])
            y = float(atom_info[1])
            z = float(atom_info[2])
            element =  atom_info[3]
            self.append_atom(element,x ,y ,z)

        # extract bond information from lines 4 + num_atoms
        for i in range(4+num_atoms, 4+num_bond+num_atoms):      #populate all the bonds
            sdf_text = fileObject.readline()
            bond_info = sdf_text.split()
            a1 = int(bond_info[0])-1        #PART 0 change
            a2 = int(bond_info[1])-1
            epairs = int(bond_info[2])
            self.append_bond(a1, a2, epairs)
    

# if __name__ == '__main__':
    
#     mol1 = Molecule()
#     mol2 = Molecule()
#     mol3 = Molecule()

#     # mol.parse(field_data.decode('utf-8').split('\n')[4:])


#     mol1.parser(open("caffeine-3D-structure-CT1001987571.sdf", "r"))
#     # print(mol1)
#     mol1.sort()
#     svg = mol1.svg()
#     fp = open("caffiene.svg", "w")
#     fp.write(svg)
#     print("created caffience.svg")
#     fp.close()


#     mol2.parser(open("CID_31260.sdf", "r"))
#     print(mol2)
#     mol2.sort()
#     print(mol2)
#     svg = mol2.svg()
#     fp = open("CID.svg", "w")
#     fp.write(svg)
#     print("created CID.svg")
#     fp.close()
    

#     mol3.parser(open("water-3D-structure-CT1000292221.sdf", "r"))
#     mol3.sort()
#     svg = mol3.svg()
#     fp = open("water.svg", "w")
#     fp.write(svg)
#     print("created water.svg")
#     fp.close()

