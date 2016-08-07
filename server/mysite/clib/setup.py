import os
import sys

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


try:
    print("building libhashutils.a")
    assert os.system("gcc -shared -fPIC -c hashutils.c -o hashutils.o") == 0
    assert os.system("ar rcs libhashutils.a hashutils.o") == 0
except:
    if not os.path.exists("libhashutils.a"):
        print("Error building external library, please create libhashutils.a manually.")
        sys.exit(1)

ext_modules = cythonize([
    Extension("hash_utils",
              sources=["hash_utils.pyx"],
              include_dirs=[os.getcwd()],  # path to .h file(s)
              library_dirs=[os.getcwd()],  # path to .a or .so file(s)
              libraries=['hashutils'])
])

setup(
    name='Demos',
    ext_modules=ext_modules,
)