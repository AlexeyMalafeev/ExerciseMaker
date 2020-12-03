class GapMaker(BaseExMaker):
    """General GapMaker class. Not to be instantiated directly.
Needs: instr, tag, check_condition(i, w), make_gap(i, count)."""
    ans_key_is_text = False
    max_num_gaps = 0
    gap_distance = 3
    repetition_allowed = False

    def check_condition(self, i, w):
        input('check_condition for {} is not implemented'.format(self.__class__.__name__))

    def finalize(self):
        self.ex_text_string = make_paragraphs(self.ex_text, self.text_obj.paragraph_ind)
        # self.ex_text_string = ' '.join([w for w in self.ex_text if w])
        if self.ans_key_is_text:
            self.ans_key_string = make_paragraphs(self.ans_key, self.text_obj.paragraph_ind)
            # self.ans_key_string = ' '.join(self.ans_key)
        else:
            self.ans_key_string = '; '.join(self.ans_key)

    def first_pass(self):
        self.indices = {}
        # find all words that can be removed
        for i, w in enumerate(self.text):
            if self.check_condition(i, w):
                self.mark_word(i, w)

    def get_indices_from_dict(self, num_w):
        return ind_from_dict(self.indices, num_w, prox=self.gap_distance)

    def make_gap(self, i, count):
        input('make_gap for {} is not implemented'.format(self.__class__.__name__))

    def mark_word(self, i, w):
        if w in self.indices:
            self.indices[w].append(i)
        else:
            self.indices[w] = [i]

    def run(self):
        self.ex_text = self.text_obj.words[:]
        self.ex_text_string = ''
        if not self.repetition_allowed:
            # remove some words
            if not self.max_num_gaps:
                num_w = len(self.indices)
            elif self.max_num_gaps <= 1:
                num_w = round((len(self.indices) * self.max_num_gaps))
            else:
                num_w = self.max_num_gaps
            sample = self.get_indices_from_dict(num_w)
        else:
            sample = [ind for ind_list in self.indices.values() for ind in ind_list]
        sample.sort()
        count = 1
        if self.ans_key_is_text:
            self.ans_key = self.ex_text[:]
        else:
            self.ans_key = []
        for i in sample:
            self.make_gap(i, count)
            self.reg_gap()
            count += 1
        # finalize
        self.finalize()
