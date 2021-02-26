import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("petsc/config/BuildSystem"))
sys.path.insert(0, os.path.abspath("petsc/config"))

from config.framework import Framework

f = Framework()

import config.packages

p = config.packages.__path__[0]
p = Path(p)
sources = p.glob("*.py")

from importlib import import_module

for source in sorted(sources):
    m = "config.packages." + source.stem
    m = import_module(m)
    c = None
    try:
        c = m.Configure(f)
    except AttributeError:
        pass
    if c and c.download:
        print()
        print(c.package)
        for d in c.download:
            print("    ", d)
    else:
        print()
        print("# no downloads for " + source.stem)
