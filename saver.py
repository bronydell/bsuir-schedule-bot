import shelve

shelve_name = "data"


def save_pref(user, key, value):
    d = shelve.open(shelve_name)
    d[str(user) + '.' + str(key)] = value
    d.close()


def save_global_pref(key, value):
    d = shelve.open(shelve_name)
    d['global.' + str(key)] = value
    d.close()


def open_pref(user, key, default):
    d = shelve.open(shelve_name)
    if (str(user) + '.' + str(key)) in d:
        return d[str(user) + '.' + str(key)]
    else:
        return default


def open_global_pref(key, default):
    d = shelve.open(shelve_name)
    if ('global.' + str(key)) in d:
        return d['global.' + str(key)]
    else:
        return default
