import configparser
import pandas as pd
import os
from typing import List,Tuple, Callable

from kast.src.spellbook.core import Spellbook
from kast.utils.data_sources.core import DataSource
from kast.utils.functions import get_attribute_by_name, import_module

class KastRuntime():
    def __init__(self, config_filepath: str):
        self._config_filepath = config_filepath
        assert os.path.exists(self._config_filepath), f'Specified config filepath {self._config_filepath} cannot be found.'


        self.parse_config()
        self.import_kaster_methods()
        self.initialize_data_source()

        self.spellbook = Spellbook(self.data_source.headers,self.kaster_definitions)

    def parse_config(self) -> None:
        # Set up config and read given file
        self.config = configparser.ConfigParser()
        self.config.read(self._config_filepath)

        # Extract paths from config
        self.kaster_methods_path = self.config['DEFAULT']['KasterMethodsPath'] 
        self.kaster_definitions_path = self.config['DEFAULT']['KasterDefinitionsPath']
        self.data_file_path = self.config['DEFAULT']['DataFile']
        self.data_type = self.config['DEFAULT']['DataType']

    def import_kaster_methods(self):
        self.kaster_definitions = []

        # Initialize definitions and split string representations of lists into lists of strings
        kaster_df: pd.DataFrame = pd.read_csv(self.kaster_definitions_path)
        kaster_string_tuples = [(inp.split(","), out.split(","), method) for inp, out, method in zip(kaster_df['input'], kaster_df['output'],kaster_df['method'])]
        # How do we test the above line?
        
        # Import given python filepath
        module = import_module(module_name='kaster_methods',file_to_import=self.kaster_methods_path)

        # For each kaster in given definitions, extract the specified function/method by the string name and create definitions including the callable
        for kaster_tuple in kaster_string_tuples:
            kaster_method = get_attribute_by_name(module,kaster_tuple[2])
            self.kaster_definitions.append((kaster_tuple[0],kaster_tuple[1],kaster_method))
    
    def initialize_data_source(self):
        module = import_module(module_name='data_source',file_to_import=f'kast/utils/data_sources/{self.data_type}_data_source.py')
        class_reference = get_attribute_by_name(module,f'{self.data_type.upper()}DataSource')
        self.data_source: DataSource = class_reference(self)        

    def run_step(self, override=None):
        if override == None:
            low_level_information = self.data_source.get_new_information()
        else:
            low_level_information = override
                
        self.spellbook.update_low_level_knowledge(low_level_information)
        self.spellbook.kast()

    def execute(self, io=None):
        while self.data_source.has_more():
            print(f'------------------------------- STEP {self.data_source.index} -------------------------------')

            self.run_step()
            if io:
                match io:
                    case 'high':
                        print([str(knowledge) for knowledge in self.spellbook.high_level_knowledge.values()])
                    case 'low':
                        print([str(knowledge) for knowledge in self.spellbook.low_level_knowledge.values()])
                    case 'both':
                        print([str(knowledge) for knowledge in self.spellbook.low_level_knowledge.values()])
                        print([str(knowledge) for knowledge in self.spellbook.high_level_knowledge.values()])

        print('----------------------------------------------------------------------------')
        print('------------------------------- RUN COMPLETE -------------------------------')
        print('----------------------------------------------------------------------------')
