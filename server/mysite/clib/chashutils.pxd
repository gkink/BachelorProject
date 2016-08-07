cdef extern from "hashutils.h":	
	ctypedef unsigned long long int ull;
	ctypedef struct HashList:
		ull* hashes
		size_t size
	ctypedef struct SearchResult:
		int frame_num
		int distance

	HashList* hash_list_from_file(char* filename)
	SearchResult hash_list_search(HashList* haystack, ull needle, int threshold)
	void hash_list_free(HashList* hashList)
