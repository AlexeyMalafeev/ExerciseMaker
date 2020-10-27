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
