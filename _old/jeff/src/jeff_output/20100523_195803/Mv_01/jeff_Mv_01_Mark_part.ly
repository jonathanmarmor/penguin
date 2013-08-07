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
	instrument = "Piano"
	copyright = ""
	tagline = ""
}

partname =
\new PianoStaff <<
	\set PianoStaff.instrumentName = #"Piano"
	\set PianoStaff.shortInstrumentName = #"pn"
	\set PianoStaff.midiInstrument = #"acoustic grand"

	\include "/Users/jmarmor/envs/jeff/src/jeff_output/20100523_195803/Mv_01/jeff_Mv_01_Mark_music.ly"
>>

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