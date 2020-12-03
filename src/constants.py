# todo
CWD = os.getcwd()
INPUT_DIR = jp(CWD, 'input')
OUTPUT_DIR = jp(CWD, 'output')
LANG_DIR = jp(CWD, 'lang')

ANSW_SECTION = '\n\nANSWERS:\n\n'
GAP = '_____'
NEW_LINE_MARKER = " <-| "
NEW_LINE_MARKER_S = " <-| ".strip()
PARAGRAPH_MARKER = '[insert_paragraph]'
PUNCTUATION = set('. , ! ? ; : \x85'.split())
SEN_SPLITTERS = '!?.'
CLAUSE_SPLITTERS = ':,;'
ALL_SPLITTERS = SEN_SPLITTERS + CLAUSE_SPLITTERS
EOSEN_EXCEPTIONS = set('mr mrs rev lt'.split())

DUBIOUS_MEASURES = 'acad_ratio intw_ratio uw_ratio mean_word_len'.split()
COMPL_MEASURES = 'rare1_ratio rare2_ratio sen_ratio'.split()


# load derivatives
dr = jp(LANG_DIR, 'derivatives.txt')
temp_wf_list = [line.split() for line in open(dr)]
DERIV_DICT = dict([(words[x], words[0]) for words in temp_wf_list for x in range(len(words)) if x != 0])


# load verb forms (dict)
dr = jp(LANG_DIR, 'vforms.txt')
temp = [line.split() for line in open(dr)]
VFORMS = {}
for words in temp:
    w, lemma = words
    VFORMS[w] = lemma
V1FORMS = set(VFORMS.values())


# load simple verb forms (dict)
dr = jp(LANG_DIR, 'vforms_simple.txt')
temp = [line.split() for line in open(dr)]
SVFORMS = {}
for words in temp:
    w, lemma = words
    SVFORMS[w] = lemma
SVFORMS.update(VFORMS)


# load skip adverbs list
dr = jp(LANG_DIR, 'skip_adverbs.txt')
SKIP_ADVERBS = set(open(dr).read().split())


# load error rules
dr = jp(LANG_DIR, 'err_rules.txt')
ERR_DICT = {}
for line in open(dr):
    if '->' in line:
        line = line.split('->')
        k = line[0].strip()
        v = [e.strip() for e in line[1].split(',')]
        ERR_DICT[k] = v


# open close words
ARTICLES = set('a an the'.split())
AUXILIARIES = set('''am are be been being did do does doing done is has have having had was were will would'''.split())
CONJUNCTIONS = set('''although and as because besides but how however nor or since so that then therefore though until
when where whereas while'''.split())
PREPOSITIONS = set('''about above after around at away before below between by despite down during for from in
into of off on onto out over than through under up with within without'''.split())
PRONOUNS = set('''all another any anybody anyone anything enough every everybody everyone everything it its least
less many more most much no nobody none nothing one other others some somebody someone something such there what who
which'''.split())
ADDED = set('''again against ago anywhere apart back behind could each either few hardly if itself just never not
only ought rather regardless same scarcely should somewhere these this those throughout till too whatever whether whilst
whose why yet'''.split())
OPEN_CLOZE_EASY = set('''a an and another any are at but for from in is it many much of on or some the there to was
were what who will with'''.split())
OPEN_CLOZE_HARD = (ARTICLES | AUXILIARIES | CONJUNCTIONS | PREPOSITIONS | PRONOUNS | ADDED | set('to'))
##open('oc words.txt', 'w').write(' '.join(sorted(OPEN_CLOZE_HARD)))

# ordered open cloze words
FCE_ORDER = open(jp(LANG_DIR, 'oc_order_fce.txt')).read().split()
FCE_SET = set(FCE_ORDER)
CAE_ORDER = open(jp(LANG_DIR, 'oc_order_cae.txt')).read().split()
CAE_SET = set(CAE_ORDER)
CPE_ORDER = open(jp(LANG_DIR, 'oc_order_cpe.txt')).read().split()
CPE_SET = set(CPE_ORDER)

# fragments
FRAG_AFTER = set('say says said saying tell tells told telling think thinks thought thinking'.split())
FRAG_FROM = set('''after although and anything anywhere as because but despite if regardless since so than that though till until what whatever when where whereas whether which while who whose why with yet'''.split())

COMMON2000 = set(open(jp(LANG_DIR, 'common_2000+.txt')).read().split())
COMMON10000 = set(open(jp(LANG_DIR, 'common_10000+.txt')).read().split())
ACADEMIC = set(open(jp(LANG_DIR, 'academic.txt')).read().split())