# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"

import configparser
import pandas as pd
import os
from inspect import getmembers, isfunction, getfullargspec

from kast.src.spellbook import Spellbook
from kast.utils.functions import get_attribute_by_name, import_module, extract_return_names
from kast.utils.print_io import *

class KastRuntime():
    def __init__(self, config_filepath: str):
        self._config_filepath = config_filepath
        assert os.path.exists(self._config_filepath), f'Specified config filepath {self._config_filepath} cannot be found.'

        self.parse_config()
        self.import_kaster_methods()
        self.initialize_data_source()

        self.spellbook = Spellbook(self.headers,self.kaster_definitions)

    def parse_config(self) -> None:
        # Set up config and read given file
        self.config = configparser.ConfigParser()
        self.config.read(self._config_filepath)

        # Extract paths from config
        self.kaster_methods_path = self.config['DEFAULT']['KasterMethodsPath'] 
        self.data_file_path = self.config['DEFAULT']['DataFile']
        self.data_type = self.config['DEFAULT']['DataType']

    def import_kaster_methods(self):
        self.kaster_definitions = []
        self.headers = []

        # Import given python filepath and create a list of the functions in that file
        module = import_module(module_name='kaster_methods',file_to_import=self.kaster_methods_path)
        func_list = getmembers(module, isfunction)

        # For each of those functions, create a Kaster definition of form ([input_variables], [output_variables], callable_kaster_method)
        sum = 0
        for f in func_list:
            f_name = f[0]
            f_callable = f[1]

            input_variables = getfullargspec(f_callable).args
            # print(f'input vars are {len(input_variables)}')
            output_variables = extract_return_names(f_name, self.kaster_methods_path)

            self.kaster_definitions.append((
                input_variables,
                output_variables,
                f[1]
            ))
            for var in input_variables:
                self.headers.append(var)
            sum = sum + len(input_variables)

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
