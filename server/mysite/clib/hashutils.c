#include "hashutils.h"

HashList* hash_list_from_file(char* filename) {
	FILE *f;
	size_t f_size;
	HashList* hashList;

	f = fopen(filename, "rb");

	fseek(f, 0L, SEEK_END);
	f_size = ftell(f);
	rewind(f);

	hashList = malloc(sizeof(HashList));
	hashList->hashes = malloc(f_size);
	hashList->size = f_size / sizeof(ull);
	fread(hashList->hashes, f_size, 1, f);

	fclose(f);

	return hashList;
}

void hash_list_free(HashList* hashList) {
	free(hashList->hashes);
	free(hashList);
}

SearchResult hash_list_search(HashList* haystack, ull needle, int threshold) {
	size_t i, len;
	int curr_dist = threshold + 1;
	int curr_frame_num = -1;

	len = haystack->size;
	for (i = 0; i < len; ++i) {
		int distance = __builtin_popcountll(needle ^ haystack->hashes[i]);
		if (distance < curr_dist) {
			curr_dist = distance;
			curr_frame_num = i;
		}
	}
	SearchResult result = { .frame_num=curr_frame_num, .distance=curr_dist };

	return result;
}

int main(int argc, char **argv) {
	// char* filename = "/home/gosip/Documents/MovieShazam/BachelorProject/cpp/pHash/Pulp_Fiction.ds";
	// ull needle = 15791986208310520790;
	// HashList* hl;

	// hl = hash_list_from_file(filename);
	// SearchResult result = hash_list_search(hl, needle, 10);
	// printf("frame_num: %d, distance: %d\n", result.frame_num, result.distance);
	// hash_list_free(hl);

	return 0;
}