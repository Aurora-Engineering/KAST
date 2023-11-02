# Knowledge Aquisition and Synthesis Tool

import numpy as np
import pandas as pd

from src.predicate import Predicate
from src.knowledge.core import Knowledge
from utils.parsers import CSVParser

def main():
	# Knowledge
	temp_arr = np.array((1,2))
	temp_low_level = Knowledge('low','Numpy Array',temp_arr,type(temp_arr))
	temp_high_level = Knowledge('high','Gripper Status','closed',type('closed'))
	print(temp_low_level)
	print(temp_high_level)
	temp_high_level.update(True)
	print(temp_high_level)

	# Predicates
	temp_pred = Predicate('at', [1,2,3])
	print(temp_pred)
	return 

def pybullet_synthesis(filename):
	# Subprocesses need to be outsourced to other classes/files 
	parser = CSVParser(filename)
	next_line = parser.get_next_line()
	home = [0,0,1]
	
	gen_pr_dict = {}
	templ_pr_dict = {}

	### <subprocess 1> ###
	# Generation of template predicates from SME knowledge (may not use Predicate class)
	position_predicate_template = Predicate('droneAtHome',home)
	templ_pr_dict['drone_at_home'] = (position_predicate_template)
	### </subprocess 1> ###


	while next_line != None:
		# Read data from CSV (line by line)
		line_index, line_series = next_line

		### <subprocess 2> ###
		# Knowledge Extraction/Data Fusion 
		# Extract useful knowledge from each line
		position = line_series['pose'].strip('][').split(',')[:3] 			# Synethesize data from SME knowledge (position is first 3 entries of pose)
		templ_pr_dict['drone_at_home'] = (position_predicate_template)

		# Transform extracted data to predicates
		position_predicate = Predicate('droneAt',position)					# Generate predicates from synthesized data
		gen_pr_dict['drone_at_home'] = position_predicate
		### </subprocess 2> ###

		# Check generated vs templated predicates to detect which are happening

		for check in gen_pr_dict.keys():
			# print('Gen vars are',gen_pr_dict[check].vars)
			# print('Templ vars are', templ_pr_dict[check].vars)
			check_bool = gen_pr_dict[check].vars == templ_pr_dict[check].vars
			print(f'{check} is {check_bool}')

		next_line = parser.get_next_line()

	return

def SME_input(frame):
	print("Please enter information to be considered in predicate formulation")
	for i in range(len(frame)):
		print(str(i) + ' - ' + str(frame[i]))

	j = 0
	while j < 3:
		urnary_operators(frame)
		j +=1
	# turnary_operators()

# print("Please enter in all variables to be considered (in sequential order) using their index, shown above. Print STOP to end variable input list.")
	# new_variable_index  = None
	# all_vars = []

	# while new_variable_index != 'STOP':
	# 	new_variable_index = input("New variable index: ")
	# 	if new_variable_index == 'STOP':
	# 		break
	# 	new_variable = frame[int(new_variable_index)]
	# 	all_vars.append(new_variable)

	# print(all_vars)


def urnary_operators(frame):
	print("Please enter in all variables to be considered for urnary operator using their index, shown above.")
	new_variable_index = input("New variable index: ")
	new_variable = frame[int(new_variable_index)]
	urnary_operator = input("Please enter one of the follow operators [<,>,=]: ")
	numerical_val = input("Please enter a numerical value: ")
	pred_name = input("Please enter a predicate descriptor: ")
	
	print(pred_name + '() ')
	print('if ' + new_variable + ' ' + urnary_operator + ' ' + str(numerical_val))

def turnary_operators():
	pass

if __name__ == '__main__':
	# main()
	# pybullet_synthesis(filename='data/pybullet_data.csv')
	SME_input(['Evana', 8, 'chicken', 2, 'day'])












