#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>

using namespace std;


struct Coordinate {
    double x;
    double y;
    double z;
};



double dist_between_coor(Coordinate* c1, Coordinate* c2) {
    return sqrt( pow(c1->x - c2->x, 2) +  pow(c1->y - c2->y, 2) + pow(c1->z - c2->z, 2) );
}


double get_num_from_line(string line, int start_index, int num_char) {
    string current_residue = line.substr(start_index, num_char);
    return atof(current_residue.c_str());
}


int count_valid_residues(const string& chain_path) {
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
    
    pdbfile.close();
    return coors;
}




int count_contacts(const string& chain1_path, const string& chain2_path, double distance_maximum) {

    const int chain1_size = count_valid_residues(chain1_path);
    const int chain2_size = count_valid_residues(chain2_path);

    Coordinate* chain1_coors = get_chain_coordinates(chain1_path, chain1_size);
    Coordinate* chain2_coors = get_chain_coordinates(chain2_path, chain2_size);

    int count = 0;

    for (int i = 0; i < chain1_size; i++) {
        for (int j = 0; j < chain2_size; j++) {
            double dist = dist_between_coor(chain1_coors+i, chain2_coors+j);
            if (dist <= distance_maximum) {
                count++;
            }
        }
    }

    delete chain1_coors;
    delete chain2_coors;
    return count;
}




int main(int argc, char** argv) {

    if (argc != 5) {
        cout << "usage: ./check_contact.exe <infile> <outfile> <contact-definition-angstroms> <contact-definition-num-residue-pairs>" << endl;
        return -1;
    }

    const string infilename = argv[1];
    const string outfilename = argv[2];
    const double dist_max = atof(argv[3]);
    const int count_min = atoi(argv[4]);

    ifstream infile_stream(infilename);
    ofstream outfile_stream(outfilename);

    string chain1path, chain2path;
    while(infile_stream >> chain1path >> chain2path) {
        int num_contacts = count_contacts(chain1path, chain2path, dist_max);
        bool contacting = num_contacts >= count_min;
        outfile_stream << contacting << "\t" << num_contacts << endl;
    }
    
    infile_stream.close();
    outfile_stream.close();

    return 0;

}
