from itertools import chain
from typing import List, Sequence


# _____________________________________________________________________________
# Extract names from list of lists whilst keeping best effort to maintain order across missing list elements
def extract_names(data: List[List]) -> List:
    if data is None or len(data) == 0:
        return []
    if len(data) == 1:
        return data[0]

    # Build names list
    names = data[0]
    tmp = []
    for itm in chain(*data):
        if (i := next((j for j, x in enumerate(names) if x == itm), -1)) < 0:
            tmp.append(itm)
        elif i >= 0 and len(tmp):
            names[i:i] = tmp
            tmp = []
    if len(tmp):
        names.extend(tmp)

    # Sort names list
    while True:
        is_swapped = False
        for row in data:
            if len(row) < 2:
                continue
            i_n = names.index(row[0])
            for r in row[1:]:
                i_m = names.index(r)
                if i_n - i_m == 1:
                    names[i_n], names[i_m] = names[i_m], names[i_n]
                    is_swapped = True
                elif i_n - i_m > 1:
                    names[i_m], names[i_m + 1:i_n + 1] = names[i_n], names[i_m:i_n]
                    is_swapped = True
                i_n = i_m
        if not is_swapped:
            break

    return names


# _____________________________________________________________________________
# Order names according to supplied list
def order_names(names: List[str], start_order: List[str], end_order: List[str] = None, ok_if_missing: bool = False) -> \
        List[str]:

    # Validate start/end sort lists
    if not ok_if_missing:
        if start_order and len(missing_names := [n for n in start_order if n not in names]):
            raise ValueError(f'Missing start name: {missing_names}')
        if end_order and len(missing_names := [n for n in end_order if n not in names]):
            raise ValueError(f'Missing end name: {missing_names}')

    # Sort end order first
    if end_order is not None and len(end_order):
        m: int = len(names) - 1
        for i, name in enumerate(end_order):
            if (j := next((k for k, x in enumerate(names) if x == name), -1)) >= 0 and m - j == 1:
                names[m], names[j] = name, names[m]
            elif m - j > 1:
                names[m], names[j:m] = name, names[j + 1:m + 1]

    # Sort start order last
    if start_order is not None and len(start_order):
        for i, name in enumerate(start_order):
            if (j := next((k for k, x in enumerate(names) if x == name), -1)) >= 0 and j - i == 1:
                names[i], names[j] = name, names[i]
            elif j - i > 1:
                names[i], names[i + 1:j + 1] = name, names[i:j]

    return names
