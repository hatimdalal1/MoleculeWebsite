import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import MolDisplay
import molecule;
import urllib
import re
import io
import molsql
import json

public_files = [ '/index.html', '/script.js', '/elementScript.js', '/sdf.html', '/sdf.js', '/viewMols.js'];
css_files = ['/style.css', '/aestyle.css', '/sdfstyle.css','/viewMols.css']
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        db = molsql.Database(reset=False)
        db.create_tables()
        if self.path == "/":
            self.send_response( 200 ) # OK
            self.send_header( "Content-type", "text/html" )

            currPath = public_files[0]
            fp = open( currPath[1:] ); 
            page = fp.read();
            fp.close();

            self.send_header( "Content-length", len(page) )
            self.end_headers()
            self.wfile.write( bytes( page, "utf-8" ) )

        elif self.path in public_files:
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );
            print(self.path)

            fp = open( self.path[1:] ); 
            page = fp.read();
            fp.close();

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path ==  '/addElements.html':
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );
            print(self.path)

            page = elemetnsPage_header

            # fp = open( self.path[1:] ); 
            # page = page + fp.read();
            # fp.close();

            data = db.conn.execute( "SELECT * FROM Elements;" ).fetchall();
            print(data)

            for elements in data:
                line = f"""<tr>
                <td>{elements[0]}</td>
                <td>{elements[1]}</td>
                <td>{elements[2]}</td>
                <td>{elements[3]}</td>
                <td>{elements[4]}</td>
                <td>{elements[5]}</td>
                <td>{elements[6]}</td>
                <td><button type=\"button\" class=\"deleteButton\" id=\"{elements[0]}\">X</button> </td>
                </tr>
                """
                page += line

            page += elemetnsPage_footer

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == '/viewMols.html':
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );
            print(self.path)

            page = viewMolPage_header

            data = db.conn.execute( "SELECT * FROM Molecules;" ).fetchall();
            strData = json.dumps(data);
            print(strData)
            
            data1 =db.conn.execute(""" SELECT MoleculeAtom.MOLECULE_ID, COUNT(MoleculeAtom.MOLECULE_ID) 
            FROM MoleculeAtom
            GROUP BY MoleculeAtom.MOLECULE_ID
            HAVING COUNT(MoleculeAtom.MOLECULE_ID) > 1
            """).fetchall()
            strData1 = json.dumps(data1)
            print(strData1)

            data2 =db.conn.execute(""" SELECT MoleculeBond.MOLECULE_ID, COUNT(MoleculeBond.MOLECULE_ID) 
            FROM MoleculeBond
            GROUP BY MoleculeBond.MOLECULE_ID
            HAVING COUNT(MoleculeBond.MOLECULE_ID) > 1
            """).fetchall()
            strData2 = json.dumps(data2)
            print(strData2)

            for mols in data:

                for i in range(len(data1)):
                    if (mols[0] == data1[i][0]):
                        j = i

                line = f"""<tr>
                <td id="molid{mols[0]}">{mols[0]}</td>
                <td class="has-details" id="molname{mols[0]}">{mols[1]} <span class="details">Num Atoms: {data1[j][1]}<br>Num Bonds: {data2[j][1]}</span> </td>
                <td><form action="viewMolecule.html" enctype="multipart/form-data" method="post"><input type="hidden" id="molName" name="molName" value="{mols[1]}"><input type="submit" value="View"/></form></td>
                </tr>
                """
                page += line

            page += viewMolPage_footer
            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );


        elif self.path in css_files:
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/css" );
            print(self.path)

            fp = open( self.path[1:] ); 
            page = fp.read();
            fp.close();

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/getElements":
            self.send_response( 200 )
            self.send_header( "Content-type", "text/json" )

            data = db.conn.execute( "SELECT * FROM Elements;" ).fetchall();
            strData = json.dumps(data);
            print(strData)
            self.send_header( "Content-length", len(strData) );
            self.end_headers();

            self.wfile.write( bytes(strData, "utf-8") );

        elif self.path == "/getMols":
            self.send_response( 200 )
            self.send_header( "Content-type", "text/json" )

            data = db.conn.execute( "SELECT * FROM Molecules;" ).fetchall();
            strData = json.dumps(data);
            print(strData)
            print(type(data[0]))
            
            data1 =db.conn.execute(""" SELECT MoleculeAtom.MOLECULE_ID, COUNT(MoleculeAtom.MOLECULE_ID) 
            FROM MoleculeAtom
            GROUP BY MoleculeAtom.MOLECULE_ID
            HAVING COUNT(MoleculeAtom.MOLECULE_ID) > 1
            """).fetchall()
            strData1 = json.dumps(data1)
            print(strData1)

            data2 =db.conn.execute(""" SELECT MoleculeBond.MOLECULE_ID, COUNT(MoleculeBond.MOLECULE_ID) 
            FROM MoleculeBond
            GROUP BY MoleculeBond.MOLECULE_ID
            HAVING COUNT(MoleculeBond.MOLECULE_ID) > 1
            """).fetchall()
            strData2 = json.dumps(data2)
            print(strData2)

            finaldata = []
            i=0
            for entries in data:
                finaldata.append( (data[i][0], data[i][1], data1[i][1], data2[i][1]) )
                i+=1
            
            print(finaldata)
            strfinaldata = json.dumps(finaldata)
            print(strfinaldata)

            
            self.send_header( "Content-length", len(strfinaldata) );
            self.end_headers();

            self.wfile.write( bytes(strfinaldata, "utf-8") );

        
        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )

    def do_POST(self):
        db = molsql.Database(reset=False)
        db.create_tables()
        if self.path == '/molecule':

            # content_length = int(self.headers['Content-Length'])
            # bytesio = io.BytesIO(self.rfile.read(content_length))
            # textio = io.TextIOWrapper(bytesio)      #wrap it

            content_length = int(self.headers['Content-Length'])
            field_data = self.rfile.read(content_length)
            pattern = r'filename="(.+?)"'
            filename = re.findall(pattern, field_data.decode())
            filename = filename[0]


            mol = Moldisplay.Molecule()        #call parse to populate the molecule and get the svg
            mol.parse(open(filename))
            mol.sort()
            svg = mol.svg()

            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.send_header('Content-length', len(svg))            
            self.end_headers()

            self.wfile.write( bytes(svg, "utf-8"))      #send svg back to webpage

        elif self.path == "/form_handler.html":

            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            # print( repr( body.decode('utf-8') ) );

            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            print( postvars);
            print(postvars["c1"][0][1:], postvars["c2"][0][1:], postvars["c3"][0][1:])

            try:
                message = "Element added";
                db['Elements'] = (postvars["number"][0], postvars["code"][0], postvars["name"][0], postvars["c1"][0][1:], postvars["c2"][0][1:], postvars["c3"][0][1:], postvars["radius"][0])
                db.conn.commit()
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/plain" );
                self.send_header( "Content-length", len(message) );
                self.end_headers();
                self.wfile.write( bytes( message, "utf-8" ) );
            except:
                message = "Element values are malicious, try again"
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/plain" );
                self.send_header( "Content-length", len(message) );
                self.end_headers();
                self.wfile.write( bytes( message, "utf-8" ) );
            # db.conn.execute('INSERT INTO Elements VALUES {%d %s %s %s %s %s %d}' % postvars["number"][0], postvars["code"][0], postvars["name"][0], postvars["c1"][0][1:], postvars["c2"][0][1:], postvars["c3"][0][1:], postvars["radius"][0])

        elif self.path == "/delete.html":

            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ))
            print(postvars)
            newVar = postvars["elementNum"][0]
            print( newVar);

            db.conn.execute(f"DELETE FROM Elements WHERE ELEMENT_NO={newVar}")
            db.conn.commit()

            self.send_response( 200 ); # OK
            message = "element deleted, refreshing page now"
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();
            self.wfile.write( bytes(message), "utf-8")
    
        elif self.path == "/sdf.html" :

            molecules = MolDisplay.Molecule();

            content_length = int(self.headers['Content-Length'])
            field_data = self.rfile.read(content_length)
            print(field_data)
            print("done")
            pattern1 = r'filename="(.+?)"'
            filename = re.findall(pattern1, field_data.decode())
            filename = filename[0]
            print("done1")

            pattern2 = r'\r\n\r\n(.*?)\r\n'
            molName = re.search(pattern2, field_data.decode())
            molName = molName[0]
            molName = molName.strip()

            print(filename)
            print(molName)

            bytesio = io.BytesIO(field_data)
            textio = io.TextIOWrapper(bytesio)
            print("done2")

            # db.add_molecule(molName, textio)

            try:
                db.add_molecule(molName, textio);
                
                message = " style = '"'color: green'"'>sdf file uploaded to database";
            except:    
                message = " style = '"'color: red'"'>sdf file or molecule name malicious"


            content = sdf_page_header + message + sdf_page_footer
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(content) );
            self.end_headers();

            self.wfile.write( bytes( content, "utf-8" ) );

        elif self.path == "/viewMolecule.html":
            content_length = int(self.headers['Content-Length'])
            field_data = self.rfile.read(content_length)

            postvars = urllib.parse.parse_qs( field_data.decode( 'utf-8' ))

            print(field_data)
            print(postvars)

            pattern2 = r'\r\n\r\n(.*?)\r\n'
            molName = re.search(pattern2, field_data.decode())
            molName = molName[0]
            molName = molName.strip()


            MolDisplay.radius = db.radius();
            MolDisplay.element_name = db.element_name();
            MolDisplay.header += db.radial_gradients();            
            message = viewMolecule_header
            message += f"<h4 id=\"{molName}\">{molName} Molecule</h4>"
            print(molName)
            curMol = db.load_mol(molName)
            curMol.sort()
            message += curMol.svg()
            message += """<div class="slidecontainer">
            <input type="range" min="0" max="360" value="0" class="slider" id="slideX" oninput="this.nextElementSibling.value = this.value">
            <output>0</output>
            <input type="range" min="0" max="360" value="0" class="slider" id="slideY" oninput="this.nextElementSibling.value = this.value">
            <output>0</output>
            <input type="range" min="0" max="360" value="0" class="slider" id="slideZ" oninput="this.nextElementSibling.value = this.value">
            <output>0</output>
            </div>"""


            self.send_response( 200 ); # OK


            message += viewMolecule_footer
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();
            self.wfile.write( bytes( message, "utf-8" ) );

        elif self.path == "/rotation":
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ))
            print(postvars)

            molName = postvars["name"][0]
            val = postvars["value"][0]
            axis = postvars["coordinate"][0]

            MolDisplay.radius = db.radius();
            MolDisplay.element_name = db.element_name();
            MolDisplay.header += db.radial_gradients(); 

            curMol = MolDisplay.Molecule
            curMol = db.load_mol(molName)
            curMol.sort()

            if (axis == "x"):
                mx = molecule.mx_wrapper(int(val),0,0);
            elif (axis == "y"):
                mx = molecule.mx_wrapper(0,int(val),0);
            elif (axis == "z"):
                mx = molecule.mx_wrapper(0,0,int(val));

            curMol.xform(mx.xform_matrix)

            curMol.sort()
            message = curMol.svg()
            print(message)

            self.send_response( 200 )
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();
            self.wfile.write( bytes( message, "utf-8" ) );


        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )





home_page = """
<html>
    <head>
        <title> File Upload </title>
    </head>
    <body>
        <h1> File Upload </h1>
        <form action="molecule" enctype="multipart/form-data" method="post">
        <p>
            <input type="file" id="sdf_file" name="filename"/>
        </p>
        <p>
            <input type="submit" value="Upload"/>
        </p>
        </form>
    </body>
</html>
"""


sdf_page_header = """
<!DOCTYPE html>
    <html>
        <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
        <script src="sdf.js" /></script>
        <link rel="stylesheet" type="text/css" href="style.css" />
        <title>Add SDF</title>
    </head>
    <body>
        <h1>Welcome to Assignment 4!</h1>
            <h3 id="home" name="home" ><a href="/index.html">Home</a></h3>
            <h3 id="addEl" name="addEl" ><a href="/addElements.html">Add/Remove Elements</a></h3>
            <h3 id="addSDF" name="addSDf"><a href="/sdf.html">Add SDF File</a></h3>
            <h3 id="viewMol" name="viewMol"><a href="viewMols.html">View Molecules</a></h3>
        <h1> File Upload </h1>
        <h4
"""

sdf_page_footer = """
            </h4>
            <form enctype="multipart/form-data" method="post" id="sdfForm" name="sdfForm">
            <p>
                <label for="sdf_file">Choose SDF file:</label>
                <input type="file" id="sdf_file" name="sdf_file"/>
            </p>
            <p>
                <label for="moleculeName">Molecule Name:</label>
                <input type="text" id="moleculeName" name="moleculeName" required>
            </p>
            <p>
                <input type="submit" value="Upload"/>
            </p>
            </form>
    </body>
"""

elemetnsPage_header = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
    <script src="/elementScript.js" /></script>
    <link rel="stylesheet" type="text/css" href="style.css" />
    <title>Add Elements</title>
</head>
<body>
  <h1>Welcome to Assignment 4!</h1>
    <h3 id="home" name="home" ><a href="/index.html">Home</a></h3>
    <h3 id="addEl" name="addEl" ><a href="/addElements.html">Add/Remove Elements</a></h3>
    <h3 id="addSDF" name="addSDf"><a href="/sdf.html">Add SDF File</a></h3>
    <h3 id="viewMol" name="viewMol"><a href="viewMols.html">View Molecules</a></h3>
  
    <br>
    <h1>Add Elements</h1>
  
    <form id="elementForm" name="elementForm">
        <label for="elementNum">Element Number:</label>
        <input type="number" id="elementNum" name="elementNum" min="1" required>
        <br><br>
    
        <label for="elementCode">Element Code:</label>
        <input type="text" id="elementCode" name="elementCode" style="text-transform: capitalize;" required>
        <br><br>
    
        <label for="elementName">Element Name:</label>
        <input type="text" id="elementName" name="elementName" style="text-transform: capitalize;" required>
        <br><br>
    
        <label for="colour1">Colour 1:</label>
        <input type="color" id="colour1" name="colour1" required>
        <br><br>
    
        <label for="colour2">Colour 2:</label>
        <input type="color" id="colour2" name="colour2" required>
        <br><br> 
    
        <label for="colour3">Colour 3:</label>
        <input type="color" id="colour3" name="colour3" required>
        <br><br>
    
        <label for="radius">Radius:</label>
        <input type="number" id="radius" name="radius" required>
        <br><br>
    
        <button id="button" name="button" "type="submit">Add Element</button>
    </form>
    <br>
    <br>
    <br>
    <table>
        <thead>
        <tr>
            <th>Element Number</th>
            <th>Element Code</th>
            <th>Element Name</th>
            <th>Colour 1</th>
            <th>Colour 2</th>
            <th>Colour 3</th>
            <th>Radius</th>
            <th>Delete</th>
        </tr>
        </thead>
    <tbody>
"""

elemetnsPage_footer = """ 
    </tbody>
  </table>
</body>
</html>
"""

viewMolPage_header = """
<!DOCTYPE html>
<html>
    <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
        <script src="/viewMols.js" /></script>
        <link rel="stylesheet" type="text/css" href="viewMols.css" />
        <title>View Molecules</title>
    </head>
    <body>
        <h1>Welcome to Assignment 4!</h1>
            <h3 id="home" name="home" ><a href="/index.html">Home</a></h3>
            <h3 id="addEl" name="addEl" ><a href="/addElements.html">Add/Remove Elements</a></h3>
            <h3 id="addSDF" name="addSDf"><a href="/sdf.html">Add SDF File</a></h3>
            <h3 id="viewMol" name="viewMol"><a href="viewMols.html">View Molecules</a></h3> 
        <br>
        <h1>View Molecules</h1>
        <table>
            <thead>
            <tr>
                <th>Molecule ID</th>
                <th>Molecule Names</th>
                <th>View</th>
            </tr>
            </thead>
        <tbody>
"""

viewMolPage_footer = """
    </tbody>
    </table>
</body>
</html>
"""


viewMolecule_header = """
<!DOCTYPE html>
<html>
    <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
        <script src="/viewMols.js" /></script>
        <link rel="stylesheet" type="text/css" href="viewMols.css" />
        <title>View Molecules</title>
    </head>
    <body>
        <h1>Welcome to Assignment 4!</h1>
            <h3 id="home" name="home" ><a href="/index.html">Home</a></h3>
            <h3 id="addEl" name="addEl" ><a href="/addElements.html">Add/Remove Elements</a></h3>
            <h3 id="addSDF" name="addSDf"><a href="/sdf.html">Add SDF File</a></h3>
            <h3 id="viewMol" name="viewMol"><a href="viewMols.html">View Molecules</a></h3> 
        <br>
        <h1>View Molecules</h1>
"""

viewMolecule_footer = """
    </body>
</html>
"""
httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
httpd.serve_forever()
