from collections import defaultdict

class keydefaultdict(defaultdict):
    def __missing__(self, key):
        value = self[key] = self.default_factory(key)
        return value
        