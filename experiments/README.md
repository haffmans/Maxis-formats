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
  * Game crashes when loading a city. Error message: "Unable to load resources"

### `sim3d2_simcopter_zero_test_2.max`

* Game: SimCopter
* Original file: `sim3d2.max`
* Changes:
  * All bytes in the geometry name table and the duplicate geometry name table **except** those for the first entry in the name table (i.e., bytes 906 to 13721, inclusive) set to zero.
  * Color of face 7 of the bambi bucket mesh (bytes at 217720 and 217725) set to 96 (0x60). Easy way to check if the game is using the modified file (top of bambi bucket is red instead of green).
* Effect:
  * The game runs normally. See *Notes*, below.
  * Top face of the bambi bucket is red instead of green.

## Notes

* SimCopter appears to use only the first entry in the geometry name table and none of the entries in the duplicate geometry name table (demonstrated by `sim3d2_simcopter_zero_test_1.max` and `sim3d2_simcopter_zero_test_2.max`). The first entry contains metadata rather than details about a specific mesh: it specifies the start of the object block, the number of objects, and the total number of vertices and faces.