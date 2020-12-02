import os
import sys


log = []


def all_exercises(text_obj):
    """
Do all modes and return stats dict.
"""
    stats = {}
    stats_mapping = [('_title_', 'file_name'),
                     ('_word_count_', 'word_count'),
                     ('_uword_count_', 'uword_count'),
                     ('_sent_count_', 'sent_count')]
    for k, v in stats_mapping:
        stats[k] = getattr(text_obj, v, 'undefined')
    std_args = ({'max_num_gaps': 0}, {'max_num_gaps': 10}, {'max_num_gaps': 20})
    # legend: ex_class, init_args, make_ex_args
    exs = ((DerivMaker, (), std_args),
           (ErrorMaker, (), std_args),
           (FragmentMaker, (FRAG_AFTER, FRAG_FROM, 'short', 7), ({'max_num_gaps': 10},)),
           (FragmentMaker, (FRAG_AFTER, FRAG_FROM, 'long', 12), ({'max_num_gaps': 10},)),
           (MissWordsMaker, (ARTICLES, 'articles'), ({'max_num_gaps': 0},)),
           (OpenClozeMaker, (OPEN_CLOZE_EASY, 'e'), ({'max_num_gaps': 0},)),
           (OpenClozeMaker, (OPEN_CLOZE_HARD, 'h'), std_args),
           (OrderedOpenClozeMaker, (FCE_SET, FCE_ORDER, 'fce'), ({'max_num_gaps': 15},)),
           (OrderedOpenClozeMaker, (CAE_SET, CAE_ORDER, 'cae'), ({'max_num_gaps': 15},)),
           (OrderedOpenClozeMaker, (CPE_SET, CPE_ORDER, 'cpe'), ({'max_num_gaps': 15},)),
           (PrepositionsMWM, (), ({'max_num_gaps': 0},)),
           (SimpleVFormsMaker, (), ({'max_num_gaps': 0},)),
           (AdvVFormsMaker, (), std_args),
           (WordbankMaker, (), std_args)
    )
    for ex_class, init_args, arg_dicts in exs:
        init_args = (text_obj,) + init_args
        ex_obj = ex_class(*init_args)
        for arg_dict in arg_dicts:
            ex_obj.make_ex(**arg_dict)
            stats[ex_obj.tag] = ex_obj.get_gaps_ratio()
    return stats


def dump_log():
    with open('log.txt', 'w') as f:
        f.write('\n'.join(log))


def main():
    # ensure 'input' and 'output' folders
    ensure_dir(INPUT_DIR)
    ensure_dir(OUTPUT_DIR)

    # open all files in 'input' folder and process them
    all_stats = {}
    for file_name in os.listdir(INPUT_DIR):
        with open(jp(INPUT_DIR, file_name)) as f:
            text_input = f.read()
        file_name = file_name.replace('.txt', '')
        text_obj = TextObject(text_input, file_name)

        # run all modes
        stats = all_exercises(text_obj)
        register_measures(text_obj, stats)
        save_text_stats(stats)
        all_stats[file_name] = stats

    save_all_stats(all_stats)
    rank(all_stats)
    quit()


def save_ex(text_output, file_id, mode_id):
    ##        log.append('{}\n{}\n\n'.format(file_id, text_output))
    text_output = text_output.replace(NEW_LINE_MARKER, '\n\n')
    with open(jp(CWD, 'output', file_id, '{} ({}).txt'.format(file_id, mode_id)), 'w') as f:
        f.write(text_output.split('ANSWERS')[0])
    with open(jp(CWD, 'output', file_id, '{} ({}) (with key).txt'.format(file_id, mode_id)), 'w') as f:
        f.write(text_output)
        

if __name__ == '__main__':
    main()
