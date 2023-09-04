import sys
import argparse
import os
import re
from enum import Enum



### Class definitions ###

class Parser_state(Enum):
    NORMAL = 1
    IN_TOOLCHANGE = 2

class Toolchange():

    def __init__(self, start_line, end_line, old_temp, new_temp):
        self.start_line = start_line
        self.end_line = end_line
        self.old_temp = old_temp
        self.new_temp = new_temp

    def __str__(self):
        return "{start}:{end} | {old_temp} -> {new_temp}".format(start = self.start_line, end = self.end_line, old_temp = self.old_temp, new_temp = self.new_temp)

    def __repr__(self):
        return self.__str__()



### Debug Constant Definitions ###

DEBUG = True
DEBUG_ENV = True
LOG = True
DEBUG_PATH = "C:\\Users\\roslan\\Desktop\\mmutest.gcode"
LOG_PATH = "C:\\Users\\roslan\\Desktop\\test.txt"

# When switching from colder material to hotter material we:
# - Insert M109 S<X>(Wait for hotend temp) (for new hotter temperature) before last little wipe sweep on wipe tower before the hotend moves to the object again



# When switchting from hotter material to colder material we:
# - Replace existing M104 S<X> with the same temperature to prevent from cooling while the cold material is still loaded
# - Insert M104 S<X> right before TOOLCHANGE_WIPE_STR to wipe the last bit of old material with the hot temperature while cooling down when the material transition happens in the nozzle
# - Insert M109 S<X> (Wait for hotend temp) before last little wipe sweep on wipe tower before the hotend moves to the object again



### Constant Definitions ###

TOOLCHANGE_START_STR = "; CP TOOLCHANGE START"
TOOLCHANGE_LOAD_STR = "; CP TOOLCHANGE LOAD"
TOOLCHANGE_UNLOAD_STR = "; CP TOOLCHANGE UNLOAD"
TOOLCHANGE_WIPE_STR = "; CP TOOLCHANGE WIPE"
TOOLCHANGE_END_STR = "; CP TOOLCHANGE END"


# Set debug environment
if DEBUG_ENV:
    os.environ["SLIC3R_PRINTER_MODEL"] = "MK3SMMU3"
    os.environ["SLIC3R_FIRST_LAYER_TEMPERATURE"] = "215,230,215,215,215"



### Functions ###

def write_log_line(line):
    if LOG:
        with open(LOG_PATH, 'a') as file:
            file.write(line + "\n")



def extract_toolchanges(gcode_lines) -> list:
    """Extracts toolchanges from a list of gcode lines (strings)

    Args:
        gcode_lines (list): A list of strings that represent the lines in the gocde

    Returns:
        list: A list containing Toolchanges
    """

    result = []
    last_seen_temp = 0
    current_seen_temp = 0
    toolchange_start_line = 0
    toolchange_end_line = 0
    current_parser_state = Parser_state.NORMAL

    for i in range(len(gcode_lines)):
        cur_line = gcode_lines[i]

        # Extract found temperatures
        if (cur_line.startswith("M104")):
            regex_match = re.search(r'S\d+', cur_line)
    
            str_temp = regex_match.group(0)[1:]
            last_seen_temp = current_seen_temp
            current_seen_temp = int(str_temp)

        if (cur_line.startswith(TOOLCHANGE_START_STR)):
            toolchange_start_line = i
            current_parser_state = Parser_state.IN_TOOLCHANGE

        if (cur_line.startswith(TOOLCHANGE_END_STR)):
            current_parser_state = Parser_state.NORMAL
            toolchange_end_line = i
            result.append(Toolchange(toolchange_start_line, toolchange_end_line, last_seen_temp, current_seen_temp))

    return result



def init_args():
    """Initializes the ArgumentParser with all the arguments that we need for this script

    Returns:
        _type_: _description_
    """
    parser = argparse.ArgumentParser("argument_parser")
    parser.add_argument("gcode_path", help="The path of the source GCODE", default="-", type=str)
    return parser.parse_args()

### End Functions ###



### Start of script ###

# Create global variables on global scope
file_content = []
output_file_content = []
temps_str = str(os.getenv("SLIC3R_TEMPERATURE"))

# Initialize Argument Parser
if not DEBUG:
    scriptArgs = init_args()
    gcdode_source_path = scriptArgs.gcode_path
else:
    gcdode_source_path = DEBUG_PATH


# Check if this even an MMU printer
printer_model = str(os.getenv("SLIC3R_PRINTER_MODEL"))
write_log_line("Printer model: {printer}".format(printer = printer_model))
if not DEBUG and printer_model != "MK3SMMU3":
    write_log_line("Exiting script because this printer does not have an MMU")
    sys.exit()

# Read source GCODE into list
with open(gcdode_source_path) as file:
    file_content = file.readlines()
    output_file_content = file_content.copy()
    write_log_line("Done reading GCODE: {ln} lines".format(ln = len(file_content)))

# Print out environment values
for name, value in os.environ.items():
    write_log_line(name)
    write_log_line(value)

# Iterate over GCODE and detect tool changes and their mode
toolchanges_list = extract_toolchanges(file_content)

write_log_line("GCODE has {num} toolchanges with different temps".format(num = len(toolchanges_list)))
write_log_line(str(toolchanges_list))

# Iterate over Toolchanges to optimize them
for toolchange in toolchanges_list:
    if toolchange.old_temp < toolchange.new_temp:
    # Change from cold to hot
    

    elif toolchange.old_temp > toolchange.new_temp:
    # Change from hot to cold

# Write GCODE inplace
with open(gcdode_source_path, "w") as output_file:
    output_file.writelines(output_file_content)



### End of Script ###




#        if (current_parser_state == Parser_state.IN_TOOLCHANGE):
#            # We are changing temperatures for a toolchange
#
#            if current_seen_temp > last_seen_temp:
#                # Colder to Hotter
#                output_file_content[toolchange_start_line] = output_file_content[toolchange_start_line].strip() + " - BetterMMU: {old_temp} -> {new_temp}".format(old_temp = last_seen_temp, new_temp = current_seen_temp) + "\n"
#
#            elif current_seen_temp < last_seen_temp:
#                # Hotter to colder
#                output_file_content[toolchange_start_line] = output_file_content[toolchange_start_line].strip() + " - BetterMMU: {old_temp} -> {new_temp}".format(old_temp = last_seen_temp, new_temp = current_seen_temp) + "\n"
