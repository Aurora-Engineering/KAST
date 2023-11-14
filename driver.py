# Knowledge Aquisition and Synthesis Tool

from src.spellbook.pddl_spellbook import PDDLSpellbook
from utils.parsers import CSVParser

def main(filename):
	
	def strlist_to_list(strlist):
		return strlist.strip('][').split(',')
	
	def pose_to_posz(pose):
		pose = [float(p) for p in pose]
		return([pose[2]])
	
	SME_translation_methods = [		# data translation tuple of form ('input_var','output_var',translation_func)
		('pose','posz',pose_to_posz)
		] 
	SME_predicate_definitions = [	# predicate definition tuple of form ('predicate name','reference variable','binary operator', numerical value), see PDDLSpellbook for more detail
		('atHome','posz','<',[1])		# currently only supports binary comparison operators
	]

	# Subprocesses need to be outsourced to other classes/files 
	parser = CSVParser(filename)
	next_line = parser.get_next_line()

	spellbook = PDDLSpellbook(
		low_level_headers=next_line.keys(),
		data_translation_methods=SME_translation_methods,
		predicate_definitions=SME_predicate_definitions
	)

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
		spellbook.evaluate_predicates()
		print(f'state is {spellbook.state}')

		next_line = parser.get_next_line()
	return

if __name__ == '__main__':
	main(filename='data/pybullet_data.csv')












