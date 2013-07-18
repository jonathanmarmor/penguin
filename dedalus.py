import music21

INSTRUMENTS = [
    {
        'name': 'Flute',
        'score_order': 1,
        'short_name': 'fl',
        'musician_name': ''
    },
    {
        'name': 'Soprano Saxophone',
        'score_order': 2,
        'short_name': 'ss',
        'musician_name': ''
    },
    {
        'name': 'Viola',
        'score_order': 3,
        'short_name': 'vla',
        'musician_name': ''
    },
    {
        'name': 'Cello',
        'score_order': 4,
        'short_name': 'vc',
        'musician_name': ''
    },
    {
        'name': 'Trombone',
        'score_order': 5,
        'short_name': 'tbn',
        'musician_name': ''
    },
    {
        'name': 'Guitar',
        'score_order': 6,
        'short_name': 'gtr',
        'musician_name': 'Didier Aschour'
    }
]


def main():
    score = music21.stream.Score()
    for instrument in INSTRUMENTS:
        part = music21.stream.Part()
        part.id = instrument['name']
        score.insert(0, part)
    score.show('text')


if __name__ == '__main__':
    main()
