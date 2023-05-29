# CC = clang
# CFLAGS = -Wall -std=c99 -pedantic -g

# all: swig libmol.so mol.o molecule_wrap.o _molecule.so

# swig:
# 	swig -python molecule.i

# libmol.so:	mol.o
# 	$(CC) mol.o -shared -o libmol.so -lm

# mol.o:  mol.c mol.h
# 	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

# molecule_wrap.o:  molecule_wrap.c mol.h
# 	$(CC) $(CFLAGS) -c molecule_wrap.c -fPIC -o molecule_wrap.o -I /Library/Frameworks/Python.framework/Versions/3.10/include/python3.10

# _molecule.so: molecule_wrap.o
# 	$(CC) molecule_wrap.o -shared -lpython3.10 -o _molecule.so -lm -L. -lmol -L/Library/Frameworks/Python.framework/Versions/3.10/lib -dynamiclib  

# clean:  
# 	rm -f *.o *.so

CC = clang
CFLAGS = -Wall -std=c99 -pedantic -g

all: swig libmol.so mol.o molecule_wrap.o _molecule.so

swig:
	swig -python molecule.i

libmol.so:	mol.o
	$(CC) mol.o -shared -o libmol.so -lm

mol.o:  mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

molecule_wrap.o:  molecule_wrap.c mol.h
	$(CC) $(CFLAGS) -c molecule_wrap.c -fPIC -o molecule_wrap.o -I /usr/include/python3.7m

_molecule.so: molecule_wrap.o
	$(CC) molecule_wrap.o -shared -lpython3.7m -o _molecule.so -lm -L. -lmol -L/usr/lib/python3.7/config-3.7m-x86_64-linux-gnus  

clean:  
	rm -f *.o *.so