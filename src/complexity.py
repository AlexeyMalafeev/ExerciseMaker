def get_ratio(val_a, val_b):
    return round(val_a / val_b, 3)


def rank(rdicts_dict):
    d = rdicts_dict
    ranking = {k: 0 for k in d}
    for m in COMPL_MEASURES:
        m_ref = '![{}]'.format(m)
        values = set()
        for k in d:
            values.add(d[k][m_ref])
        t_ranks = {v: i + 1 for i, v in enumerate(sorted(values))}
        for k in ranking:
            ranking[k] += t_ranks[d[k][m_ref]]
    r_order = sorted(ranking, key=ranking.get)
    mlen = max((len(k) for k in ranking)) + len(str(len(ranking))) + 2
    file_dir = jp(OUTPUT_DIR, '![compl ranking].txt')
    with open(file_dir, 'w') as f:
        for i, k in enumerate(r_order):
            f.write('{:<{}}  {}\n\n'.format('{}. {}'.format(i + 1, k), mlen, ranking[k]))


def register_measures(text_obj, rdict):
    measures = COMPL_MEASURES
    for m in measures:
        rdict['![{}]'.format(m)] = getattr(text_obj, m)


def save_all_stats(all_stats):
    file_dir = jp(OUTPUT_DIR, '[all ratios].txt')
    d = all_stats
    keys = sorted(d)
    subkeys = sorted(d[keys[0]])
    with open(file_dir, 'w') as f:
        for key in keys:
            ratios = ', '.join(['{}. {}'.format(k, d[key][k]) for k in subkeys])
            f.write('{}: {}\n\n'.format(key, ratios))
    subkeys.remove('_title_')
    for sk in subkeys:
        save_one_stat(all_stats, sk)


def save_one_stat(rdicts_dict, key):
    file_dir = jp(OUTPUT_DIR, '{}.txt'.format(key))
    d = {k: v[key] for k, v in rdicts_dict.items()}
    mlen = max((len(k) for k in d))
    keys = sorted(d, key=d.get)
    with open(file_dir, 'w') as f:
        for k in keys:
            f.write('{:<{}}  {}\n\n'.format(k, mlen, d[k]))


def save_text_stats(text_stats):
    keys = sorted(text_stats)
    file_dir = jp(OUTPUT_DIR, text_stats['_title_'], '[stats].txt')
    with open(file_dir, 'w') as f:
        for k in keys:
            f.write('{:<17}{}\n'.format(k, text_stats[k]))