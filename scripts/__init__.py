"""_summary_

"""

from typing import Callable


class Scripts:
    def __init__(self, module):
        self.module = module

    def __str__(self):
        return dir(self.script_file)

    def _methods(self):
        methods = []
        for m in self.script_file:
            if isinstance(m, Callable):
                methods.append(m)

        return methods 
