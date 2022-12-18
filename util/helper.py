def get_dict_from_list_by_key(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))