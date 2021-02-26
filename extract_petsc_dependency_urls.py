import os
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, os.path.abspath("petsc/config/BuildSystem"))
sys.path.insert(0, os.path.abspath("petsc/config"))

from config.framework import Framework

f = Framework()

import config.packages

p = config.packages.__path__[0]
p = Path(p)
sources = p.glob("*.py")

from importlib import import_module

schemes = Counter()
for source in sorted(sources):
    m = f"config.packages.{source.stem}"
    m = import_module(m)
    c = None
    try:
        c = m.Configure(f)
    except AttributeError:
        pass
    if c and c.download:
        print()
        print(c.package)
        if c.gitcommit:
            print(f"    # git ref: {c.gitcommit}")
        for d in c.download:
            print(f"    {d}")
            scheme, rest = d.split(":", 1)
            assert rest.startswith("//"), f"expected {scheme}://, saw {d}"
            schemes[scheme] += 1
    else:
        print()
        print(f"# no downloads for {source.stem}")

print()
scheme_counts = schemes.most_common()
msg = "# {count:" + str(len(str(scheme_counts[0][1]))) + "}  {scheme}"
for scheme, count in scheme_counts:
    print(msg.format(count=count, scheme=scheme))
