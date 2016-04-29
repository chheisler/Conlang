from random import random
from json import load
from re import sub, escape

def main():
    word = _generate()
    print "raw: %s" % word
    word = _change(word)
    
def _generate():
    config = load(open('machine.json'))
    states = config['states']
    state = states[config['start']]
    output = []
    while state is not None:
        roll = random()
        total = 0.0
        for transition in state:
            total += transition['weight']
            if roll <= total:
                output.append(transition["emit"])
                state = states.get(transition["to"])
                break;
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