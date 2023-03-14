#ifndef CHECK_H
#define CHECK_H

#include <string>
using namespace std;

#include "pdb.h"

// given the paths to two chains, return if the chains are in contact.


/**
 * @brief Checks if two chains are in contact.
 * @note requires that the new chains be in separate files but derived from the same multimeric assembly
 * 
 * @param chainPathA path to the first chain
 * @param chainPathB path to the second chain
 * @param threshNumPairsContact the minimum number of residue pairs, non-exclusive, between the chains near enough to constitute a contact
 * @param threshDistContactAngstroms the maximum distance between residues to constitue a contacting pair
 * @returns bool True for chains meeting the contact criteria or False otherwise
 */
bool check_chains_contact(string chainPathA, string chainPathB, int threshNumPairsContact, float threshDistContactAngstroms);



#endif /* CHECK_H */