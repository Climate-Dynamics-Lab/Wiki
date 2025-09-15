import numpy as np
import warnings
import re
from typing import Union, List, Callable, Optional

def split_list_max_n(lst: Union[List, np.ndarray], n: int) -> List:
    """
    Split `lst` into balanced chunks with at most `n` elements each.

    Args:
        lst: List to split.
        n: Maximum number of elements in each chunk of `lst`.

    Returns:
        List of `n` chunks of `lst`
    """
    k = int(np.ceil(len(lst) / n))  # Number of chunks needed
    avg = int(np.ceil(len(lst) / k))
    return [lst[i * avg : (i + 1) * avg] for i in range(k)]


def parse_int_list(value: Union[str, int, List], format_func: Callable = lambda x: str(x),
                   all_values: Optional[List] = None) -> List:
    """
    Takes in a value or list of values e.g. `[1, 2, 3]` and converts it into a list of strings where
    each string has the format given by `format_func` e.g. `['1', '2', '3']` for the default case.

    There are three string options for `value`:

    * `value='x:y'`, will return all integers between `x` and `y` inclusive.
    * `value='firstX'` will return first X values of `all_values`.
    * `value='firstY'` will return first Y values of `all_values`.

    Args:
        value: Variable to convert into list of strings
        format_func: How to format each integer within the string.
        all_values: List of all possible integers, must be provided if `value='firstX'` or `value='firstY'`.

    Returns:
        List, where each integer in `value` is converted using `format_func`.
    """
    if isinstance(value, list):
        pass
    elif isinstance(value, int):
        value = [value]
    elif isinstance(value, str):
        value = value.strip()       # remove blank space
        # Can specify just first or last n years
        if re.search(r'^first(\d+)', value):
            if all_values is None:
                raise ValueError(f'With value={value}, must provide all_values')
            n_req = int(re.search(r'^first(\d+)', value).group(1))
            if n_req > len(all_values):
                warnings.warn(f"Requested {value} but there are only "
                              f"{len(all_values)} available:\n{all_values}")
            value = all_values[:n_req]
        elif re.search(r'^last(\d+)', value):
            if all_values is None:
                raise ValueError(f'With value={value}, must provide all_values')
            n_req = int(re.search(r'^last(\d+)', all_values).group(1))
            if n_req > len(all_values):
                warnings.warn(f"Requested {value} but there are only "
                              f"{len(all_values)} available:\n{all_values}")
            value = all_values[-n_req:]
        elif ':' in value:
            # If '1979:2023' returns all integers from 1979 to 2023
            start, end = map(int, value.split(':'))
            value = list(range(start, end + 1))
        else:
            value = [int(value)]
    else:
        raise ValueError(f"Unsupported format: {value}")
    return [format_func(i) for i in value]


def round_any(x: Union[float, np.ndarray], base: float, round_type: str = 'round') -> Union[float, np.ndarray]:
    """
    Rounds `x` to the nearest multiple of `base` with the rounding done according to `round_type`.

    Args:
        x: Number or array to round.
        base: Rounds `x` to nearest integer multiple of value of `base`.
        round_type: One of the following, indicating how to round `x`:

            - `'round'`
            - `'ceil'`
            - `'float'`

    Returns:
        Rounded version of `x`.

    Example:
        ```
        round_any(3, 5) = 5
        round_any(3, 5, 'floor') = 0
        ```
    """
    if round_type == 'round':
        return base * np.round(x / base)
    elif round_type == 'ceil':
        return base * np.ceil(x / base)
    elif round_type == 'floor':
        return base * np.floor(x / base)
    else:
        raise ValueError(f"round_type specified was {round_type} but it should be one of the following:\n"
                         f"round, ceil, floor")