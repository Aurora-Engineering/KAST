# Knowledge Aquisition and Synthesis Tool

import numpy as np
import pandas as pd

from src.predicate import Predicate
from src.knowledge.core import Knowledge
from src.sme_inputs import binary_operators
from utils.parsers import CSVParser

def main():
	def test_func(value):
		return(value+1)
	
	info = Knowledge('low','pose')
	info.update(1)

	new = info.kast('pos',test_func)
	return 

def pybullet_synthesis(filename):
	
	def strlist_to_list(strlist):
		return strlist.strip('][').split(',')
	
	def pose_to_posz(pose):
		pose = [float(p) for p in pose]
		return(pose[2])
	
	# Subprocesses need to be outsourced to other classes/files 
	parser = CSVParser(filename)
	next_line = parser.get_next_line()
	
	low_level_dict = {}
	high_level_dict = {}
	pred_dict = {}

	for column in next_line.keys():
		low_level_dict[column] = Knowledge(_label='low',_name=column) # Create a Knowledge object to be updated for each DF column
	
	### <subprocess> ###
	# Generate methods to transition low to high level data ahead of time
	# Should probably be exported to sme_inputs; plus, this definition is ugly - need to simplify like other SME input step
	transition_methods = []
	transition_methods.append({'input_var':'pose','output_var':'posz','method':pose_to_posz}) # Req info: starting var, ending var, function used
	for entry in transition_methods:
		ret = {entry['output_var']: Knowledge('high',entry['output_var'])}
		high_level_dict.update(ret)
	### </subprocess> ###


	### <subprocess> ###
	# Generation of template predicates from SME knowledge
	ret = {}
	print("Follow the steps to input predicates.\nEnter STOP to finish predicate generation.")
	while ret != None:
		ret = binary_operators()
		if ret == None:
			break
		pred_dict.update(ret) 
	# Now have dictionary of SME defined predicates i.e. {'droneAtHome': Predicate(pos < 1)}
	### </subprocess> ###




	while next_line != None: # Loop over CSV
		# Read data from CSV (line by line); iteration done at the end so we catch the None case

		### <subprocess> ###
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
			low_level_dict[column].update(temp) # Update Knowledge entry with new value on each loop
		### </subprocess> ###

		### <subprocess> ###
		# Extract high level knowledge based on SME inputs - abstract out
		for entry in transition_methods:
			if entry['input_var'] in low_level_dict.keys():
				high_level_dict.update({entry['output_var']: low_level_dict[entry['input_var']].kast(entry['output_var'],entry['method'])}) # This line sucks. How do we best abstract this out?

			# Process occurring here: 
			# for all the pre-defined transition methods (all the pre-defined high level data transformations)
			# if the input variable they require is present in the low level knowledge
			# update the high level dictionary with the corresponding output from feeding the low level input var into the translation method
		
		### </subprocess> ###

		### <subprocess> ###
		# Loop through predicates list and see which are occurring
		pred_bools = {}
		for predicate in pred_dict.keys(): # for all defined predicates
			if pred_dict[predicate].name in high_level_dict.keys(): # if the variable considered (ex. 'pos' in (pos lt 1)) is present in the high level knowledge
				print('predicate threshold is', pred_dict[predicate].vars)
				print('high level info is', high_level_dict[pred_dict[predicate].name].value)
				pred_bools[predicate] = pred_dict[predicate].operator(high_level_dict[pred_dict[predicate].name].value,float(pred_dict[predicate].vars)) 
				# Return whether the predicate is true by evaluating the operator of the predicate with the predicate threshold and the current high level value
				# Issue: need to ensure that predicate threshold and current value are of comparable types

				# clearly these attributes need renaming and a bunch of these dicts need to go, but the functionality is there
		
		print(pred_bools)


		### </subprocess> ###

		next_line = parser.get_next_line()
	return

if __name__ == '__main__':
	# main()
	pybullet_synthesis(filename='data/pybullet_data.csv')
	# SME_input(['Evana', 8, 'chicken', 2, 'day'])












