"""
build_lib_power.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

Generate generic power symbols for supply and ground nets.
"""
from __future__ import print_function, division
import sys
import os.path

PWR_NAMES = [
    "VCC", "VDD", "AVCC", "1v2", "1v8", "3v3", "5v", "VBATT", "VSHORE",
]

GND_NAMES = [
    "GND", "AGND", "DGND", "PGND", "CHASSIS", "EARTH"
]


def gnd(name):
    out = []
    out.append('#\n# {}\n#'.format(name))
    out.append('DEF {} #PWR 0 40 N N 1 F P'.format(name))
    out.append('F0 "#PWR" -130 40 50 H I L CNN')
    out.append('F1 "{}" 0 -100 50 H V C CNN'.format(name))
    out.append('DRAW')
    out.append('P 2 0 1 0 0 0 0 -30 N')
    out.append('P 4 0 1 0 -30 -30 30 -30 0 -60 -30 -30 f')
    out.append('X {} 1 0 0 0 L 50 50 1 1 W N'.format(name))
    out.append('ENDDRAW\nENDDEF\n#\n')
    return out


def pwr(name):
    out = []
    out.append('#\n# {}\n#'.format(name))
    out.append('DEF {} #PWR 0 40 N N 1 F P'.format(name))
    out.append('F0 "#PWR" 0 110 50 H I L CNN')
    out.append('F1 "{}" 0 90 50 H V C CNN'.format(name))
    out.append('DRAW')
    out.append('P 2 0 1 0 0 50 20 20 N')
    out.append('P 3 0 1 0 0 0 0 50 -20 20 N')
    out.append('X {} 1 0 0 0 L 50 50 1 1 W N'.format(name))
    out.append('ENDDRAW\nENDDEF\n#\n')
    return out


def main(libpath, verify=False):
    out = []
    out.append("EESchema-LIBRARY Version 2.3")
    out.append("#encoding utf-8\n")
    out.append("#========================================================")
    out.append("# Automatically generated by agg-kicad build_lib_power.py")
    out.append("# See github.com/adamgreig/agg-kicad")
    out.append("#========================================================\n")

    for name in PWR_NAMES:
        out += pwr(name)
    for name in GND_NAMES:
        out += gnd(name)

    out.append('# End Library\n')
    lib = "\n".join(out)

    # Check if the library has changed
    if os.path.isfile(libpath):
        with open(libpath) as f:
            oldlib = f.read()
            if lib == oldlib:
                return True

    # If so, validation has failed or update the library file
    if verify:
        return False
    else:
        with open(libpath, "w") as f:
            f.write(lib)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[2] == "--verify":
        if main(sys.argv[1], verify=True):
            print("OK: libs up-to-date.")
            sys.exit(0)
        else:
            print("Error: lib not up-to-date.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: {} <lib path> [--verify]".format(sys.argv[0]))
        sys.exit(1)
