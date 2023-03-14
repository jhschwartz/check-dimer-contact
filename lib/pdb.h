#ifndef TYPES_H
#define TYPES_H

#include <string>
#include <vector>
using namespace std;

/**
 * @brief struct of a 3D coordinate
 */
struct Coordinate {
    float x, y, z;
};


/**
 * @brief struct to represent a single atom from a PDB file.
 */
struct Atom {
    Coordinate coor; // the coordinates of the atom
    string atomType; // the atom type, e.g. "CB" or "N". Only those in the PDB standard are valid.
    string record; // the listed atom record in the PDB, e.g. "ATOM" or "HETATM"
};



/**
 * @brief class to represent individual residues and their member atoms
 */
class Residue {
public:
    vector<Atom> atoms; // every Atom member of the residue
    string aaType3L; // the amino acid type in 3-letter form, e.g. "GLY"
    string aaType1L; // the amino acid type in 1-letter form, e.g. "G"

    /**
     * @brief gets the distance between two residues
     * @return float the distance between the residues
     * @note uses cbeta when available, calphas as a backup, and NULL if neither available for one residue.
     */
    static float distance(Residue r1, Residue r2);
private: 

    /**
     * @brief converts amino acid 3-letter code to 1-letter code, e.g. "GLY" to "G"
     * 
     * @param aaType3L a valid 3-letter amino acid code
     * @return string the corresponding 1-letter amino acid code
     */
    string aa3to1(string aaType3L);
};

/**
 * @brief class to represent a chain from a PDB file
 */
class Chain {
public:
    vector<Residue> residues;
    string chainNameActual;
    string chainNameFile;

    /**
     * @brief Get the coordinates at the extremes of the chain
     * @note for each residue, uses cbetas, calphas as a backup, and skips residues with neither
     * 
     * @return vector<Coordinate> the coordinates at the extremes, in this order: [minX, maxX, minY, maxY, minZ, maxZ]
     */
    vector<Coordinate> getExtrema();
}

#endif /* TYPES_H */