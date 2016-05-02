from re import sub

def transform(word, transform):
    for rule in transform['rules']:
        target = '(?:%s)' % _join(rule['from'])
        after = '(?<=(%s))' % _join(rule['after']) if 'after' in rule else '()'
        before = '(?=(%s))' % _join(rule['before']) if 'before' in rule else '()'
        pattern = after + target + before
        mapping = {key: value for key, value in zip(rule['from'], rule['to'])}
        word = sub(pattern, lambda match: _sub(match, mapping), word)
    return word

def _join(phones):
    return '|'.join(phone for phone in phones)
    
def _sub(match, mapping):
    to = mapping[match.string[match.start():match.end()]]
    return to.replace('^', match.group(1)).replace('$', match.group(2))
    