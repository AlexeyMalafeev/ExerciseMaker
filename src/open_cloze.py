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
