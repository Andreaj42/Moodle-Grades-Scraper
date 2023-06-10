import os
import sys

def load_variables(var : str):
    if var in os.environ:
        variable = os.environ[var]
        return variable

    raise RuntimeError(f'Merci de définir la variable : {var}')