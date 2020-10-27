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
