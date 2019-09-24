# Experiments

Files modified with the aim of learning how assets are stored for SimCopter and Streets of SimCity or for other purposes.

## Files

To use a modified `.max` file, rename it to match the name of the original file and place it in the appropriate game's `geo` folder (it's advisable to back up the original file first, of course).

### `sim3d2_simcopter_bucket_test_1.max`

* Game: SimCopter
* Original file: `sim3d2.max`
* Changes:
  * Color of face 7 of the bambi bucket mesh (bytes at 217720 and 217725) set to 96 (0x60). For untextured faces (texture file set to 0) that are shaded, inspection of original mesh data indicates that both the group number (the byte at 217720, for this face) and texture index (the byte at 217725) values should be set to the same value.
* Effect:
  * Top face of the bambi bucket is red instead of green. 

### `sim3d2_simcopter_zero_test_1.max`

* Game: SimCopter
* Original file: `sim3d2.max`
* Changes:
  * All bytes in the geometry name table and the duplicate geometry name table (i.e., bytes 853 to 13721, inclusive) set to zero.
  * Color of face 7 of the bambi bucket mesh (bytes at 217720 and 217725) set to 96 (0x60). Easy way to check if the game is using the modified file (top of bambi bucket is red instead of green).
* Effect:
  * Game crashes when loading a city. Error message: "Unable to load resources".

### `sim3d2_simcopter_zero_test_2.max`

* Game: SimCopter
* Original file: `sim3d2.max`
* Changes:
  * All bytes in the geometry name table and the duplicate geometry name table **except** those for the first entry in the name table (i.e., bytes 906 to 13721, inclusive) set to zero.
  * Color of face 7 of the bambi bucket mesh (bytes at 217720 and 217725) set to 96 (0x60). Easy way to check if the game is using the modified file (top of bambi bucket is red instead of green).
* Effect:
  * The game runs normally. See *Notes*, below.
  * Top face of the bambi bucket is red instead of green.

### `sim3d2_simcopter_replacement_test_1.max`

Objective: replace the bambi bucket (ID: 123) with the police car (ID: 285). The ID numbers come from the duplicate geometry name table (see `geom-table-printer.py` in the `tools` directory of this repo).

* Game: SimCopter
* Original file: `sim3d2.max`
* Changes:
  * Replaced object block for the bambi bucket (stored at offset 216595) with a copy of the object block for the police car (stored at offset 316523).
    * Changed the unknown value (stored at offset 216611, between the two always-zero values) from that of the police car (0x00135B10) to that of the bucket (0x0003E422).
      * **Not required:** this can be set to zero with no ill effects.
    * Changed the name (stored at 216619) from that of the police car to that of the bucket.
      * **Not required:** this can be set to zero with no ill effects.
    * Changed the unknown 12 bytes (stored at offset 216707) from that of the police car to that of the bucket.
      * **Required:** otherwise crash and an error message reading "ERROR: unable to get object 123" (123 is the ID of the bucket).
  * Since the object block replacement changed the face size and number of other attributes, additional changes were required.
    * File size (stored at offset 4) changed to 0x000942F7.
      * **Not required:** this can be set to zero with no ill effects.
    * Size of geometry block (stored at offset 833) changed to 0x00093FBA.
      * **Not required:** this can be set to zero with no ill effects.
    * Modifications to first entry of geometry name table (metadata):
      * Total number of rendered vertices (stored at offset 882) changed to 29080 = 0x00007198.
        * **Required:** otherwise in-game error message ("An unrecoverable error occurred during city initialization and SimCopter must quit.") followed by crash and generic "SimCopter has stopped working" error.
      * Total number of faces (stored at offset 894) changed to 8481 = 0x00002121.
        * **Required:** otherwise crash and generic "SimCopter has stopped working" error.
      * Total number of unique vertices (stored at offset 898) changed to 8874 = 0x000022AA.
        * **Required:** otherwise in-game error message ("An unrecoverable error occurred during city initialization and SimCopter must quit.") followed by crash and generic "SimCopter has stopped working" error. 
  * All bytes in the geometry name table and the duplicate geometry name table **except** those for the first entry in the name table (i.e., bytes 906 to 13721, inclusive) set to zero (as in `sim3d2_simcopter_zero_test_2.max`; see above).
* Effect:
  * The bambi bucket is replaced by the police car. Pretty entertaining.

### `sim3d2_simcopter_replacement_test_2.max`

Same as `sim3d2_simcopter_replacement_test_1.max`, but all the changes marked as "not required" have their corresponding values set to zero.

## Notes

* SimCopter appears to use only the first entry in the geometry name table and none of the entries in the duplicate geometry name table (demonstrated by `sim3d2_simcopter_zero_test_1.max` and `sim3d2_simcopter_zero_test_2.max`). The first entry contains metadata rather than details about a specific mesh: it specifies the start of the object block, the number of objects, and the total number of vertices and faces.
* Based on `sim3d2_simcopter_replacement_test_1.max`, the unknown 12 bytes (following the 88-byte name field) in each object block are used by SimCopter when loading an object. Presumably their value is linked to the object IDs since the error message displayed when these 12 bytes are not set correctly refers to the ID.