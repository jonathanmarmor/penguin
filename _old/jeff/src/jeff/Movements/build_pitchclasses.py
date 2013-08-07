### build pitchclasses from root and chord type
### 2009-09-07
###

def build_pitchclasses(root, chordtype):
	'''build pitchclasses of a chord from root and chord type (if chord type is in relative notation (eg. [0,4,7]) rather than interval notation (eg. [4,3,5]))'''
	result = []
	for pc_offset in chordtype:
		newnote = (root + pc_offset) % 12
		result.append(newnote)
	return result
	
def build_pitchclasses_from_intervals(root, chord_intervals):
	'''build pitchclasses of a chord from root and chord type (if chord type is in interval notation (eg. [4,3,5]) rather than relative notation (eg. [0,4,7]))'''
	result = [root]
	previousNote = root
	for interval in chord_intervals[:-1]:
		newnote = (previousNote + interval) % 12
		result.append(newnote)
		previousNote = newnote
	return result
	

if __name__ == "__main__":
	root = 2
	
	chordtype = [0,4,7,10]
	chord_pcs1 = build_pitchclasses(root, chordtype)
	
	chordintervals = [4,3,3,2]
	chord_pcs2 = build_pitchclasses_from_intervals(root, chordintervals)
	
	# result will be 2,6,9,0
	
	print chord_pcs1
	print chord_pcs2