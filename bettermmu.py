import sys
import argparse



# When switching from colder material to hotter material we:
# - Insert M109 S<X>(Wait for hotend temp) before last little wipe sweep on wipe tower before the hotend moves to the object again



# When switchting from hotter material to colder material we:
# - Replace existing M104 S<X> with the same temperature to prevent from cooling while the cold material is still loaded
# - Insert M104 S<X> right before TOOLCHANGE_WIPE_STR to wipe the last bit of old material with the hot temperature while cooling down when the material transition happens in the nozzle
# - Insert M109 S<X> (Wait for hotend temp) before last little wipe sweep on wipe tower before the hotend moves to the object again

debug = True
DEBUG_PATH = "C:\\Users\\roslan\\Desktop\\mmutest.gcode"

TOOLCHANGE_START_STR = "; CP TOOLCHANGE START"
TOOLCHANGE_UNLOAD_STR = "; CP TOOLCHANGE UNLOAD"
TOOLCHANGE_WIPE_STR = "; CP TOOLCHANGE WIPE"
TOOLCHANGE_END_START = "; CP TOOLCHANGE END"


file_content = ()

# Initialize Argument Parser
if not debug:
    parser = argparse.ArgumentParser("argument_parser")
    parser.add_argument("gcode_path", help="The path of the source GCODE", default="-", required = False, type=str)
    args = parser.parse_args()
    gcdode_source_path = args.gcode_path

if debug:
    gcdode_source_path = DEBUG_PATH

# Read source GCODE into list
with open(gcdode_source_path) as file:
    file_content = file.readlines()
    print(file_content[300])




