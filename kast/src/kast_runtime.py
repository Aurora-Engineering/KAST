import configparser
import pandas as pd
import os
from typing import List,Tuple, Callable
from inspect import getmembers, isfunction, getfullargspec

from kast.src.spellbook import Spellbook
from kast.utils.data_sources.core import DataSource
from kast.utils.functions import get_attribute_by_name, import_module, extract_return_names
from kast.utils.print_io import *

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
    
        # Import given python filepath and create a list of the functions in that file
        module = import_module(module_name='kaster_methods',file_to_import=self.kaster_methods_path)
        func_list = getmembers(module, isfunction)
        
        # For each of those functions, create a Kaster definition of form ([input_variables], [output_variables], callable_kaster_method)
        for index, f in enumerate(func_list):
            f_name = f[0]
            f_callable = f[1]
            self.kaster_definitions.append((
                getfullargspec(f_callable).args,
                extract_return_names(f_name, self.kaster_methods_path),
                func_list[index][1]
            ))
    
    def initialize_data_source(self):
        module = import_module(module_name='data_source',file_to_import=f'kast/utils/data_sources/{self.data_type}_data_source.py')
        class_reference = get_attribute_by_name(module,f'{self.data_type.title()}DataSource')
        self.data_source = class_reference(self)

    def run_step(self, override=None, io=False):
        if override == None:
            low_level_information = self.data_source.get_new_information()
        else:
            low_level_information = override
            self.data_source.index += 1
                
        self.spellbook.update_low_level_knowledge(low_level_information)
        self.spellbook.kast()
        
        if io:
            print_data_source_step(self.data_source.index)
            print_spellbook_knowledge(self,io)

        return(self.spellbook)

    def execute(self, io=False):
        print_kast_header()
        while self.data_source.has_more():
            self.spellbook = self.run_step(io=io)
            yield self.spellbook
        print_kast_ender()
