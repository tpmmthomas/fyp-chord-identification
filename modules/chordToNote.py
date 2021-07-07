
#0 = C, 12 = B pitch class
major_offset = [0,4,7]
minor_offset = [0,3,7]
diminished_offset = [0,3,6]
augmented_offset = [0,4,8]
#Using chart in shared file as reference
major_key_Chordtype = [0,1,1,0,0,1,2]
minor_key_Chordtype = [1,2,0,1,1,0,2]

key = "Cmajor"
chord = "I"

#Determines whether the chord type (major,minor,etc)
def typeAnalysis(key,chord):
    isSeven = chord[-1:] == "7"
    if len(chord) >=6 and chord[0:6].upper() == "GERMAN":
        return "ger",True
    elif len(chord) >=6 and chord[0:6].upper() == "FRENCH":
        return "fre",True
    elif len(chord) >=7 and chord[0:7].upper() == "ITALIAN":
        return "ita",True
    elif len(chord)>=3 and chord[0:3].upper() == "DIM":
        return "dim",True
    elif len(chord)>=3 and chord[0:3].upper() == "AUG":
        return "aug",True
    elif chord[0] == "B":
        return "maj"
    
def startPosition():

