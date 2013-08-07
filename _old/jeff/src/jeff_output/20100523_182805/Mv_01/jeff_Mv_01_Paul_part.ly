\version "2.12.2"

\paper {
	#(set-paper-size "legal")
	#(define bottom-margin (* 1 cm))
	page-breaking-between-system-padding = 6\mm
	left-margin = 13\mm
	indent = 22\mm
	between-system-padding = 6\mm
}

\header {
	composer = ""
	title = "Movement 1"
	subtitle = ""
	instrument = "Trumpet"
	copyright = ""
	tagline = ""
}

partname =
\new Staff {
	\numericTimeSignature
	\set Staff.instrumentName = #"Trumpet"
	\set Staff.shortInstrumentName = #"tr"
	\set Staff.midiInstrument = #"trumpet"
	\clef treble
	\transpose bes c' % transpose the part! first argument is "sounds", second is "written"

	\include "/Users/jmarmor/envs/jeff/src/jeff_output/20100523_182805_1/Mv_01/jeff_Mv_01_Paul_music.ly"

}

\score {
	<<
		\set Score.autoBeaming = ##f
		\override Score.Stem #'stemlet-length = #0.75
		\tempo 4 = 86
		\partname

	>>
	\layout { }
	\midi { }
}