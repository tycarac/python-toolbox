from itertools import chain
from typing import List


# _____________________________________________________________________________
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
