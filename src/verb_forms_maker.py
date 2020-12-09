class SimpleVFormsMaker(GapMaker):
    vforms = SVFORMS
    submode = 'e'

    def check_condition(self, i, w):
        orig_w = self.orig_no_punc[i]
        not_after_to = i == 0 or self.text[i - 1] != 'to'
        is_v1 = w in V1FORMS
        return (
            w in self.vforms
            and not orig_w[0].isupper()  # avoid clashes with names
            and (not is_v1 or not_after_to)
        )  # avoid to + V1, too obvious

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
    aux_pos = set(
        'am is are was were be been being have has had having will would do does did'.split()
    )
    aux_neg = set(
        "not isn't aren't wasn't weren't don't doesn't didn't won't wouldn't haven't hasn't hadn't".split()
    )
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
