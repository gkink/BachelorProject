#include <stdio.h>
#include <stdlib.h>

typedef unsigned long long int ull;
typedef struct { ull* hashes; size_t size; } HashList;
typedef struct { int frame_num; int distance; } SearchResult;

HashList* hash_list_from_file(char* filename);
void hash_list_free(HashList* hashList);
SearchResult hash_list_search(HashList* haystack, ull needle, int threshold);
