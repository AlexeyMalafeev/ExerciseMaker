from complexity import get_ratio


class BaseExMaker(object):
    def __init__(self, text_obj):
        self.text_obj = text_obj
        self.tag = ''
        self.instr = ''
        self.text = self.text_obj.bare_words[:]
        self.text_len = len(self.text)
        self.orig_no_punc = self.text_obj.words_no_punc[:]
        self.orig_with_punc = text_obj.words[:]
        self.ex_text = []
        self.ex_text_string = ''
        self.punc = self.text_obj.punc_only
        self.gap_count = 0
        self.ans_key = []
        self.ans_key_string = ''

        self.first_pass()

    def first_pass(self):
        input('first_pass for {} is not implemented'.format(self.__class__.__name__))

    def get_gaps_ratio(self):
        return get_ratio(self.gap_count, self.text_obj.word_count)

    def make_ex(self, **kwargs):
        self.gap_count = 0
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.set_tag()
        self.set_instr()
        self.run()
        self.save()

    def reg_gap(self):
        self.gap_count += 1

    def run(self):
        input('run for {} is not implemented'.format(self.__class__.__name__))

    def save(self):
        """
        Save self.ex_text_string and self.ans_key_string to a text file;
        self.instr and self.tag should also be defined within the subclass."""
        self.ex_text_string = self.ex_text_string.replace(NEW_LINE_MARKER, '\n\n')
        self.ans_key_string = self.ans_key_string.replace(NEW_LINE_MARKER, '\n\n')
        fn = self.text_obj.file_name
        tag = self.tag
        instr = self.instr
        tdir = self.text_obj.target_dir
        self.ex_text_string = '{}\n\n{}'.format(instr, self.ex_text_string)
        with open(os.path.join(tdir, '{} {}.txt'.format(fn, tag)), 'w') as f:
            f.write(self.ex_text_string)
        with open(os.path.join(tdir, '{} {} [key].txt'.format(fn, tag)), 'w') as f:
            f.write(self.ex_text_string + ANSW_SECTION + self.ans_key_string)

    def set_instr(self):
        input('instr for {} is not set'.format(self.__class__.__name__))

    def set_tag(self):
        input('tag for {} is not set'.format(self.__class__.__name__))
