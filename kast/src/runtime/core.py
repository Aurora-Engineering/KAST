import configparser
import pandas as pd
import importlib.util
from typing import List,Tuple, Callable

from kast.src.spellbook.core import Spellbook
from kast.utils.data_sources.core import DataSource

def strlist_to_list(strlist):
	return strlist.strip('][').split(',')

class KastRuntime():
    def __init__(self, config_filepath: str):
        self.kaster_definitions = []

        self._config_filepath = config_filepath
        self.parse_config()
        self.initialize_data_source()
        self.spellbook = Spellbook(self.data_source.headers,self.kaster_definitions)

    def parse_config(self):
        
        # Set up config and read given file
        self.config = configparser.ConfigParser()
        self.config.read(self._config_filepath)

        # Extract paths from config
        kaster_methods_path = self.config['DEFAULT']['KasterMethodsPath'] 
        kaster_definitions_path = self.config['DEFAULT']['KasterDefinitionsPath']
        self.data_file_path = self.config['DEFAULT']['DataFile']
        self.data_type = self.config['DEFAULT']['DataType']

        # Initialize definitions and split string representations of lists into lists of strings
        kaster_def_raw: pd.DataFrame = pd.read_csv(kaster_definitions_path)
        kaster_strings = [(strlist_to_list(inp), strlist_to_list(out), method) for inp, out, method in zip(kaster_def_raw['input'], kaster_def_raw['output'],kaster_def_raw['method'])]
        
        # Import given python filepath
        spec = importlib.util.spec_from_file_location('utils.pybullet_utils',kaster_methods_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # For each kaster in given definitions, extract the specified function/method by the string name and create definitions including the callable
        for kaster in kaster_strings:
            kaster_method = getattr(module,kaster[2])
            self.kaster_definitions.append((kaster[0],kaster[1],kaster_method))
    
    def initialize_data_source(self):
        spec = importlib.util.spec_from_file_location('utils.data_sources',f'kast/utils/data_sources/{self.data_type}_datasource.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        class_attr = getattr(module,f'{self.data_type.upper()}DataSource')
        self.data_source: DataSource = class_attr(self)        

    def run_step(self, override_frame=None):
        if override_frame == None:
            low_level_information = self.data_source.get_new_information()
        else:
            low_level_information = override_frame
        
        self.spellbook.update_low_level_knowledge(low_level_information)
        self.spellbook.kast()

    def execute(self, io=None):
        while self.data_source.has_more():
            print(f'------------------------------- STEP {self.data_source.index} -------------------------------')

            self.run_step()
            if io:
                match io:
                    case 'high':
                        print(self.spellbook.high_level_knowledge)
                    case 'low':
                        print(self.spellbook.low_level_knowledge)
                    case 'both':
                        print(self.spellbook.low_level_knowledge)
                        print(self.spellbook.high_level_knowledge)

        print('----------------------------------------------------------------------------')
        print('------------------------------- RUN COMPLETE -------------------------------')
        print('----------------------------------------------------------------------------')
