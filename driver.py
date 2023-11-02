# Knowledge Aquisition and Synthesis Tool

import numpy as np
import pandas as pd

from src.predicate import Predicate
from src.knowledge.core import Knowledge
from src.sme_inputs import comparative_operators
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
	
	def strlist_to_list(strlist):
		return strlist.strip('][').split(',')
	
	# Subprocesses need to be outsourced to other classes/files 
	parser = CSVParser(filename)
	next_line = parser.get_next_line()
	
	knowledge_dict = {}
	pred_dict = {}

	for column in next_line.keys:
		knowledge_dict[column] = Knowledge(_label='low',_name=column) # Create a Knowledge object to be updated for each DF column
	

	### <subprocess 1> ###
	# Generation of template predicates from SME knowledge
	ret = {}
	print("Follow the steps to input predicates.\nEnter STOP to finish predicate generation.")
	while ret != None:
		ret = comparative_operators()
		if ret == None:
			break
		pred_dict.update(ret) 
	# Now have dictionary of SME defined predicates i.e. {'droneAtHome': Predicate(pos < 1)}

	### </subprocess 1> ###


	while next_line != None: # Loop over CSV
		# Read data from CSV (line by line); iteration done at the end so we catch the None case

		### <subprocess 2> ###
		# Knowledge updating

		# Convert input to knowledge
		# should the below operation live more in the parser? or in get_next_line, at least;
		# have get_next_line return dict with preserved datatypes rather than
		for column in next_line.keys(): # for each DF column
			if type(next_line[column]) == str:
				temp = strlist_to_list(next_line[column]) # need to convert lists stored as strings in csv to list (or array, or whatever)
															# most of the time csv's wouldn't require this - if we were getting pybullet data from redis we wouldn't have to worry abt this
			else:
				temp = next_line[column]
			knowledge_dict[column].update(temp) # Update Knowledge entry with new value on each loop
		### </subprocess 2> ###

		### <subprocess 3> ###
		# Extract useful knowledge from each line
		position = knowledge_dict['pose'][:3] 			# Synethesize data from SME knowledge (position is first 3 entries of pose)
		### </subprocess 3> ###

		### <subprocess 4> ###
		# Loop through predicates list and see which are occurring

		### </subprocess 4> ###

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

def SME_input_rev1():
	i = 0
	while i < 5:
		ret = comparative_operators()
		if ret == None:
			break
	

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
	pybullet_synthesis(filename='data/pybullet_data.csv')
	# SME_input(['Evana', 8, 'chicken', 2, 'day'])












