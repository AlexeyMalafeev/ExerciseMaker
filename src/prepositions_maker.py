class PrepositionsMWM(MissWordsMaker):
    words_after_to = set(
        '''a an the some any no this that these those me you him her it its itself us them my mine
    myself your yours yourself his himself hers herself our ours ourselves their theirs themselves what whatever who
    whom whoever something anything nothing someone anyone somebody anybody nobody somewhere anywhere nowhere such
    each all one two three four five six seven eight nine ten eleven twelve'''.split()
    )

    def __init__(self, text_obj):
        rem_words = PREPOSITIONS
        category = 'prepositions'
        MissWordsMaker.__init__(self, text_obj, rem_words, category)

    def check_condition(self, i, w):
        orig_w = self.orig_no_punc[i]
        try:
            next_w = self.orig_no_punc[i + 1]
            different_sentences = self.text_obj.sen_mask[i] != self.text_obj.sen_mask[i + 1]
        except IndexError:
            next_w = ''
            different_sentences = True
        condition_for_to = w == 'to' and (
            next_w in self.words_after_to
            or next_w.istitle()
            or has_digit(next_w)
            or not next_w
            or different_sentences
            or (len(next_w) > 5 and next_w.endswith('ing'))
        )
        return (orig_w[1:].islower() or len(w) == 1) and (w in self.rem_words or condition_for_to)
