from engine import Engine
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument('name', help='name of language configuration')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='show intermediate sound changes'
    )
    parser.add_argument(
        '-r', '--repeat', type=int, default=1,
        help='generate multiple words'
    )
    parser.add_argument(
        '-p', '--phonetic', action='store_true',
        help='show phonetic transcriptions'
    )
    parser.add_argument(
        '-R', '--raw', action='store_true',
        help='show raw state machine output'
    )
    parser.add_argument(
        '-w', '--words', nargs='+',
        help='use given words instead of state machine output'
    )
    engine = Engine(parser)
    engine.run()
    
if __name__ == '__main__':
    main()