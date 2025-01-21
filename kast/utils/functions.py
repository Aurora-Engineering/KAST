# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"

import importlib.util
import os
import ast

def import_module(module_name: str, file_to_import: str):
    """
    Programmatically import a module from a filepath

    Parameters
    ----------
    module_name : str
        Name of the imported module (required but not used)
    file_to_import : str
        String filepath of imported module

    Returns
    -------
    module
        An accessible module (e.g. by module.attribute or module.method)
    """
    assert os.path.exists(file_to_import), f"File {file_to_import} failed to import, check your config"

    spec = importlib.util.spec_from_file_location(module_name, file_to_import)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def extract_return_names(f_name, file):
    """
    Given a file and function name, extract the names of the variables returned from that function.
    Used in KAST to generate Kaster output variable names (which are then used to initialize high level knowledge)
    Parameters
    ----------
    f_name : str
        String name of the function to be analyzed
    file : str
        File from which to import function
    Returns
    -------
    output_variables : List[str]
        List of string names of the variables returned by the function
    """
                                                                             
    for x in return_file_nodes(file):
        print('looped')     
        if not(isinstance(x, ast.FunctionDef)):
            print('checked class instance')                                                             
            continue                                                                                        
        if not(x.name == f_name): 
            continue 
        for b in x.body:         
            output_vars = check_body_node(b)  
            if output_vars != None:
                return output_vars                                                                         

# Decorators: these get wrapped to prevent having to test them. Trying to mock calls that pytest uses (ast and getattr fall under this category) causes testing issues.
def get_attribute_by_name(object, name):
    return getattr(object,name) 

def return_file_nodes(file): 
        return(ast.walk(ast.parse(open(file).read())))

def check_body_node(node):
    if isinstance(node, ast.Return):  
        if isinstance(node.value, ast.Tuple):
            output_variables = [var.id for var in node.value.elts]
            return output_variables