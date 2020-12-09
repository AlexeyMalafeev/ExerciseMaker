os.path.join = os.path.join
rnd = random.randint


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_gap_info(num_gaps):
    """Return string:
        0           -> ''
        0.9 (< 1)   -> '90%'
        15 (> 1)    -> '15'"""
    if num_gaps == 0:
        return ''
    elif num_gaps <= 1:
        return ' {}%'.format(round(num_gaps * 100))
    else:
        return ' {}'.format(num_gaps)


def ind_from_dict(ind_dict, n, prox=2):
    """
Randomly choose a number (n) of indices from dict (ind_dict) of lists of indices
with minimum difference (prox) between all indices.
Shortest lists of indices have a priority.
"""
    ind = [ig[:] for ig in ind_dict.values()]
    ind.sort(key=len, reverse=True)
    new = []
    while len(new) < n and ind != []:
        ig = ind.pop()
        if not ig:
            continue
        i = random.choice(ig)
        new.append(i)
        for ii in range(i - prox, i + prox + 1):
            for ig in ind:
                if ii in ig:
                    ig.remove(ii)
    return new


def ind_from_dict_ordered(ind_dict, order, n, prox=2):
    """
Randomly choose a number (n) of indices from dict (ind_dict) of lists of indices
with minimum difference (prox) between all indices.
Ordered (order = [word1, word2, ...]): words have a priority over _preceding_ words.
"""
    ind = []
    for w in order:
        if w in ind_dict:
            ind.append(ind_dict[w])
    new = []
    while len(new) < n and ind != []:
        ig = ind.pop()
        if not ig:
            continue
        i = random.choice(ig)
        new.append(i)
        for ii in range(i - prox, i + prox + 1):
            for ig in ind:
                if ii in ig:
                    ig.remove(ii)
    return new


def ind_from_list(ind_list, n, prox=2):
    """
Randomly choose a number (n) of indices from list (ind_list)
with minimum difference (prox) between all indexes.
"""
    ind = set(ind_list)
    new = []
    while len(new) < n and ind != set():
        i = random.sample(ind, 1)[0]  # sets don't support indexing
        new.append(i)  # so can't use random.choice
        for ii in range(i - prox, i + prox + 1):
            if ii in ind:
                ind.remove(ii)
    return new


def mean(seq, round_digits=3):
    n = len(seq)
    if n == 0:
        raise ValueError('The sequence is empty.')
    s = sum(seq)
    r = round_digits
    return round(s / n, r)


def num_to_letter(n):
    """0 -> a
    1 -> b
    2 -> c
    30 -> e1
    100 -> w3
    1000000 -> o38461"""
    import string
    letters = string.ascii_lowercase
    a, b = divmod(n, 26)
    return '{}{}'.format(letters[b], a if a > 0 else '')
