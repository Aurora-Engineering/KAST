import importlib.util
import os

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

