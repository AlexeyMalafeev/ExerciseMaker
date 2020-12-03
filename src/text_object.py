class TextObject(object):
    # not considered in word length
    comm1 = COMMON2000
    comm2 = COMMON10000
    acad_wl = ACADEMIC

    def __init__(self, text_input, file_name, target_dir=None):
        self.text = text_input
        self.paragraphs = []  # list of paragraph string
        self.paragraph_ind = []  # indices for splitting text into paragraphs
        self.normalize_input()
        self.words = self.text.split()
        self.words_no_punc = [remove_punc(w) for w in self.words]
        self.word_count = len([w for w in self.words_no_punc if w])
        self.bare_words = [w.lower() for w in self.words_no_punc]
        self.words_set = {w for w in self.bare_words if w}
        self.uword_count = len(self.words_set)
        self.rare1 = {w for w in self.words_set if w not in self.comm1 and not has_digit(w)}
        self.rare2 = {w for w in self.words_set if w not in self.comm2 and not has_digit(w)}
        self.academic = {w for w in self.words_set if w in self.acad_wl}
        self.punc_only = [get_punc(w) for w in self.words]
        self.sentences = self.get_sentences()  # list of lists; unchanged words
        self.sent_count = len(self.sentences)
        # fill sen_mask: [0, 0, 0, ..., 1, 1, 1, ..., 2...]
        self.sen_mask = []
        for i, sen in enumerate(self.sentences):
            self.sen_mask.extend([i] * len(sen))
        self.file_name = file_name
        self.measure_compl()
        self.make_dir(target_dir)
        self.write_stuff()

    def get_sentences(self):
        sens = []
        new_sen = []
        end = len(self.words) - 1

        def add_sen(sen):
            sens.append(sen)

        for i, w in enumerate(self.words):
            new_sen.append(w)

            lpunc, rpunc = self.punc_only[i]
            cond1 = any((c in rpunc for c in SEN_SPLITTERS))

            if i != end:
                nw = self.words_no_punc[i + 1]
                cond2 = ((nw and nw[0].isupper()) or self.words[i] == NEW_LINE_MARKER_S)  # i+1?
            else:
                cond2 = False

            barew = self.bare_words[i]
            cond3 = barew not in EOSEN_EXCEPTIONS

            cond4 = i == end

            if (cond1 and cond2 and cond3) or cond4:
                add_sen(new_sen)
                new_sen = []

        return sens

    def make_dir(self, target_dir):
        if not target_dir:
            target_dir = jp(OUTPUT_DIR, self.file_name)
        self.target_dir = target_dir
        ensure_dir(self.target_dir)


    def measure_compl(self):
        word_lengths = [len(w) for w in self.words_set]
        self.mean_word_len = mean(word_lengths)
        self.uw_ratio = get_ratio(self.uword_count, self.word_count)
        self.rare1_ratio = get_ratio(len(self.rare1), self.uword_count)
        self.rare2_ratio = get_ratio(len(self.rare2), self.uword_count)
        self.acad_ratio = get_ratio(len(self.academic), self.uword_count)
        self.sen_ratio = get_ratio(self.word_count, self.sent_count)

    def normalize_input(self):
        """Normalize text."""
        text_input = self.text.replace('\u2026', '... ')
        text_input = text_input.replace(chr(8216), '\'')
        text_input = text_input.replace(chr(8217), '\'')
        text_input = text_input.replace(chr(8220), '"')
        text_input = text_input.replace(chr(8221), '"')
        self.paragraphs = [p for p in text_input.split('\n') if p and not p.isspace()]
        x = -1
        for p in self.paragraphs:
            x += len(p.split())
            self.paragraph_ind.append(x)
        self.paragraph_ind.pop()  # remove the last index as it is useless
        self.text = text_input.replace('\n', ' ')
        # print(self.text)
        # print('\n'.join(self.paragraphs))
        # print(self.paragraph_ind)
        # input('...')

    def write_stuff(self):
        """Write stuff to the target directory (incl. a copy of the original text)."""
        fn = self.file_name
        tdir = self.target_dir

        # copy
        with open(jp(tdir, '{}.txt'.format(fn)), 'w') as f:
            f.write('\n\n'.join(self.paragraphs))

        # sentences
        with open(jp(tdir, '[sent].txt'), 'w') as f:
            sens = [' '.join((w for w in s)) for s in self.sentences]
            sens_st = ('\n'.join(('{}. {}'.format(i + 1, s) for i, s in enumerate(sens))))
            f.write(sens_st)

        # rare words
        open(jp(tdir, '[rare1].txt'), 'w').write(' '.join(sorted(self.rare1)))
        open(jp(tdir, '[rare2].txt'), 'w').write(' '.join(sorted(self.rare2)))
        # acad.words
        open(jp(tdir, '[acad].txt'), 'w').write(' '.join(sorted(self.academic)))