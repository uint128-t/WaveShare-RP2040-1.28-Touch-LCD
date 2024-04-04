from . import *
import os

programs = []
print("Loading programs...")
for module in os.listdir("/programs"):
    if module == "__init__.py" or module[-3:] != ".py":
        continue
    print(f"load {module}")
    exec(f"from . import {module[:-3]} as prgm") # fun
    prgm.id = module[:-3]
    programs.append(prgm)

print(programs)