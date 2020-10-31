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


def make_paragraphs(words, par_ind):
    """Make paragraphs and return text as a string."""
    for i in par_ind:
        words[i] += PARAGRAPH_MARKER
    text = ' '.join([w for w in words if w])
    return text.replace(PARAGRAPH_MARKER+' ', '\n\n')


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
