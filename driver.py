# Knowledge Aquisition and Synthesis Tool
from kast.src.runtime.core import KastRuntime


def main():
	runtime = KastRuntime('kast/config/example_config.ini')
	for spellbook in runtime.execute(io='high'):
		for knowledge_object_name, knowledge_object in spellbook.high_level_knowledge.items():
			print(f'{knowledge_object}')

def manual_override():
	runtime = KastRuntime('kast/config/manual_pass_config.ini')
	yielded_spellbook = runtime.run_step({'pose': '[1,1,1]','pose1':'[2,2,2]','pose2':'[3,3,3]'},io=False)
	for _, knowledge_object in yielded_spellbook.high_level_knowledge.items():
		print(f'{knowledge_object}')
		print(f'{knowledge_object.value}')

if __name__ == '__main__':
	main()











