from util import keydefaultdict
from json import load
from collections import defaultdict
from random import random
from transform import transform

class Engine:
    def __init__(self, parser):
        self._args = parser.parse_args()
        self._config = load(open(self._args.name + '.json'))
        self._scales = keydefaultdict(self._scale)
        
    def run(self):
        if self._args.words is None:
            words = [self._generate() for x in range(self._args.repeat)]
        else:
            words = self._args.words
        for word in words:
            for change in self._config['changes']:
                word = transform(word, change)
                if self._args.verbose:
                    print '%s: %s' % (change['name'], self._format(word))
            if not self._args.verbose:
                print self._format(word)
            else:
                print
        
    def _generate(self):
        states = self._config['states']
        name = self._config['start']
        output = []
        visits = defaultdict(int)
        while name is not None:
            state = states[name]
            roll = random() * self._scales[name]
            total = 0.0
            for transition in state:
                total += transition['weight']
                if 'add' in transition:
                    total += transition['add'] * visits[name]
                total = min(max(total, 0.0), self._scales[name])
                if roll <= total:
                    output.append(transition['emit'])
                    next_name = transition['to']
                    break;
            visits[name] += 1
            name = next_name
        output = ''.join(output)
        if self._args.raw:
            print 'raw: %s' % self._format(output)
        return output
        
    def _scale(self, key):
        state = self._config['states'][key]
        return sum(transition['weight'] for transition in state)
        
    def _format(self, word):
        transliteration = self._config['transliteration']
        transliterated = transform(word, transliteration)
        if self._args.phonetic:
            return '%s [%s]' %  (transliterated, word)
        return transliterated
        