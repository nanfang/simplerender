from __future__ import unicode_literals
from UserDict import UserDict

_concat = ''.join

# core render
def render_string(content, model, prefix, suffix):
    blocks = []
    matching = False
    total_len = len(content)
    prefix_len = len(prefix)
    suffix_len = len(suffix)
    i = 0
    j = 0
    while i < total_len:
        if not matching:
            if prefix == content[i:i + prefix_len]:
                matching = True
                i += prefix_len
                while prefix == content[i + 1 - prefix_len:i + 1]:
                    i += 1
                blocks.append(content[j:i-prefix_len])
                j=i
            else:
                i += 1
        else:
            if suffix == content[i:i + suffix_len]:
                matching = False
                if i>j:
                    key = content[j:i]
                    if key in model:
                        blocks.append(model[key])
                        i += suffix_len

                    else:
                        blocks.append(prefix)
                        blocks.append(key)
                else:
                    blocks.append(prefix)
                j = i
            else:
                i += 1
    if matching:
        blocks.append(prefix + content[j:])
    else:
        blocks.append(content[j:])
    return _concat(blocks)


def xstr(s):
    return '' if s is None else str(s)

class CaseInsensitiveDict(UserDict):
    def __init__(self, dict=None, **kwargs):
        self.data = {}
        if dict is not None:
            for key, value in dict.iteritems():
                self.data[key.upper()]=value
        if len(kwargs):
            for key, value in kwargs:
                self.data[key.upper()]=value

    def __getitem__(self, key):
        key = key.upper()
        if key in self.data:
            return self.data[key]
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)

    def __setitem__(self, key, item):
        key = key.upper()
        self.data[key] = item

    def __delitem__(self, key):
        key = key.upper()
        del self.data[key]

    def __contains__(self, key):
        key = key.upper()
        return key in self.data

    def has_key(self, key):
        return key.upper() in self.data

    def pop(self, key, *args):
        key = key.upper()
        return self.data.pop(key, *args)

# model with features like
class FeatureModel(object):
    def __init__(self, raw_model, insensitive=False, alts=None, formatter=xstr):
        self.model = CaseInsensitiveDict(raw_model) if insensitive else raw_model
        alts = alts if alts else {}
        self.alts = CaseInsensitiveDict(alts) if insensitive else alts
        self.formatter = formatter

    def __contains__(self, key):
        return key in self.model or key in self.alts

    def __getitem__(self, key):
        return self.formatter(self.model.get(key) or self.alts[key])

# render function with features
def xrender(content, model, alts=None, formatter=xstr):
    return render_string(content, FeatureModel(model, insensitive=True, alts=alts, formatter=formatter), '##', '##')
