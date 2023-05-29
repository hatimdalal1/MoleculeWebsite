import os;
import sqlite3;
import MolDisplay 
from MolDisplay import Molecule, Atom, Bond

class Database:

    def __init__(self, reset):
        
        self.conn = sqlite3.connect('molecules.db')
        if reset:        #if reset then delete   
            os.remove('molecules.db')

        self.conn = sqlite3.connect('molecules.db')
        self.conn.commit()

    def create_tables(self):
        #Elements table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Elements (  
                    ELEMENT_NO          INTEGER            NOT NULL,
                    ELEMENT_CODE        VARCHAR(4)         NOT NULL,
                    ELEMENT_NAME        VARCHAR(33)        NOT NULL,
                    COLOUR1             CHAR(7)            NOT NULL,
                    COLOUR2             CHAR(7)            NOT NULL,
                    COLOUR3             CHAR(7)            NOT NULL,
                    RADIUS              DECIMAL(3)         NOT NULL, 
                    PRIMARY KEY (ELEMENT_NO) )""")

        #Atoms table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Atoms (
                    ATOM_ID             INTEGER             NOT NULL    PRIMARY KEY     AUTOINCREMENT,
                    ELEMENT_CODE        VARCHAR(3)          NOT NULL,
                    X                   DECIMAL(7,4)        NOT NULL,
                    Y                   DECIMAL(7,4)        NOT NULL,
                    Z                   DECIMAL(7,4)        NOT NULL,
                    FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements)""")

        #Bonds table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Bonds (
                            BOND_ID         INTEGER         NOT NULL        PRIMARY KEY     AUTOINCREMENT,
                            A1              INTEGER         NOT NULL,
                            A2              INTEGER         NOT NULL,
                            EPAIRS          INTEGER         NOT NULL )""")

        #Molecules table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Molecules (
                    MOLECULE_ID         INTEGER             NOT NULL            PRIMARY KEY     AUTOINCREMENT,
                    NAME                TEXT                NOT NULL            UNIQUE) """)

        #MoleculeAtom table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeAtom (
                    MOLECULE_ID         INTEGER         NOT NULL,
                    ATOM_ID             INTEGER         NOT NULL,
                    PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                    FOREIGN KEY(MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                    FOREIGN KEY(ATOM_ID) REFERENCES Atoms(ATOM_ID) )""")

        #MoleculeBond table
        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeBond (
                    MOLECULE_ID         INTEGER         NOT NULL,
                    BOND_ID             INTEGER         NOT NULL,
                    FOREIGN KEY(MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                    FOREIGN KEY(BOND_ID) REFERENCES Bonds(BOND_ID),
                    PRIMARY KEY(MOLECULE_ID, BOND_ID))""")

        self.conn.commit()

    def __setitem__( self, table, values ):
        self.conn.execute(f"INSERT INTO {table} VALUES {values}")
    
    def add_atom(self, molname, atom):
        # self.conn.execute('INSERT INTO Atoms (ELEMENT_CODE, X, Y, Z) VALUES ("%s", "%f", "%f", "%f")' % (atom.element, atom.x, atom.y, atom.z) )
        elements = self.conn.execute("SELECT ELEMENT_CODE FROM Elements").fetchall()
        print(elements, atom.element)
        exist = 0

        for element in elements:
            for els in element:
                if atom.element == els:
                    print(els)
                    exist = 1
        
        if exist == 0:
            atom.element = "gg"
        print(exist, atom.element)
        
        self.__setitem__("Atoms (ELEMENT_CODE, X, Y, Z)", (atom.element, atom.x, atom.y, atom.z))       #add atom

        atom_id = self.conn.execute('SELECT MAX(ATOM_ID) FROM Atoms WHERE (ELEMENT_CODE = "%s" AND X = "%f" AND Y = "%f" AND Z = "%f")' % (atom.element, atom.x, atom.y, atom.z)).fetchall()     #change this to get the latest addition
        mol_id = self.conn.execute('SELECT MOLECULE_ID FROM Molecules WHERE (NAME = "%s")' % (molname)).fetchall()
        
        # self.conn.execute('INSERT INTO MoleculeAtom (MOLECULE_ID, ATOM_ID) VALUES ("%d", "%d")' % (mol_id[0][0], atom_id[0][0]))
        self.__setitem__("MoleculeAtom (MOLECULE_ID, ATOM_ID)", (mol_id[0][0], atom_id[0][0]))      #add entry in MoleculeAtom

        self.conn.commit()

    def add_bond( self, molname, bond ):
        # self.conn.execute('INSERT INTO Bonds (A1, A2, EPAIRS) VALUES ("%d", "%d", "%d")' % (bond.a1, bond.a2, bond.epairs) )
        self.__setitem__("Bonds (A1, A2, EPAIRS)", (bond.a1, bond.a2, bond.epairs))     #add bond

        bond_id = self.conn.execute('SELECT MAX(BOND_ID) FROM Bonds WHERE (A1 = "%d" AND A2 = "%d" AND EPAIRS = "%d")' % (bond.a1, bond.a2, bond.epairs)).fetchall()
        mol_id = self.conn.execute('SELECT MOLECULE_ID FROM Molecules WHERE (NAME = "%s")' % (molname)).fetchall()
        
        # self.conn.execute('INSERT INTO MoleculeBond (MOLECULE_ID, BOND_ID) VALUES ("%d", "%d")' % (mol_id[0][0], bond_id[0][0]))
        self.__setitem__("MoleculeBond (MOLECULE_ID, BOND_ID)", (mol_id[0][0], bond_id[0][0]))      #add entry in molecule bond
        self.conn.commit()

    def add_molecule( self, name, fp ):
        mol = Molecule()
        mol.parser(fp)      #for A4
        # mol.parse(fp)     #for local testing

        self.conn.execute('INSERT INTO Molecules (NAME) VALUES ("%s")' % (name))        #add molecule into molecule table

        for i in range(mol.atom_no):        #add all atoms and bonds
            self.add_atom(name, mol.get_atom(i))
        
        for i in range(mol.bond_no):
            self.add_bond(name, mol.get_bond(i))

    def load_mol( self, name ):
        newMol = Molecule()
        
        mol_id = self.conn.execute('SELECT MOLECULE_ID FROM Molecules WHERE (NAME = "%s")' % (name)).fetchall()[0][0]
        
        allAtoms = self.conn.execute("""SELECT Atoms.ELEMENT_CODE, Atoms.X, Atoms.Y, Atoms.Z FROM
        Atoms INNER JOIN MoleculeAtom ON
        Atoms.ATOM_ID=MoleculeAtom.ATOM_ID
        WHERE MoleculeAtom.MOLECULE_ID="%d"
        ORDER BY Atoms.ATOM_ID ASC""" % (mol_id)).fetchall()         #get atom values where molname = name and reference using mollecule_id

        allBonds = self.conn.execute("""SELECT Bonds.A1, Bonds.A2, Bonds.EPAIRS FROM
        Bonds INNER JOIN MoleculeBond ON
        Bonds.BOND_ID = MoleculeBond.BOND_ID
        WHERE MOLECULE_ID = "%d"
        ORDER BY Bonds.BOND_ID ASC""" % (mol_id)).fetchall()

        for atom in allAtoms:       #populate molecule object with atoms and bonds
            newMol.append_atom(atom[0], atom[1], atom[2], atom[3])

        for bond in allBonds:
            newMol.append_bond(bond[0], bond[1], bond[2])
            
        return newMol

    def radius( self ):
        rad_dict = {}

        table = self.conn.execute('''SELECT ELEMENT_CODE, RADIUS FROM Elements''').fetchall()

        for rows in table:      #get value for all elemnts and add to dictionary
            element = rows[0]
            rad = rows[1]
            rad_dict[element] = rad
        rad_dict["gg"] = 20
        return rad_dict
            
    def element_name( self ):
        element_dict = {}

        table = self.conn.execute('''SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements''').fetchall()

        for rows in table:          #get value for all elemnts and add to dictionary
            element = rows[0]
            name = rows[1]
            element_dict[element] = name
        element_dict["gg"] = "gg"
        return element_dict

    def radial_gradients( self ):

        returnString = ""

        table = self.conn.execute('''SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements''').fetchall()

        for rows in table:      #get all values from table and concatenate string
            name = rows[0]
            c1 = rows[1]
            c2 = rows[2]
            c3 = rows[3]

            returnString = returnString + """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
            <stop offset="0%%" stop-color="#%s"/>
            <stop offset="50%%" stop-color="#%s"/>
            <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>""" % (name, c1, c2, c3)
        
        returnString += """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
            <stop offset="0%%" stop-color="#%s"/>
            <stop offset="50%%" stop-color="#%s"/>
            <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>""" % ("gg", "FF0000", "00FF00", "0000FF")

        return returnString
    


if __name__ == "__main__":
    db = Database(reset=True)
    db.create_tables()

    db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 )
    db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 )
    db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 )
    db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 )
    print("opening file", end="\n\n\n")

    fp = open( 'water-3D-structure-CT1000292221.sdf' )
    db.add_molecule( 'Water', fp )

    fp = open( 'caffeine-3D-structure-CT1001987571.sdf' )
    db.add_molecule( 'Caffeine', fp )

    fp = open( 'CID_31260.sdf' )
    db.add_molecule( 'Isopentanol', fp )

    #  # # display tables
    # print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    # print("")
    # print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
    # print("")
    # print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
    # print("")
    # print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
    # print("")
    # print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
    # print("")
    # print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );

   
    # db = Database(reset = False); # or use default

    # MolDisplay.radius = db.radius();
    # MolDisplay.element_name = db.element_name();
    # MolDisplay.header += db.radial_gradients();

    # for molecule in [ 'Water', 'Caffeine', 'Isopentanol' ]:
    #     mol = db.load_mol( molecule );
    #     mol.sort();
    #     fp = open( molecule + ".svg", "w" );
    #     fp.write( mol.svg() );
    #     fp.close();
    #     print("Created", molecule)

    db = Database(reset = False)
    # db['Elements'] = ( 11, 'Na', 'Sodium', '000000', '000000', '020202', 10 )

    db.conn.execute('DELETE FROM Elements WHERE ELEMENT_CODE = "hhH" ')
    db.conn.execute('DELETE FROM Elements WHERE ELEMENT_CODE = "BB" ')
    db.conn.execute('DELETE FROM Elements WHERE ELEMENT_CODE = "LI" ')
    db.conn.execute('DELETE FROM Elements WHERE ELEMENT_CODE = "asc" ')
    
    
    print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    print("")

    db.conn.execute('DELETE FROM Molecules WHERE NAME = "wats" ')
    db.conn.execute('DELETE FROM Molecules WHERE NAME = "caf" ')
    db.conn.execute('DELETE FROM Molecules WHERE NAME = "aa" ')

    print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    # db['Elements'] = ( 3, 'Li', 'Lithium', 'FFFFFF', '050505', '020202', 25 )

    db.conn.commit()