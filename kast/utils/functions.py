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

def get_attribute_by_name(object, name):
    return getattr(object,name) # This just exists to shield this method for testing

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
    for x in ast.walk(ast.parse(open(file).read())):                                                        
        if not(isinstance(x, ast.FunctionDef)):                                                             
            continue                                                                                        
        if not(x.name == f_name):                                                                            
            continue                                                                                        
        for b in x.body:                                                                                    
            if isinstance(b, ast.Return):  
                if isinstance(b.value, ast.Tuple):
                    output_variables = [var.id for var in b.value.elts]
                    return output_variables