# Set appropriately before running.
filePath = "C:/SimCopter-Stuff/SIMCOPTER/geo/sim3d1.max"

offsetGeomTableStart = 829 # This is stored earlier in the file, but it's always 829.
lengthGeomTableEntry = 53 # 17 + 9*4
lengthDuplicateGeomTableEntry = 36 # 9*4 (no name, no object count, prepended ID)

# Tally these just to check them against the values in the first entry in the name table.
totalRenderedVertices = 0
totalFaces = 0
totalUniqueVertices = 0

nameTableHeadings = ["Name", "Offset", "Count", "Zero", "Vertex Count", "Zero", "Zero", "Face Count", "Unique Vertex Count", "Zero"];
nameTable = []

# Don't bother storing the always-zero bytes.
duplicateNameTableHeadings = ["ID", "Offset", "Vertex Count", "Face Count", "Unique Vertex Count"]
duplicateNameTable = []

with open(filePath, "rb") as file:
    data = file.read()

    pos = offsetGeomTableStart

    # Skip "GEOM".
    pos += 4
    
    sizeGeomBlock = int.from_bytes(data[pos:pos+4], byteorder='little')
    pos += 4
    
    entryCount = int.from_bytes(data[pos:pos+4], byteorder='little')
    pos +=4
    
    geomCount = int.from_bytes(data[pos:pos+4], byteorder='little')
    pos += 4
    
    offsetStartNameTable = int.from_bytes(data[pos:pos+4], byteorder='little')
    pos += 4
    
    offsetStartDuplicateNameTable = int.from_bytes(data[pos:pos+4], byteorder='little')
    pos += 4

    print("=== GEOMETRY HEADER DATA ===\n"
          "Size of geometry block: {0}\n"
          "Number of entries in table: {1}\n"
          "Number of entries in duplicate table: {2}\n"
          "Start of table: {3}\n"
          "Start of duplicate table: {4}".format(sizeGeomBlock, entryCount, geomCount, offsetStartNameTable, offsetStartDuplicateNameTable))

    pos2 = pos + entryCount*lengthGeomTableEntry;

    for i in range(entryCount):
        # Names are null-terminated. Subsequent bytes within the range allocated for the name are garbage.
        name = data[pos:pos+17].partition(b'\0')[0].decode("ascii", "ignore")
        pos += 17

        offsetIntoMeshTable = int.from_bytes(data[pos:pos+4], byteorder='little')
        pos += 4

        # 1 = object; other values indicate that name is the filename.
        quantity = int.from_bytes(data[pos:pos+4], byteorder='little')
        pos += 4

        alwaysZero1 = int.from_bytes(data[pos:pos+4], byteorder='little')
        pos += 4

        vertexCountWithDuplicates = int.from_bytes(data[pos:pos+4], byteorder='little')
        pos += 4

        alwaysZero2 = int.from_bytes(data[pos:pos+4], byteorder='little')
        pos += 4

        alwaysZero3 = int.from_bytes(data[pos:pos+4], byteorder='little')
        pos += 4

        faceCount = int.from_bytes(data[pos:pos+4], byteorder='little')
        pos += 4

        vertexCount = int.from_bytes(data[pos:pos+4], byteorder='little')
        pos += 4
        
        alwaysZero4 = int.from_bytes(data[pos:pos+4], byteorder='little')
        pos += 4

        if i != 0:
            totalRenderedVertices += vertexCountWithDuplicates
            totalFaces += faceCount
            totalUniqueVertices += vertexCount

        nameTable.append([name, offsetIntoMeshTable, quantity, alwaysZero1, vertexCountWithDuplicates, alwaysZero2, alwaysZero3, faceCount, vertexCount, alwaysZero4])

        if i != 0: # First entry in table (metadata) isn't repeated in duplicate table.

            # Instead of name, duplicate table has an ID (might not be an ID, of course).
            dup_id = int.from_bytes(data[pos2:pos2+4], byteorder='little')
            pos2 += 4

            dup_offsetIntoMeshTable = int.from_bytes(data[pos2:pos2+4], byteorder='little')
            pos2 += 4

            # No object count in duplicate table. (They'd all be set to 1.)

            # Skip an always-zero byte.
            pos2 += 4

            dup_vertexCountWithDuplicates = int.from_bytes(data[pos2:pos2+4], byteorder='little')
            pos2 += 4

            # Skip two always-zero bytes.
            pos2 += 4
            pos2 += 4

            dup_faceCount = int.from_bytes(data[pos2:pos2+4], byteorder='little')
            pos2 += 4

            dup_vertexCount = int.from_bytes(data[pos2:pos2+4], byteorder='little')
            pos2 += 4

            # Skip an always-zero byte.
            pos2 += 4

            duplicateNameTable.append([dup_id, dup_offsetIntoMeshTable, dup_vertexCountWithDuplicates, dup_faceCount, dup_vertexCount])
            
print("=== COMPUTED TOTALS ===\n"
      "(should match first entry in name table)\n"
      "\tRendered vertices: {0}\n"
      "\tFaces: {1}\n"
      "\tUnique vertices: {2}".format(totalRenderedVertices, totalFaces, totalUniqueVertices))

print("=== GEOMETRY NAME TABLE ===")
print(" | ".join(nameTableHeadings))
for entry in nameTable:
    print("{0:_<17} | {1:>7} | {2:>3} | {3} | {4:>5} | {5} | {6} | {7:>5} | {8:>5} | {9}".format(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8], entry[9]))

print("=== DUPLICATE GEOMETRY NAME TABLE ===") # Only new info in this table is the ID number.
print(" | ".join(duplicateNameTableHeadings))
for entry in duplicateNameTable:
    print("{0:>5} | {1:>7} | {2:>5} | {3:>5} | {4:>5}".format(entry[0], entry[1], entry[2], entry[3], entry[4]))
