class FragmentMaker(GapMaker):
    ans_key_is_text = True

    def __init__(self, text_obj, frag_after, frag_from, submode_name, max_frag_len):
        self.frag_after = frag_after  # set of word forms
        self.frag_from = frag_from  # set of word forms
        self.submode_name = submode_name
        self.min_frag_len = 3
        self.max_frag_len = max_frag_len
        self.indices = {}  # {sen_no: [ind_0, ind_1, ind_2, ...], ...}
        self.count = 1  # counter to mark gaps in ex_text
        self.mark_sen = -1  # mark rest of words in sentence mark_sen
        self.skip_sen = -1  # don't mark sentence skip_sen
        self.sen_mask = text_obj.sen_mask
        GapMaker.__init__(self, text_obj)

    def check_condition(self, i, w):
        curr_sen_ind = self.sen_mask[i]
        prev_w = self.text[i - 1] if i != 0 else ''
        prev_rpunc = self.punc[i - 1][1] if i != 0 else ''
        rpunc = self.punc[i][1]
        prev_sen_ind = self.sen_mask[i - 1] if i != 0 else -1
        if curr_sen_ind == self.mark_sen:
            # if we have marked some words in this sentence already
            if curr_sen_ind == self.skip_sen:
                # if we have stopped marking words in this sentence
                return False
            elif rpunc and rpunc[-1] in ALL_SPLITTERS:
                # if we need to stop marking words in this sentence (end of clause)
                self.skip_sen = curr_sen_ind
                return True
            else:
                # if we have marked at least one word and want to continue marking (no end of clause)
                return True
        elif (
            w in self.frag_from or prev_w in self.frag_after or (prev_rpunc and prev_rpunc in ',;:')
        ) and prev_sen_ind == curr_sen_ind:
            # if we can start marking words in a new sentence
            self.mark_sen = curr_sen_ind
            return True

    def finalize(self):
        GapMaker.finalize(self)
        fragments = []
        order = list(self.indices.keys())
        random.shuffle(order)
        for j, n in enumerate(order):
            frag = ' '.join([self.orig_with_punc[i] for i in self.indices[n]])
            frag = remove_punc(
                frag
            )  # this removes the punctuation at the beginning and at the end of the fragment
            frag = frag[0].lower() + frag[1:]  # hide the capitalization of the first letter
            new_frag = '{}) '.format(num_to_letter(j)) + frag
            fragments.append(new_frag)
        self.ex_text_string = '  {}\n\n{}'.format('\n  '.join(fragments), self.ex_text_string)

    def make_gap(self, i, count=None):
        curr_sen_ind = self.sen_mask[i]
        gap_indices = self.indices[curr_sen_ind]
        gap_starts = gap_indices[0]
        gap_ends = gap_indices[-1]
        if i == gap_starts:
            self.ex_text[i] = '({}) {}{}{}{}'.format(
                self.count, GAP, GAP, self.punc[gap_starts][0], self.punc[gap_ends][1]
            )
            self.ans_key[i] = '({}) {}'.format(self.count, self.orig_with_punc[i])
            self.count += 1
        # elif i == gap_ends:
        #     self.ex_text[i] = self.punc[i][1][-1]
        else:
            self.ex_text[i] = ''

    def mark_word(self, i, w):
        if self.mark_sen in self.indices:
            self.indices[self.mark_sen].append(i)
        else:
            self.indices[self.mark_sen] = [i]

    def run(self):
        self.ex_text = self.text_obj.words[:]
        self.ex_text_string = ''
        sample_dict = {}
        del_keys = []
        for k, v in self.indices.items():
            if self.min_frag_len <= len(v) <= self.max_frag_len:
                # remove fragments that are not too long and not too short
                sample_dict[k] = v
            else:
                del_keys.append(k)
        keep_keys = list(sample_dict)
        if len(sample_dict) > self.max_num_gaps:  # check if there are not too many fragments
            random.shuffle(keep_keys)
            # remove some fragments if too many
            keep_keys, extra = keep_keys[: self.max_num_gaps], keep_keys[self.max_num_gaps :]
            del_keys.extend(extra)
        for k in del_keys:
            del self.indices[k]  # still need to delete these for correct finalization
        sample = []
        for k in keep_keys:
            sample.extend(sample_dict[k])
        sample.sort()
        self.ans_key = self.ex_text[:]
        for i in sample:
            self.make_gap(i)
            self.reg_gap()
        # finalize
        self.finalize()

    def set_instr(self):
        self.instr = '''Fill the gaps with suitable fragments:'''

    def set_tag(self):
        self.tag = '[fragments {}{}]'.format(self.submode_name, get_gap_info(self.max_num_gaps))
