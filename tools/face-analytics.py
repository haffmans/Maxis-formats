#!/usr/bin/env python3

"""
Get some basic FACE statistics from the sim3d*.max files to discover the flags/unknown bytes meanings.

Run from the SimCopter/geo directory.
"""

entries = dict()
faces = 0
files = ['sim3d1.max', 'sim3d2.max', 'sim3d3.max']

for filename in files:
    with open('sim3d1.max', 'rb') as f:
        data = f.read()
        offset = 0
        fsize = len(data)

        for offset in range(len(data) - 4):
            marker = data[offset:offset+4]

            if marker == b'FACE':
                # Offset additions: 'FACE' marker (4), size (4), num vertices (2) ...
                flags = int.from_bytes(data[offset+4+4+2:offset+4+4+2+2], byteorder='little')
                # ... flags (2), is_light (2), face_group (4)
                unknown = data[offset+4+4+2+2+2+4]
                t = (flags, unknown)
                if t not in entries:
                    entries[t] = 0
                entries[t] += 1
                faces += 1

print("Faces: {0}".format(faces))
cnt = 0
for t in sorted(entries):
    print("Flags {0:5d} {0:016b}, Unknown 0x{1:02x}: {2}".format(t[0], t[1], entries[t]))
    cnt += entries[t]

for t in sorted(entries, key=lambda t: (t[1], t[0])):
    print("Unknown 0x{1:02x}, Flags {0:5d} {0:016b}: {2}".format(t[0], t[1], entries[t]))
    cnt += entries[t]
