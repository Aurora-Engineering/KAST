# Knowledge Aquisition and Synthesis Tool

from src.predicate import Predicate
from src.knowledge.core import Knowledge
import numpy as np

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

if __name__ == '__main__':
	main()