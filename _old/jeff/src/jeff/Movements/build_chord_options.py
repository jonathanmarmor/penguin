from build_pitchclasses import build_pitchclasses


def chordtypes_on_roots(chordtypes, roots=[0,1,2,3,4,5,6,7,8,9,10,11]):
	"""For each chordtype in chordtypes, makes a chord on each root in roots
	"""
	
	chords = []
	for pc in roots:
		for ct in chordtypes:
			new = tuple( build_pitchclasses(pc, ct) )
			chords.append(new)
	return chords

def chords_in_scale(chordtypes, scale=(0,2,4,5,7,9,11)):
	"""Build each chordtype in chordtypes on each note in scale.  If all the notes in each resulting chord is in the scale add to result.
	"""
	scale_set = set(scale)
	chords = []
	for pc in scale:
		for ct in chordtypes:
			new = tuple( build_pitchclasses(pc, ct) )
			
			if set(new).issubset(scale_set):
				chords.append(new)
	return chords

def containing(chords, pitches):
	"""return a list of chords in chords that contain all pitches in pitches.
	"""
	pitches_set = set(pitches)
	result = []
	for chord in chords:
		if pitches_set.issubset(set(chord)):
			result.append(chord)
	
	return result
	
def get_scaletype_on_all_pitchclasses( scaletype ):
	'''
	take a scale type in the form [0,2,4,5,7,9,11] or (0,4,7)
	return a list of the scale type transposed to each of the 12 pitchclasses
	'''
	result = []
	for root in range(12):
		new_pitchclasses = [ (root + relative_pc) % 12 for relative_pc in scaletype ]
		result.append( new_pitchclasses )
	
	return result

def get_scales_containing_chord( chord_pitchclasses, scale_types ):
	'''
	take a chord in pitchclass notation (0,4,7) or [1,5,8,0]
	take a list of scale types
	make a list of all scale types with roots on all pitchclass
	find all the scales that contain all the notes of the chord
	return this list of scales
	if there aren't any scales that contain this chord, return an empty list
	'''
	
	all_scales = []
	for scale_type in scale_types:
		scales_of_this_scale_type = get_scaletype_on_all_pitchclasses( scale_type )
		all_scales.extend( scales_of_this_scale_type )
	
	chord = set( tuple( chord_pitchclasses ) )

	possible_scales = []
	for s in all_scales:
		scale = set( tuple( s ) )
		if chord.issubset( scale):
			possible_scales.append( s )

	return possible_scales



def _test():
	from andre_chords import chordTypePitchclasses
	chordtypes = chordTypePitchclasses

	print build_chord_options(chordtypes)

if __name__ == "__main__":
	_test()