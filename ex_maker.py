#! python3


import random
import os
import sys
import traceback

jp = os.path.join
rnd = random.randint

log = []


def all_exercises(text_obj):
    """
Do all modes and return stats dict.
"""
    stats = {}
    stats_mapping = [('_title_', 'file_name'),
                     ('_word_count_', 'word_count'),
                     ('_uword_count_', 'uword_count'),
                     ('_sent_count_', 'sent_count')]
    for k, v in stats_mapping:
        stats[k] = getattr(text_obj, v, 'undefined')
    std_args = ({'max_num_gaps': 0}, {'max_num_gaps': 10}, {'max_num_gaps': 20})
    # legend: ex_class, init_args, make_ex_args
    exs = ((DerivMaker, (), std_args),
           (ErrorMaker, (), std_args),
           (FragmentMaker, (FRAG_AFTER, FRAG_FROM, 'short', 7), ({'max_num_gaps': 10},)),
           (FragmentMaker, (FRAG_AFTER, FRAG_FROM, 'long', 12), ({'max_num_gaps': 10},)),
           (MissWordsMaker, (ARTICLES, 'articles'), ({'max_num_gaps': 0},)),
           (OpenClozeMaker, (OPEN_CLOZE_EASY, 'e'), ({'max_num_gaps': 0},)),
           (OpenClozeMaker, (OPEN_CLOZE_HARD, 'h'), std_args),
           (OrderedOpenClozeMaker, (FCE_SET, FCE_ORDER, 'fce'), ({'max_num_gaps': 15},)),
           (OrderedOpenClozeMaker, (CAE_SET, CAE_ORDER, 'cae'), ({'max_num_gaps': 15},)),
           (OrderedOpenClozeMaker, (CPE_SET, CPE_ORDER, 'cpe'), ({'max_num_gaps': 15},)),
           (PrepositionsMWM, (), ({'max_num_gaps': 0},)),
           (SimpleVFormsMaker, (), ({'max_num_gaps': 0},)),
           (AdvVFormsMaker, (), std_args),
           (WordbankMaker, (), std_args)
    )
    for ex_class, init_args, arg_dicts in exs:
        init_args = (text_obj,) + init_args
        ex_obj = ex_class(*init_args)
        for arg_dict in arg_dicts:
            ex_obj.make_ex(**arg_dict)
            stats[ex_obj.tag] = ex_obj.get_gaps_ratio()
    return stats


def dump_log():
    with open('log.txt', 'w') as f:
        f.write('\n'.join(log))


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


def get_punc(word):
    """
Return (left_punc_string, right_punc_string):
    "Cat -> ('"', '')
    cat, -> ('', ',')
    'cat' -> ("'", "'")
    cat's -> ('', "'s")
    cat-powered -> ('', '-powered')
        etc.
"""
    return get_word_and_punc(word)[1:]


def get_ratio(val_a, val_b):
    return round(val_a / val_b, 3)


def get_word_and_punc(word):
    """
Return (word_without_punc, left_punc_string, right_punc_string):
"Cat -> ('Cat', '"', '')
cat, -> ('cat', '', ',')
'cat' -> ('cat', "'", "'")
cat's -> ('cat's', '', "")
"cat-powered" -> ('cat-powered', '"', '"')
    etc.
"""
    if word.isalnum():  # check for the most frequent input
        return word, '', ''
    lpunc = ''
    word_starts = 0
    for i, c in enumerate(word):
        if not c.isalnum():
            lpunc += c
        else:
            word_starts = i
            break
    rpunc = ''
    word_ends = 0
    for i, c in enumerate(word[::-1]):
        if not c.isalnum():
            rpunc += c
        else:
            word_ends = len(word) - i
            break
    if rpunc:
        rpunc = rpunc[::-1]
    word_no_punc = word[word_starts:word_ends]
    return word_no_punc, lpunc, rpunc


def has_digit(chars):
    """
Return True if any of the chars is numeric.
"""
    return any((c.isdigit() for c in chars))


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


def main():
    # ensure 'input' and 'output' folders
    ensure_dir(INPUT_DIR)
    ensure_dir(OUTPUT_DIR)

    # open all files in 'input' folder and process them
    all_stats = {}
    for file_name in os.listdir(INPUT_DIR):
        with open(jp(INPUT_DIR, file_name)) as f:
            text_input = f.read()
        file_name = file_name.replace('.txt', '')
        text_obj = TextObject(text_input, file_name)

        # run all modes
        stats = all_exercises(text_obj)
        register_measures(text_obj, stats)
        save_text_stats(stats)
        all_stats[file_name] = stats

    save_all_stats(all_stats)
    rank(all_stats)
    quit()


def make_paragraphs(words, par_ind):
    """Make paragraphs and return text as a string."""
    for i in par_ind:
        words[i] += PARAGRAPH_MARKER
    text = ' '.join([w for w in words if w])
    return text.replace(PARAGRAPH_MARKER+' ', '\n\n')


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


def rank(rdicts_dict):
    d = rdicts_dict
    ranking = {k: 0 for k in d}
    for m in COMPL_MEASURES:
        m_ref = '![{}]'.format(m)
        values = set()
        for k in d:
            values.add(d[k][m_ref])
        t_ranks = {v: i + 1 for i, v in enumerate(sorted(values))}
        for k in ranking:
            ranking[k] += t_ranks[d[k][m_ref]]
    r_order = sorted(ranking, key=ranking.get)
    mlen = max((len(k) for k in ranking)) + len(str(len(ranking))) + 2
    file_dir = jp(OUTPUT_DIR, '![compl ranking].txt')
    with open(file_dir, 'w') as f:
        for i, k in enumerate(r_order):
            f.write('{:<{}}  {}\n\n'.format('{}. {}'.format(i + 1, k), mlen, ranking[k]))


def register_measures(text_obj, rdict):
    measures = COMPL_MEASURES
    for m in measures:
        rdict['![{}]'.format(m)] = getattr(text_obj, m)


def remove_punc(word):
    return get_word_and_punc(word)[0]


def safely_remove_word(i, end, orig_no_punc, ex_text, punc):
    # capitalize following word
    orig_w = orig_no_punc[i]
    if orig_w[0].isupper() and (not orig_w.isupper() or len(orig_w) == 1):
        if i != (end - 1):
            ex_text[i + 1] = smart_cap(ex_text[i + 1])
    lpunc, rpunc = punc[i]
    # add punc to following word
    if lpunc and i != (end - 1):
        ex_text[i + 1] = lpunc + ex_text[i + 1]
    # add punc to previous word
    if rpunc and i != 0:
        ex_text[i - 1] += rpunc
    ex_text[i] = ''


def save_all_stats(all_stats):
    file_dir = jp(OUTPUT_DIR, '[all ratios].txt')
    d = all_stats
    keys = sorted(d)
    subkeys = sorted(d[keys[0]])
    with open(file_dir, 'w') as f:
        for key in keys:
            ratios = ', '.join(['{}. {}'.format(k, d[key][k]) for k in subkeys])
            f.write('{}: {}\n\n'.format(key, ratios))
    subkeys.remove('_title_')
    for sk in subkeys:
        save_one_stat(all_stats, sk)


def save_ex(text_output, file_id, mode_id):
    ##        log.append('{}\n{}\n\n'.format(file_id, text_output))
    text_output = text_output.replace(NEW_LINE_MARKER, '\n\n')
    with open(jp(CWD, 'output', file_id, '{} ({}).txt'.format(file_id, mode_id)), 'w') as f:
        f.write(text_output.split('ANSWERS')[0])
    with open(jp(CWD, 'output', file_id, '{} ({}) (with key).txt'.format(file_id, mode_id)), 'w') as f:
        f.write(text_output)


def save_one_stat(rdicts_dict, key):
    file_dir = jp(OUTPUT_DIR, '{}.txt'.format(key))
    d = {k: v[key] for k, v in rdicts_dict.items()}
    mlen = max((len(k) for k in d))
    keys = sorted(d, key=d.get)
    with open(file_dir, 'w') as f:
        for k in keys:
            f.write('{:<{}}  {}\n\n'.format(k, mlen, d[k]))


def save_text_stats(text_stats):
    keys = sorted(text_stats)
    file_dir = jp(OUTPUT_DIR, text_stats['_title_'], '[stats].txt')
    with open(file_dir, 'w') as f:
        for k in keys:
            f.write('{:<17}{}\n'.format(k, text_stats[k]))


def smart_cap(word):
    w = ''
    for i, c in enumerate(word):
        if c.isalpha():
            w += c.capitalize()
            w += word[i + 1:]
            break
        elif c.isdigit():  # do not capitalize words starting with digits, like 14-year-old
            return word
        w += c
    return w


def quit():
    dump_log()
    input(' Press Enter to exit...')
    sys.exit()
        

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('')
        traceback.print_exc()
        dump_log()
        input('')

