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
	instrument = "Bass"
	copyright = ""
	tagline = ""
}

partname =
\new Staff {
	\numericTimeSignature
	\set Staff.instrumentName = #"Bass"
	\set Staff.shortInstrumentName = #"bs"
	\set Staff.midiInstrument = #"acoustic bass"
	\clef bass
	\transpose c c' % transpose the part! first argument is "sounds", second is "written"

	\include "/Users/jmarmor/envs/jeff/src/jeff_output/20100523_195803/Mv_01/jeff_Mv_01_James_music.ly"

}

\score {
	<<
		\set Score.autoBeaming = ##f
		\override Score.Stem #'stemlet-length = #0.75
		\tempo 4 = 62
		\partname

	>>
	\layout { }
	\midi { }
}