from gap_maker import GapMaker


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
