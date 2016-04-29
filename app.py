from random import random
from json import load
from re import sub, escape
from collections import defaultdict

def main():
    word = _generate()
    print "raw: %s" % word
    word = _change(word)
    
def _generate():
    config = load(open('machine.json'))
    states = config['states']
    name = config['start']
    output = []
    visits = defaultdict(int)
    while name is not None:
        state = states[name]
        roll = random()
        total = 0.0
        for transition in state:
            total += transition['weight']
            if 'add' in transition:
                total = min(max(total + transition['add'] * visits[name], 0.0), 1.0)
            if roll <= total:
                output.append(transition["emit"])
                next_name = transition["to"]
                break;
        visits[name] += 1
        name = next_name
    return ''.join(output)
    
def _change(word):
    config = load(open('machine.json'))
    changes = config['changes']
    for change in changes:
        for rule in change['rules']:
            target = '(?:%s)' % _join(rule['from'])
            after = '(?<=(%s))' % _join(rule['after']) if 'after' in rule else '()'
            before = '(?=(%s))' % _join(rule['before']) if 'before' in rule else '()'
            pattern = after + target + before
            map = {k: v for k, v in zip(rule['from'], rule['to'])}
            word = sub(pattern, lambda match: _sub(match, map), word)
        print '%s: %s' % (change['name'], word)
    return word
    
def _join(phones):
    return '|'.join([escape(phone) for phone in phones])

def _sub(match, map):
    to = map[match.string[match.start():match.end()]]
    return to.replace('^', match.group(1)).replace('$', match.group(2))
    
def _format(phone):
    return phone.replace('^', r'\1').replace('$', r'\2')
    
if __name__ == '__main__':
    main()