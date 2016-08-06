#include <fstream>
#include <vector>
#include <iostream>
#include <bitset>

#include <string.h>
#include <stdlib.h>

typedef struct { int hi; int lo; } hash64_t;
typedef unsigned long long ull;

using namespace std;

void read_hashes(ifstream &in, vector<hash64_t> &vec) {
    hash64_t buffer;
    while (in.read((char *)(&buffer), sizeof(hash64_t))) {
        hash64_t h = (hash64_t) buffer;
        vec.push_back(h);
    }
}

int hamming_distance(hash64_t a, hash64_t b) {
    return __builtin_popcount(a.lo ^ b.lo) + __builtin_popcount(a.hi ^ b.hi); 
}

void fill_in_buckets(vector<size_t> (*buckets)[57][256], vector<hash64_t> &descriptors) {
    size_t num_descriptors = descriptors.size();
    for (size_t i = 0; i < num_descriptors; ++i) {
        ull ll = ((ull)(descriptors[i].hi) << 32) | descriptors[i].lo;
        for (int j = 0; j < 57; ++j) {
            size_t index = (ll >> (56-j)) & 0xff;
            (*buckets)[j][index].push_back(i);
        }
    }
}

int main(int argc, char **argv) {    
    vector<hash64_t> descriptors;
    vector<int> delims;
    vector<size_t> buckets[57][256];

    for (int i = 1; i < argc; ++i) {
        ifstream in (argv[1], ios::binary);
        read_hashes(in, descriptors);
        delims.push_back(descriptors.size());
        in.close();
    }

    //vector<size_t> (*p_buckets)[57][256] = &buckets;
    //fill_in_buckets(p_buckets, descriptors);

    // while (1) {
    //     unsigned int a,b,c;
    //     string binary;
    //     cin >> a >> b;
    //     if (a == 0 && b == 0) break;
    //     ull query = (ull)(a) << 32 | b;

    //     binary = bitset<64>(query).to_string();
    //     cout << binary.substr(0,32) << " " << binary.substr(32) << endl;

    //     for (int i = 0; i < 57; ++i) {
    //         size_t index = (query >> (56-i)) & 0xff;
    //         vector<size_t> indices = buckets[i][index];
    //         size_t l = indices.size();
    //         if (l) {
    //             cout << "index: " << index << endl;
    //             cout << "length: " << l << endl;
    //             cout << "how many to print? ";
    //             cin >> c;
    //             for (int j = 0; j < c; ++j) {
    //                 hash64_t hash = descriptors[indices[j]];
    //                 ull ll = ((ull)(hash.hi) << 32) | hash.lo;
    //                 binary = bitset<64>(ll).to_string();
    //                 cout << binary.substr(0,32) << " " << binary.substr(32) << endl;
    //             }
    //         }
    //     }
    // }

    // for (int i = 0; i < 57; ++i) {
    //     cout << "index: " << i << endl;
    //     for (int j = 0; j < 256; ++j) {
    //         cout << "suffix: " << bitset<8>(j).to_string() << endl << endl;
    //         vector<size_t> curr_vec = buckets[i][j];
    //         for (int k = 0; k < curr_vec.size(); ++k) {
    //             hash64_t hash = descriptors[k];
    //             ull ll = ((ull)(hash.hi) << 32) | hash.lo;
    //             cout << bitset<64>(ll).to_string() << " " << k << endl;
    //         }
    //     }
    // }
    
    for (int i = 0; i < descriptors.size(); ++i) {
        hash64_t hash = descriptors[i];
        ull ll = ((ull)(hash.hi) << 32) | hash.lo;
        cout << bitset<64>(ll).to_string() << endl;
    }

    return 0;
}
