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


class DerivMaker(GapMaker):
    deriv_dict = DERIV_DICT
    gap_distance = 2

    def check_condition(self, i, w):
        orig_w = self.orig_no_punc[i]
        return orig_w and orig_w.islower() and w in self.deriv_dict

    def make_gap(self, i, count):
        w = self.text[i]
        lpunc, rpunc = self.punc[i]
        lemma = self.deriv_dict.get(w)
        self.ans_key.append('({}) {}'.format(count, self.orig_no_punc[i]))
        self.ex_text[i] = '({}){}{}({}){}'.format(count, lpunc, GAP, lemma, rpunc)

    def set_instr(self):
        self.instr = 'Fill in the gaps with derivatives of the words in parentheses:'

    def set_tag(self):
        self.tag = '[deriv{}]'.format(get_gap_info(self.max_num_gaps))


class ErrorMaker(GapMaker):
    ans_key_is_text = True
    err_dict = ERR_DICT
    adj_err_dict = {'ful': 'full', 'ous': 'ouse'}
    verb_err_dict = {'s': '', 'es': '', 'ed': 'ing', 'ing': 'ed'}

    def __init__(self, text_obj):
        self.other_err_lookup = {}
        GapMaker.__init__(self, text_obj)

    def check_condition(self, i, w):
        orig_w = self.orig_no_punc[i]
        if not orig_w.isupper() and len(orig_w) >= 1:
            if w in self.err_dict:
                self.curr_err_key = w
                return True
            else:
                for ending, repl in self.adj_err_dict.items():
                    if w.endswith(ending):
                        self.curr_err_key = ending
                        self.other_err_lookup[w] = w[:-3] + repl
                        return True
                for ending, repl in self.verb_err_dict.items():
                    if w.endswith(ending) and w in VFORMS:
                        length = len(ending)
                        err = w[:-length] + repl
                        if err in VFORMS:
                            self.other_err_lookup[w] = err
                            self.curr_err_key = ending
                            return True

    def make_gap(self, i, count):
        # get error
        w = self.text[i]
        if w in self.err_dict:
            error = random.choice(self.err_dict[w])
        else:
            error = self.other_err_lookup[w]

        # disguise error
        orig_w = self.orig_no_punc[i]
        lpunc, rpunc = self.punc[i]
        error = error.capitalize() if orig_w[0].isupper() else error
        error = '{}{}{}'.format(lpunc, error, rpunc)
        # replace
        self.ex_text[i] = error
        # empty replacement case
        if remove_punc(self.ex_text[i]) == '':
            safely_remove_word(i, self.text_len, self.orig_no_punc, self.ex_text, self.punc)
        self.ans_key[i] = '({}) *{} -> {}'.format(count, self.ex_text[i], self.orig_with_punc[i])

    def mark_word(self, i, w):
        w = self.curr_err_key
        GapMaker.mark_word(self, i, w)

    def set_instr(self):
        self.instr = 'Find errors in the following text:'

    def set_tag(self):
        self.tag = '[err{}]'.format(get_gap_info(self.max_num_gaps))


class FragmentMaker(GapMaker):
    ans_key_is_text = True

    def __init__(self, text_obj, frag_after, frag_from, submode_name, max_frag_len):
        self.frag_after = frag_after  # set of word forms
        self.frag_from = frag_from  # set of word forms
        self.submode_name = submode_name
        self.min_frag_len = 3
        self.max_frag_len = max_frag_len
        self.indices = {}  # {sen_no: [ind_0, ind_1, ind_2, ...], ...}
        self.count = 1  # counter to mark gaps in ex_text
        self.mark_sen = -1  # mark rest of words in sentence mark_sen
        self.skip_sen = -1  # don't mark sentence skip_sen
        self.sen_mask = text_obj.sen_mask
        GapMaker.__init__(self, text_obj)

    def check_condition(self, i, w):
        curr_sen_ind = self.sen_mask[i]
        prev_w = self.text[i-1] if i != 0 else ''
        prev_rpunc = self.punc[i-1][1] if i != 0 else ''
        rpunc = self.punc[i][1]
        prev_sen_ind = self.sen_mask[i-1] if i != 0 else -1
        if curr_sen_ind == self.mark_sen:
            # if we have marked some words in this sentence already
            if curr_sen_ind == self.skip_sen:
                # if we have stopped marking words in this sentence
                return False
            elif rpunc and rpunc[-1] in ALL_SPLITTERS:
                # if we need to stop marking words in this sentence (end of clause)
                self.skip_sen = curr_sen_ind
                return True
            else:
                # if we have marked at least one word and want to continue marking (no end of clause)
                return True
        elif (w in self.frag_from or prev_w in self.frag_after or (prev_rpunc and prev_rpunc in ',;:')) and prev_sen_ind == curr_sen_ind:
            # if we can start marking words in a new sentence
            self.mark_sen = curr_sen_ind
            return True

    def finalize(self):
        GapMaker.finalize(self)
        fragments = []
        order = list(self.indices.keys())
        random.shuffle(order)
        for j, n in enumerate(order):
            frag = ' '.join([self.orig_with_punc[i] for i in self.indices[n]])
            frag = remove_punc(frag)  # this removes the punctuation at the beginning and at the end of the fragment
            frag = frag[0].lower() + frag[1:]  # hide the capitalization of the first letter
            new_frag = '{}) '.format(num_to_letter(j)) + frag
            fragments.append(new_frag)
        self.ex_text_string = '  {}\n\n{}'.format('\n  '.join(fragments), self.ex_text_string)

    def make_gap(self, i, count=None):
        curr_sen_ind = self.sen_mask[i]
        gap_indices = self.indices[curr_sen_ind]
        gap_starts = gap_indices[0]
        gap_ends = gap_indices[-1]
        if i == gap_starts:
            self.ex_text[i] = '({}) {}{}{}{}'.format(self.count, GAP, GAP, self.punc[gap_starts][0],
                                                     self.punc[gap_ends][1])
            self.ans_key[i] = '({}) {}'.format(self.count, self.orig_with_punc[i])
            self.count += 1
        # elif i == gap_ends:
        #     self.ex_text[i] = self.punc[i][1][-1]
        else:
            self.ex_text[i] = ''

    def mark_word(self, i, w):
        if self.mark_sen in self.indices:
            self.indices[self.mark_sen].append(i)
        else:
            self.indices[self.mark_sen] = [i]

    def run(self):
        self.ex_text = self.text_obj.words[:]
        self.ex_text_string = ''
        sample_dict = {}
        del_keys = []
        for k, v in self.indices.items():
            if self.min_frag_len <= len(v) <= self.max_frag_len:
                # remove fragments that are not too long and not too short
                sample_dict[k] = v
            else:
                del_keys.append(k)
        keep_keys = list(sample_dict)
        if len(sample_dict) > self.max_num_gaps:  # check if there are not too many fragments
            random.shuffle(keep_keys)
            # remove some fragments if too many
            keep_keys, extra = keep_keys[:self.max_num_gaps], keep_keys[self.max_num_gaps:]
            del_keys.extend(extra)
        for k in del_keys:
            del self.indices[k]  # still need to delete these for correct finalization
        sample = []
        for k in keep_keys:
            sample.extend(sample_dict[k])
        sample.sort()
        self.ans_key = self.ex_text[:]
        for i in sample:
            self.make_gap(i)
            self.reg_gap()
        # finalize
        self.finalize()

    def set_instr(self):
        self.instr = '''Fill the gaps with suitable fragments:'''

    def set_tag(self):
        self.tag = '[fragments {}{}]'.format(self.submode_name, get_gap_info(self.max_num_gaps))


class MissWordsMaker(GapMaker):
    ans_key_is_text = True
    repetition_allowed = True

    def __init__(self, text_obj, rem_words, category):
        self.rem_words = rem_words
        self.category = category
        GapMaker.__init__(self, text_obj)

    def check_condition(self, i, w):
        orig_w = self.orig_no_punc[i]
        return (orig_w[1:].islower() or len(w) == 1) and w in self.rem_words

    def make_gap(self, i, count):
        safely_remove_word(i, self.text_len, self.orig_no_punc, self.ex_text, self.punc)
        self.ans_key[i] = '({}) {}'.format(count, self.ans_key[i])

    def set_instr(self):
        self.instr = 'Insert {} where appropriate:'.format(self.category)

    def set_tag(self):
        self.tag = '[{}]'.format(self.category)


class OpenClozeMaker(GapMaker):
    def __init__(self, text_obj, rem_words, submode_name):
        self.rem_words = rem_words
        self.submode_name = submode_name
        GapMaker.__init__(self, text_obj)

    def check_condition(self, i, w):
        orig_w = self.orig_no_punc[i]
        return w in self.rem_words and (orig_w[1:].islower() or len(w) == 1)

    def make_gap(self, i, count):
        lpunc, rpunc = self.punc[i]
        self.ex_text[i] = '({}){}{}{}'.format(count, lpunc, GAP, rpunc)
        self.ans_key.append('({}) {}'.format(count, self.orig_no_punc[i]))

    def set_instr(self):
        self.instr = '''Fill the gaps with suitable words, such as articles, prepositions, conjunctions, pronouns and \
auxiliaries:'''

    def set_tag(self):
        self.tag = '[open {}{}]'.format(self.submode_name, get_gap_info(self.max_num_gaps))


class OrderedOpenClozeMaker(OpenClozeMaker):
    def __init__(self, text_obj, rem_words, order, submode_name):
        """order is a list of words, from less to more relevant"""
        self.rem_words = rem_words
        self.order = order
        self.submode_name = submode_name
        GapMaker.__init__(self, text_obj)

    def get_indices_from_dict(self, num_w):
        return ind_from_dict_ordered(self.indices, self.order, num_w, prox=self.gap_distance)


class PrepositionsMWM(MissWordsMaker):
    words_after_to = set('''a an the some any no this that these those me you him her it its itself us them my mine
    myself your yours yourself his himself hers herself our ours ourselves their theirs themselves what whatever who
    whom whoever something anything nothing someone anyone somebody anybody nobody somewhere anywhere nowhere such
    each all one two three four five six seven eight nine ten eleven twelve'''.split())

    def __init__(self, text_obj):
        rem_words = PREPOSITIONS
        category = 'prepositions'
        MissWordsMaker.__init__(self, text_obj, rem_words, category)

    def check_condition(self, i, w):
        orig_w = self.orig_no_punc[i]
        try:
            next_w = self.orig_no_punc[i+1]
            different_sentences = self.text_obj.sen_mask[i] != self.text_obj.sen_mask[i+1]
        except IndexError:
            next_w = ''
            different_sentences = True
        condition_for_to = w == 'to' and (next_w in self.words_after_to or next_w.istitle() or has_digit(next_w) or
                                          not next_w or different_sentences or
                                          (len(next_w) > 5 and next_w.endswith('ing')))
        return (orig_w[1:].islower() or len(w) == 1) and (w in self.rem_words or condition_for_to)


class SimpleVFormsMaker(GapMaker):
    vforms = SVFORMS
    submode = 'e'

    def check_condition(self, i, w):
        orig_w = self.orig_no_punc[i]
        not_after_to = i == 0 or self.text[i-1] != 'to'
        is_v1 = w in V1FORMS
        return (w in self.vforms and not orig_w[0].isupper()  # avoid clashes with names
                and (not is_v1 or not_after_to))  # avoid to + V1, too obvious

    def make_gap(self, i, count):
        w = self.text[i]
        lemma = self.vforms.get(w)
        lpunc, rpunc = self.punc[i]
        self.ans_key.append('({}) {}'.format(count, self.orig_no_punc[i]))
        self.ex_text[i] = '({}){}{}({}){}'.format(count, lpunc, GAP, lemma, rpunc)

    def set_instr(self):
        self.instr = 'Use the appropriate verb form to fill each of the gaps:'

    def set_tag(self):
        self.tag = '[verbs {}{}]'.format(self.submode, get_gap_info(self.max_num_gaps))

class AdvVFormsMaker(SimpleVFormsMaker):
    vforms = VFORMS
    skip_adverbs = SKIP_ADVERBS
    aux_pos = set('am is are was were be been being have has had having will would do does did'.split())
    aux_neg = set("not isn't aren't wasn't weren't don't doesn't didn't won't wouldn't haven't hasn't hadn't".split())
    submode = 'h'

    def make_gap(self, i, count):
        w = self.text[i]
        lemma = self.vforms.get(w)
        k = i - 1
        corr_form = [self.orig_no_punc[i]]
        while k >= 0:
            prev_w = self.text[k]
            if self.punc[k][1]:  # avoid some false 'long' forms
                break
            if prev_w in self.aux_pos:
                remove_w = True
            elif prev_w in self.aux_neg:
                lemma = 'not {}'.format(lemma)
                remove_w = True
            elif prev_w in self.skip_adverbs:
                remove_w = False
            else:
                break
            corr_form.append(self.orig_no_punc[k])
            if remove_w:
                self.ex_text[k] = ''
            k -= 1
        corr_form.reverse()
        answ = ' '.join(corr_form)
        self.ans_key.append('({}) {}'.format(count, answ))
        lpunc, rpunc = self.punc[i]
        self.ex_text[i] = '({}){}{}({}){}'.format(count, lpunc, GAP, lemma, rpunc)

        
class WordbankMaker(GapMaker):
    def check_condition(self, i, w):
        return (self.orig_no_punc[i].islower() and self.text.count(w) == 1) and w in COMMON10000

    def finalize(self):
        GapMaker.finalize(self)
        self.used.sort(key=str.lower)
        self.ex_text_string = '({})\n\n{}'.format(', '.join(self.used), self.ex_text_string)

    def make_ex(self, **kwargs):
        self.used = []
        GapMaker.make_ex(self, **kwargs)

    def make_gap(self, i, count):
        self.used.append(self.text[i])
        lpunc, rpunc = self.punc[i]
        self.ex_text[i] = '({}){}{}{}'.format(count, lpunc, GAP, rpunc)
        self.ans_key.append('({}) {}'.format(count, self.orig_no_punc[i]))

    def set_instr(self):
        self.instr = 'Fill the gaps with the words below:'

    def set_tag(self):
        self.tag = '[wordbank{}]'.format(get_gap_info(self.max_num_gaps))
        

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('')
        traceback.print_exc()
        dump_log()
        input('')

