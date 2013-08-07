\version "2.12.2"

\paper {
	#(set-paper-size "legal")
	left-margin = 13\mm
	indent = 22\mm
	#(define bottom-margin (* 1 cm))
	page-breaking-between-system-padding = 6\mm
	between-system-padding = 6\mm
}

\header {
	composer = ""
	title = "Movement 1"
	subtitle = ""
	copyright = ""
	tagline = ""
}


Emma =
\new Staff {
	\numericTimeSignature
	\set Staff.instrumentName = #"Soprano Saxophone"
	\set Staff.shortInstrumentName = #"SSax"
	\set Staff.midiInstrument = #"soprano sax"
	\clef treble
	\include "/Users/jmarmor/envs/jeff/src/jeff_output/20100523_182805_1/Mv_01/jeff_Mv_01_Emma_music.ly"

}

Paul =
\new Staff {
	\numericTimeSignature
	\set Staff.instrumentName = #"Trumpet"
	\set Staff.shortInstrumentName = #"tr"
	\set Staff.midiInstrument = #"trumpet"
	\clef treble
	\include "/Users/jmarmor/envs/jeff/src/jeff_output/20100523_182805_1/Mv_01/jeff_Mv_01_Paul_music.ly"

}

Katie =
\new Staff {
	\numericTimeSignature
	\set Staff.instrumentName = #"Casio SK1"
	\set Staff.shortInstrumentName = #"SK1"
	\set Staff.midiInstrument = #"lead 1 (square)"
	\clef treble
	\include "/Users/jmarmor/envs/jeff/src/jeff_output/20100523_182805_1/Mv_01/jeff_Mv_01_Katie_music.ly"

}

Christine =
\new Staff {
	\numericTimeSignature
	\set Staff.instrumentName = #"Flute"
	\set Staff.shortInstrumentName = #"f"
	\set Staff.midiInstrument = #"flute"
	\clef treble
	\include "/Users/jmarmor/envs/jeff/src/jeff_output/20100523_182805_1/Mv_01/jeff_Mv_01_Christine_music.ly"

}

Michael =
\new Staff {
	\numericTimeSignature
	\set Staff.instrumentName = #"Guitar"
	\set Staff.shortInstrumentName = #"gtr"
	\set Staff.midiInstrument = #"acoustic guitar (steel)"
	\clef treble
	\include "/Users/jmarmor/envs/jeff/src/jeff_output/20100523_182805_1/Mv_01/jeff_Mv_01_Michael_music.ly"

}

Mark =
\new PianoStaff <<
	\set PianoStaff.instrumentName = #"Piano"
	\set PianoStaff.shortInstrumentName = #"pn"
	\set PianoStaff.midiInstrument = #"acoustic grand"

	\include "/Users/jmarmor/envs/jeff/src/jeff_output/20100523_182805_1/Mv_01/jeff_Mv_01_Mark_music.ly"
>>

James =
\new Staff {
	\numericTimeSignature
	\set Staff.instrumentName = #"Bass"
	\set Staff.shortInstrumentName = #"bs"
	\set Staff.midiInstrument = #"acoustic bass"
	\clef bass
	\include "/Users/jmarmor/envs/jeff/src/jeff_output/20100523_182805_1/Mv_01/jeff_Mv_01_James_music.ly"

}

\score {
	<<
		\set Score.autoBeaming = ##f
		\override Score.Stem #'stemlet-length = #0.75
		\tempo 4 = 86

		\Emma
		\Paul
		\Katie
		\Christine
		\Michael
		\Mark
		\James

	>>
	\layout { }
	\midi { }
}