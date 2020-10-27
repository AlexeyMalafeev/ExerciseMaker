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
