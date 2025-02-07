# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"

from kast.src.kast_runtime import KastRuntime
from kast.utils.print_io import *
import argparse


def main():
	arg_parser = argparse.ArgumentParser(description='')
	arg_parser.add_argument('--demo', '-d', action='store_true',
						 help='Run the demo data')
	arg_parser.add_argument('--live', '-l', action='store_true',
						 help='Run a demo using user input live data')

	args = arg_parser.parse_args()

	if args.demo:
		runtime = KastRuntime('kast/config/example_config.ini')
		for yielded_spellbook in runtime.execute(io='both'):
			# Access new values on each step through the yielded spellbook
			# For example, to extract the value of the high level Knowledge object 'posx'
			# posx = yielded_spellbook.high_level_knowledge['posx'].value
			pass
		quit()
	
	if args.live:
		runtime = KastRuntime('kast/config/live_demo_config.ini')
		print_kast_header()
		while True:
			pose_input = input('Enter a Python-format list of three numbers (ex. [1,1,1]) to use as the pose variable. Enter STOP to exit.\n>>')
			if pose_input == 'STOP':
				print_kast_ender()
				break
			else:
				yielded_spellbook = runtime.run_step({'pose': pose_input,'rpy': '[1, 1, 1]'},io='both')
				# Access new values on each step through the yielded spellbook
				# For example, to extract the value of the high level Knowledge object 'posx'
				# posx = yielded_spellbook.high_level_knowledge['posx'].value

if __name__ == '__main__':
	main()