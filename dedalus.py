"""A piece of music for Dedalus ensemble.

http://www.youtube.com/watch?v=_syDjTX90zA&feature=share&list=PL477C973BF13F8BBE

"""

import datetime

import music21


def get_score():
    score = music21.stream.Score()

    md = music21.metadata.Metadata()
    md.title = 'Music for Dedalus Ensemble'
    md.composer = 'Jonathan Marmor'
    md.date = datetime.datetime.utcnow().strftime('%Y/%m/%d')
    md.groupTitle = 'Dedalus'
    md.dedication = 'Didier Aschour'
    score.insert(0, md)

    fl = music21.instrument.Flute()
    sax = music21.instrument.SopranoSaxophone()
    vla = music21.instrument.Viola()
    vc = music21.instrument.Violoncello()
    tbn = music21.instrument.Trombone()
    gtr = music21.instrument.ElectricGuitar()

    instruments = [fl, sax, vla, vc, tbn, gtr]
    parts = []
    for i in instruments:
        part = music21.stream.Part()
        part.insert(0, i)
        part.id = i.instrumentAbbreviation
        score.insert(0, part)
        parts.append(part)

    score.insert(0, music21.layout.StaffGroup(parts))

    return score


# def add_phrase(score):


if __name__ == '__main__':
    score = get_score()
    score.show()
