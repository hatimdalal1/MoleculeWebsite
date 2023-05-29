#include "mol.h"
#include <math.h>


void atomset( atom *atom, char element[3], double *x, double *y, double *z ) {
    strcpy(atom->element, element);
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

void atomget( atom *atom, char element[3], double *x, double *y, double *z ) {
    strcpy(element, atom->element);
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ) {
    
    bond->epairs = *epairs;     //A2 change
    bond->a1 = *a1;             //A2 change 
    bond->a2 = *a2;             //A2 change
    bond->atoms = *atoms;
    compute_coords(bond);

}

void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){        
    *epairs = bond->epairs;
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;       //A2 change
    
}

void compute_coords(bond *bond) {       //A2 change
    unsigned short a1 = bond->a1;
    unsigned short a2 = bond->a2;
    
    bond->x1 = bond->atoms[a1].x;
    bond->x2 = bond->atoms[a2].x;

    bond->y1 = bond->atoms[a1].y;
    bond->y2 = bond->atoms[a2].y;

    bond->z = (bond->atoms[a1].z + bond->atoms[a2].z) / 2;

    bond->dx = bond->x2 - bond->x1;
    bond->dy = bond->y2 - bond->y1;

    bond->len = sqrt((bond->dx * bond->dx) + (bond->dy * bond->dy));

    bond->dx = (bond->x2 - bond->x1)/bond->len;
    bond->dy = (bond->y2 - bond->y1)/bond->len;

}

molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ) {
    molecule *molecule_alloc;
    molecule_alloc = malloc(sizeof(molecule));
    if (molecule_alloc == NULL) {
        return NULL;
    }

    molecule_alloc->atom_max = atom_max;
    molecule_alloc->atom_no = 0;
    molecule_alloc->atoms = malloc(atom_max * sizeof(atom));
    if (molecule_alloc->atoms == NULL) {
        return NULL;
    }
    molecule_alloc->atom_ptrs = malloc(atom_max * sizeof(atom*));       
    if (molecule_alloc->atom_ptrs == NULL) {
        return NULL;
    }

    molecule_alloc->bond_max = bond_max;
    molecule_alloc->bond_no = 0;
    molecule_alloc->bonds = malloc(bond_max * sizeof(bond));
    if (molecule_alloc->bonds == NULL) {
        return NULL;
    }
    molecule_alloc->bond_ptrs = malloc(bond_max * sizeof(bond*));       
    if (molecule_alloc->bond_ptrs == NULL) {
        return NULL;
    }

    return molecule_alloc;
}

molecule *molcopy( molecule *src ) {
    molecule *new_mol = molmalloc(src->atom_max, src->bond_max);

    for (int i =0; i<src->atom_no; i++) {       
        molappend_atom(new_mol, &src->atoms[i]);
    }

    for (int j=0; j<src->bond_no; j++) {
        molappend_bond(new_mol, &src->bonds[j]);
    }
    return new_mol;
}

void molfree( molecule *ptr ) {
    free(ptr->atoms);
    free(ptr->atom_ptrs);

    free(ptr->bonds);
    free(ptr->bond_ptrs);

    free(ptr);
}

void molappend_atom( molecule *molecules, atom *atoms ) {
    if (molecules->atom_no == molecules->atom_max) {
        
        if (molecules->atom_max == 0) {
            molecules->atom_max = 1;
        } else {
            molecules->atom_max *= 2;
        }
        molecules->atoms = realloc(molecules->atoms, molecules->atom_max * sizeof(atom));        
        if (molecules->atoms == NULL) {
            exit(0);
        }   
        molecules->atom_ptrs = realloc(molecules->atom_ptrs, molecules->atom_max * sizeof(atom*));
        if (molecules->atom_ptrs == NULL) {
            exit(0);
        }

        for (int i=0; i<molecules->atom_no; i++) {
            molecules->atom_ptrs[i] = &molecules->atoms[i];
        }
    }
    molecules->atoms[molecules->atom_no] = *atoms;
    molecules->atom_ptrs[molecules->atom_no] = &molecules->atoms[molecules->atom_no];
    molecules->atom_no++;
    
}

void molappend_bond( molecule *molecules, bond *bonds ) {
    if (molecules->bond_no == molecules->bond_max) {
        if (molecules->bond_max == 0) {
            molecules->bond_max = 1;
        } else {
            molecules->bond_max *= 2;
        }
        molecules->bonds = realloc(molecules->bonds, molecules->bond_max * sizeof(bond));
        if (molecules->bonds == NULL) {
            exit(0);
        }
        molecules->bond_ptrs = realloc(molecules->bond_ptrs, molecules->bond_max * sizeof(bond*));
        if (molecules->bond_ptrs == NULL) {
            exit(0);
        }

        for (int i=0; i<molecules->bond_no; i++) {
            molecules->bond_ptrs[i] = &molecules->bonds[i];
        }
    }
    molecules->bonds[molecules->bond_no] = *bonds;
    molecules->bond_ptrs[molecules->bond_no] = &molecules->bonds[molecules->bond_no];
    molecules->bond_no++;
}

int atom_comp(const void *a, const void *b) {     
    atom* one;
    //one = malloc(sizeof(atom));
    atom* two;
    //two = malloc(sizeof(atom));
    one = *(atom**)a;
    two = *(atom**)b;

    float diff = one->z - two->z;
    if (diff<0) {
        return -1;
    }
    else {
        return 1;
    }
    //return(one->z - two->z);
}

int bond_comp(const void *a, const void *b) {     
    bond* one;
    bond* two;
    one = *(bond**)a;
    two = *(bond**)b;

    float diff = one->z - two->z;
    if (diff<0) {
        return -1;
    }
    else {
        return 1;
    }
    //return (one->z - two->z);       //A2 change
}

void molsort( molecule *molecule ) {

    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom *), atom_comp);     
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond *), bond_comp);      
}

void xrotation( xform_matrix xform_matrix, unsigned short deg ) {
    double angle = ((deg * 3.141592654)/180);

    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(angle);
    xform_matrix[1][2] = -sin(angle);

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(angle);
    xform_matrix[2][2] = cos(angle);
}

void yrotation( xform_matrix xform_matrix, unsigned short deg ) {
    double angle = ((deg * 3.141592654)/180);
    //xform_matrix x = { {cos(deg), 0, sin(deg)}, {0, 1, 0}, {-sin(deg), 0, cos(deg)} };

    xform_matrix[0][0] = cos(angle);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(angle);

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = -sin(angle);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(angle);
    
}

void zrotation( xform_matrix xform_matrix, unsigned short deg ) {
    double angle = ((deg * 3.141592654)/180);

    
    xform_matrix[0][0] = cos(angle);
    xform_matrix[0][1] = -sin(angle);
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = sin(angle);
    xform_matrix[1][1] = cos(angle);
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

void mol_xform( molecule *molecule, xform_matrix matrix ) {
    double tempX, tempY, tempZ;
    
    
    for (int i=0; i<molecule->atom_no; i++) {
        tempX = molecule->atoms[i].x;
        tempY = molecule->atoms[i].y;
        tempZ = molecule->atoms[i].z;
        molecule->atoms[i].x = ( (matrix[0][0]* tempX) + (matrix[0][1] * tempY) + (matrix[0][2] * tempZ) );
        molecule->atoms[i].y = ( (matrix[1][0]* tempX) + (matrix[1][1] * tempY) + (matrix[1][2] * tempZ) );
        molecule->atoms[i].z = ( (matrix[2][0]* tempX) + (matrix[2][1] * tempY) + (matrix[2][2] * tempZ) );
    }

    for (int i=0; i<molecule->bond_no; i++) {
        molecule->bonds->atoms = molecule->atoms;       
        compute_coords(molecule->bond_ptrs[i]);
    }
}
