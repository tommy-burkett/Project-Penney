from typing import Callable
from datetime import datetime as dt
from src.datagen import get_decks

DEBUG = True


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


n = 1_000_000
seed = 42

get_decks_timed = debugger_factory()(get_decks)

get_decks_timed(n, seed=42)

np.unique(decks[15], return_counts=True)


