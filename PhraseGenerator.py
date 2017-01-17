#!usr/bin/env python3

import random
from MidiFile3 import MIDIFile

def generateScale():
	scale = []
	nMax = -1
	while(nMax < 11):
		# Generate next note in scale
		note = random.randint(1,2)
		if nMax == 10: note = 1
		scale.append(nMax + note)
		nMax += note

	return scale

def noteToLetter(note):
	letters = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	return letters[note]

def letterToNote(letter):
	letters = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	return letters.index(letter.upper())

def showScale(scale):
	"""Shows scale to user in letter form."""
	lScale = []
	for n in scale:
		lScale.append(noteToLetter(n))

	return lScale

def getExistingScale():
	"""Allows user to pick an existing scale."""
	chromatic = [0,1,2,3,4,5,6,7,8,9,10,11]
	major = [0,2,4,5,7,9,11]
	nMinor = [0,2,3,5,7,8,10]
	hMinor = [0,2,3,5,7,8,11]
	majPent = [0,2,4,7,9]
	minPent = [0,3,5,7,10]
	blues = [0,3,5,6,7,10]
	wholeTone = [0,2,4,6,8,10]
	octaves = [0]

	chosen = input("What scale? (chromatic, major, n. minor, h. minor, maj. pent, min. pent, blues, whole tone, octaves) ").lower()
	if chosen == "chromatic": return chromatic
	elif chosen == "major": return major
	elif chosen == "nminor": return nMinor
	elif chosen == "hminor": return hMinor
	elif chosen == "majpent": return majPent
	elif chosen == "minpent": return minPent
	elif chosen == "blues": return blues
	elif chosen == "wholetone": return wholeTone
	elif chosen == "octaves": return octaves

def expandScale(scale, octaves):
	xScale = []
	for i in range(octaves):
		xScale += [x+(12*i) for x in scale]
	return xScale

# Get phrase details
oLength = int(input("Phrase length (in beats): "))
oTempo = int(input("Phrase tempo (in bpm): "))
oOctaves = int(input("Octave range: "))
minVel = int(input("Minimum velocity (0-127): "))
maxVel = int(input("Maximum velocity (0-127): "))
oKey = letterToNote(input("Key: "))
oName = input("Name: ")
pOfNote = int(input("Percentage probability of a note being present: "))
minLength = float(input("Minimum length of note: "))
maxLength = float(input("Maximum length of note: "))
generatingScale = int(input("Generate scale (1) or choose a scale (2)?"))

# Initialise MIDI file details
oFile = MIDIFile(1)
oFile.addTrackName(0, oLength, oName)
oFile.addTempo(0, oLength, oTempo)

# Generate scale or allow user to choose a scale
if(generatingScale == 1):
	scale = generateScale()
	print("Scale generated as:", showScale(scale))
else:
	scale = getExistingScale()

# Expand scale to octave range
scale = expandScale(scale, oOctaves)

# Generate notes in phrase
cTime = 0.0
while(cTime < oLength):
	# Generate length of note
	nLength = (random.uniform(minLength, maxLength))

	# Generate pitch of note
	nPitch = 36 + oKey + random.choice(scale)

	# Generate velocity of note
	nVelocity = random.randint(minVel,maxVel)

	# Add note to track if it is selected to appear based on probability
	if random.randint(1,100) <= pOfNote: oFile.addNote(0,0,nPitch,cTime,nLength,nVelocity)

	cTime += nLength

# Write MIDI file to disk
binfile = open((oName+".mid"), 'wb') 
oFile.writeFile(binfile)
binfile.close()

# Tell user that file has been created
print("File has been created as '" + oName + ".mid'!")
