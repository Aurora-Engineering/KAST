# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"

"""
print_io.py
Helper script used by sim.py to print out simulation data with pretty colors
"""

#############################     COLORS    #############################
# Static class to hold color constants
class bcolors:
    HEADER = '\033[96m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Global colors dictionary
scolors = {'HEADER' : bcolors.HEADER,
           'OKBLUE' : bcolors.OKBLUE,
           'OKGREEN' : bcolors.OKGREEN,
           'WARNING' : bcolors.WARNING,
           'FAIL' : bcolors.FAIL,
           'ENDC' : bcolors.ENDC,
           'BOLD' : bcolors.BOLD,
           'UNDERLINE' : bcolors.UNDERLINE}

# Global dictionary for STATUS -> COLOR
status_colors = {'GREEN' : bcolors.OKGREEN,
                 'YELLOW' : bcolors.WARNING,
                 'RED' : bcolors.FAIL,
                 '---' : bcolors.OKBLUE}

#############################      I/O     #############################
# Print that the simulation started
def print_kast_header():
    print(bcolors.HEADER + bcolors.BOLD+ "\n*************************************************")
    print("************    KAST INITIALIZED     ************")
    print("*************************************************" + bcolors.ENDC)

def print_kast_ender():
    print(bcolors.HEADER + bcolors.BOLD+ "\n*************************************************")
    print("***************     COMPLETE     ****************")
    print("*************************************************" + bcolors.ENDC)

# Print when a new step is starting
def print_data_source_step(step_num):
    print(bcolors.HEADER + bcolors.BOLD + "\n--------------------- STEP " + str(step_num) + " ---------------------\n" + bcolors.ENDC)

def print_spellbook_knowledge(runtime,io=False):
    match io:
        case 'high':
            print(bcolors.OKBLUE +"\nHigh Level Knowledge Values" + bcolors.ENDC)
            print([str(knowledge) for knowledge in runtime.spellbook.high_level_knowledge.values()])
        case 'low':
            print(bcolors.OKBLUE +"\nLow Level Knowledge Values" + bcolors.ENDC)
            print([str(knowledge) for knowledge in runtime.spellbook.low_level_knowledge.values()])
        case 'both':
            print(bcolors.OKBLUE +"\nLow Level Knowledge Values:" + bcolors.ENDC)
            print([str(knowledge) for knowledge in runtime.spellbook.low_level_knowledge.values()])
            print(bcolors.OKBLUE +"\nHigh Level Knowledge Values:" + bcolors.ENDC)
            print([str(knowledge) for knowledge in runtime.spellbook.high_level_knowledge.values()])