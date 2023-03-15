#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>

#include "include/cxxopts-3.1.1/include/cxxopts.hpp"

using namespace std;


struct Coordinate {
    double x;
    double y;
    double z;
};



double dist_between_coor(Coordinate& c1, Coordinate& c2) {
    return sqrt( pow(c1.x - c2.x, 2) +  pow(c1.y - c2.y, 2) + pow(c1.z - c2.z, 2) );
}


double get_num_from_line(string line, int start_index, int num_char) {
    string current_residue = line.substr(start_index, num_char);
    return atof(current_residue.c_str());
}


int count_residues(const string& chain_path) {
    ifstream pdbfile(chain_path);

    int count = 0;

    int current_residue = 0;
    int last_residue = -1;
    
    string atom_type;
    bool seen_ca_or_cb = false;
    
    for(string line; getline(pdbfile, line);) {

        // skip line if line does not start with ATOM or HETATM
        if (line.find("ATOM") != 0 and line.find("HETATM") != 0) {
            continue;
        }

        current_residue = (int)get_num_from_line(line, 22, 4);

        if (current_residue != last_residue and seen_ca_or_cb) {
            count++;
            seen_ca_or_cb = false;
        }
        
        // if cb or ca
        atom_type = line.substr(12, 3);
        if (atom_type.find("CB") != string::npos or atom_type.find("CA") != string::npos) {
            seen_ca_or_cb = true;
        }

        last_residue = current_residue;
    }

    if (seen_ca_or_cb) {
        count++;
    }

    return count;

}


Coordinate* get_chain_coordinates(const string& chain_path, int num_residues) {
    ifstream pdbfile(chain_path);

    Coordinate* coors = new Coordinate[num_residues];
    int coors_index = 0;
    
    int last_residue = -1;
    int current_residue = 0;

    Coordinate CA;
    Coordinate CB;

    bool CA_updated = false;
    bool CB_updated = false;
    string atom_type;

    for (string line; getline(pdbfile, line);) {
        // skip line if line does not start with ATOM or HETATM
        if (line.substr(0, 4) != "ATOM" and line.substr(0,6) != "HETATM") {
            continue;
        }

        current_residue = (int)get_num_from_line(line, 22, 4);

        if (current_residue != last_residue) {
            if (CB_updated) {
                coors[coors_index++] = CB;
            }
            else if (CA_updated) {
                coors[coors_index++] = CA;
            }

            CB_updated = false;
            CA_updated = false;
            last_residue = current_residue;
        }

        atom_type = line.substr(12, 3);
        if (atom_type.find("CB") != string::npos) {
            CB.x = get_num_from_line(line, 30, 8);
            CB.y = get_num_from_line(line, 38, 8);
            CB.z = get_num_from_line(line, 46, 8);
            CB_updated = true;
        }
        else if (atom_type.find("CA") != string::npos) {
            CA.x = get_num_from_line(line, 30, 8);
            CA.y = get_num_from_line(line, 38, 8);
            CA.z = get_num_from_line(line, 46, 8);
            CA_updated = true;
        }

        
    }

    if (CB_updated) {
        coors[coors_index++] = CB;
    }
    else if (CA_updated) {
        coors[coors_index++] = CA;
    }
    

    return coors;
}



bool in_contact(const string& chain1_path, const string& chain2_path, double distance_maximum, int count_minimum) {

    int chain1_num_residues = count_residues(chain1_path);
    int chain2_num_residues = count_residues(chain2_path);

    Coordinate* chain1_coors = get_chain_coordinates(chain1_path, chain1_num_residues);
    Coordinate* chain2_coors = get_chain_coordinates(chain2_path, chain2_num_residues);

    int count = 0;

    for (int i = 0; i < chain1_num_residues; i++) {
        for (int j = 0; j < chain2_num_residues; j++) {
            double dist = dist_between_coor(chain1_coors[i], chain2_coors[j]);
            if (dist <= distance_maximum) {
                count++;
            }

            if (count >= count_minimum) {
                goto double_break;
            }

        }
    }

double_break:
    delete chain1_coors;
    delete chain2_coors;

    return (count >= count_minimum);
}




int main(int argc, char** argv) {

    cxxopts::Options options("PDB chains contact checker", 
        "checks if two PDB chains, of the same PDB entry "
        "and split into their own files, are in contact "
        "according to the given definition of being in contact."
    );

    options.add_options()
        ("c1,chain1-path", "path to chain1's pdb file", cxxopts::value<string>())
        ("c2,chain2-path", "path to chain2's pdb file", cxxopts::value<string>())
        ("d,threshold-max-contact-distance", "The maximum distance, in angstroms, between residues to be considered in contact", 
            cxxopts::value<double>()->default_value("8"))
        ("n,threshold-min-pairs", "The minimum number of residue pairs between chains, non-exclusive, that must be in contact for the chains to be considered in contact", 
            cxxopts::value<int>()->default_value("10"))
        ("h,help", "Print usage")
    ;

    auto result = options.parse(argc, argv);

    if (result.count("help"))
    {
      cout << options.help() << endl;
      exit(0);
    }

    const string chain1 = result["chain1-path"].as<string>();
    const string chain2 = result["chain2-path"].as<string>();
    double distance_thresh = result["threshold-max-contact-distance"].as<double>();
    int num_pairs_thresh = result["threshold-min-pairs"].as<int>();

    bool contacting = in_contact(chain1, chain2, distance_thresh, num_pairs_thresh);

    if (contacting) {
        return 1;
    }
    return 0;

}