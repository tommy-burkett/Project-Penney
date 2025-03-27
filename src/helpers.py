from typing import Callable
from datetime import datetime as dt

DEBUG = True

PATH_DATA = 'data'
PATH_FIGURES = 'figures'


def debugger_factory(show_args=True) -> Callable:
    def debugger(func:Callable) -> Callable:
        if DEBUG:
            def wrapper(*args, **kwargs):
                if show_args:
                    print(f'{func.__name__} was called with:')
                    print('Positional arguments:\n', args)
                    print('Keyword arguments:\n', kwargs)
        
                t0 = dt.now()
                results = func(*args, **kwargs)
                print(f'{func.__name__} ran for {dt.now()-t0}')
                return results
        else:
            return func
        return wrapper
    return debugger

