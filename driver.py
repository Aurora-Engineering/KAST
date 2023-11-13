# Knowledge Aquisition and Synthesis Tool

import numpy as np
import pandas as pd

from src.predicate import Predicate
from src.knowledge.core import Knowledge
from src.spellbook.core import Spellbook
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

	pred_dict = {} # Want to potentially keep this separate from spellbook to keep PDDL as a separate 

	SME_methods = [('pose','posz',pose_to_posz)] # data translation tuple of form ('input_var','output_var',translation_func)

	spellbook = Spellbook(
		low_level_headers=next_line.keys(),
		data_translation_methods=SME_methods,
	)

	# for value in spellbook.low_level_knowledge.values():
	# 	print(value)
    
	# for value in spellbook.high_level_knowledge.values():
	# 	print(value)
    
	# for kaster in spellbook.kasters:
	# 	print(kaster)

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




	while next_line != None:
		# Read data from CSV (line by line); iteration done at the end so we catch the None case

		# should the below operation live more in the parser? or in get_next_line, at least;
		# have get_next_line return dict with preserved datatypes? is this automatable?
		temp = {}
		for column in next_line.keys(): # for each DF column
			if type(next_line[column]) == str:
				temp[column] = strlist_to_list(next_line[column]) # need to convert lists stored as strings in csv to list (or array, or whatever)
														  # most of the time csv's wouldn't require this - if we were getting pybullet data from redis we wouldn't have to worry abt this
			else:
				temp[column] = next_line[column]
		
		spellbook.update_low_level_knowledge(temp) # Update low level knowledge using current line, whose typing is fixed by above loop
		spellbook.kast() 					       # Use predefined kasters to generate high-level knowledge from low level knowledge

		### <subprocess> ###
		# Loop through predicates list and see which are occurring
		pred_bools = {}
		for predicate in pred_dict.keys(): # for all defined predicates
			if pred_dict[predicate].name in spellbook.high_level_knowledge.keys(): # if the variable considered (ex. 'pos' in (pos lt 1)) is present in the high level knowledge
				# print('predicate threshold is', pred_dict[predicate].vars)
				# print('high level info is', spellbook.high_level_knowledge[pred_dict[predicate].name].value)
				pred_bools[predicate] = pred_dict[predicate].operator(spellbook.high_level_knowledge[pred_dict[predicate].name].value,float(pred_dict[predicate].vars)) 
				# Return whether the predicate is true by evaluating the operator of the predicate with the predicate threshold and the current high level value
				# Issue: need to ensure that predicate threshold and current value are of comparable types

				# clearly these attributes need renaming and a bunch of these dicts need to go, but the functionality is there
		
		# print(pred_bools)


		### </subprocess> ###
		# print('posz:',spellbook.high_level_knowledge['posz'].value)
		next_line = parser.get_next_line()
	
	return

if __name__ == '__main__':
	# main()
	pybullet_synthesis(filename='data/pybullet_data.csv')
	# SME_input(['Evana', 8, 'chicken', 2, 'day'])












