cimport chashutils

cdef class HashList:
	cdef chashutils.HashList* _hl
	def __cinit__(self, filename):
		cdef bytes filename_bytes = filename.encode()
		cdef char * c_filename = filename_bytes
		self._hl = chashutils.hash_list_from_file(c_filename)
		
	def search(self, query, threshold):
		res = chashutils.hash_list_search(self._hl, <chashutils.ull>query, <int>threshold)
		return (res.frame_num, res.distance)

	def __dealloc__(self):
		chashutils.hash_list_free(self._hl)