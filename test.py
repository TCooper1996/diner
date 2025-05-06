import ctypes.util
import os
import sys

print("PYTHON EXECUTABLE:", sys.executable)
print("ENVIRONMENT PATH:")
print(os.environ.get("PATH", ""))
print("DYLD_LIBRARY_PATH:", os.environ.get("DYLD_LIBRARY_PATH"))
print("PKG_CONFIG_PATH:", os.environ.get("PKG_CONFIG_PATH"))

print("\nFinding Cairo using ctypes.util.find_library:")
print("Result:", ctypes.util.find_library("cairo"))