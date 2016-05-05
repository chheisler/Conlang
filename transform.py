from re import sub

def transform(word, transform):
    for rule in transform['rules']:
        if 'map' in rule:
            target = '(?:%s)' % '|'.join(key for key in rule['map'])
        else:
            target = rule['from']
        if 'where' in rule:
            after, before = rule['where'].split('_')
        else:
            after = rule['after'] if 'after' in rule else ''
            before = rule['before'] if 'before' in rule else ''
        pattern = ('(?<=%s)' % after) + target + ('(?=%s)' % before)
        if 'map' in rule:
            word = sub(pattern, lambda match: _map(match, rule['map']), word)
        else:
            word = sub(pattern, rule['to'], word)
    return word
    
def _map(match, map):
    to = map[match.string[match.start():match.end()]]
    return sub(r'\\(\d)', lambda m: match.group(int(m.group(1))), to)
    
    