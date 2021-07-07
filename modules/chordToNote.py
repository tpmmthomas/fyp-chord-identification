#0 = C, 12 = B pitch class
major_offset = [0,4,7]
minor_offset = [0,3,7]
diminished_offset = [0,3,6]
augmented_offset = [0,4,8]
german_offset = [0,]
#Using chart in shared file as reference
major_key_Chordtype = [0,1,1,0,0,1,2]
minor_key_Chordtype = [1,2,0,1,1,0,2]
key_map ={0:"maj",1:"min",2:"dim"}
pitch_to_index={"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
key = "Cminor"
chord = "II"

#Input chord format: either only I to VII (can with +, - and 7), german, f
'''
def InputValidation(key,chord):
    if key[-5:].upper() != "MAJOR" and key[-5:].upper() != "MINOR":
        print("Invalid key.")
        return False
    if len(chord) >=6 and chord[:6].upper() == "GERMAN":
        chord = chord[-6:]
    if len(chord) >=6 and chord[:6].upper() == "FRENCH":
        chord = chord[-6:]
    if len(chord) >=7 and chord[:7].upper() == "ITALIAN":
        chord = chord[-7:]
'''    
def RomanToInt(x):
    if len(x) >=3 and x[:3].upper() == "III":
        return 3
    elif len(x) >=3 and x[:3].upper() == "VII":
        return 7
    elif len(x) >=2 and x[:3].upper() == "II":
        return 2
    elif len(x) >=2 and x[:3].upper() == "IV":
        return 4
    elif len(x) >=2 and x[:3].upper() == "VI":
        return 6
    elif x[0].upper() == "I":
        return 1
    elif x[0].upper() == "V":
        return 5
    else:
        return 0

        
#Determines whether the chord type (major,minor,etc)
def typeAnalysis(key,chord):
    isSeven = chord[-1:] == "7"
    if isSeven:
        chord = chord[:-1]
    if len(chord) >=3 and chord[0:3].upper() == "GER":
        return "ger",isSeven
    elif len(chord) >=3 and chord[0:3].upper() == "FRE":
        return "fre",isSeven
    elif len(chord) >=3 and chord[0:3].upper() == "ITA":
        return "ita",isSeven
    elif len(chord)>=3 and chord[0:3].upper() == "DIM":
        return "dim",isSeven
    elif len(chord)>=3 and chord[0:3].upper() == "AUG":
        return "aug",isSeven
    elif chord[0] == "B":
        return "maj",isSeven
    elif chord[-1:] == "+":
        return "maj",isSeven
    elif chord[-1:] == "-":
        return "min",isSeven
    else:
        if key[-5:].upper() == "MAJOR":
            idx = RomanToInt(chord) -1
            if idx == -1:
                print("Wrong input format.")
                exit(-1) 
            return key_map[major_key_Chordtype[idx]],isSeven
        else:
            idx = RomanToInt(chord) -1
            if idx == -1:
                print("Wrong input format.")
                exit(-1) 
            return key_map[minor_key_Chordtype[idx]],isSeven           
    
def startPosition(key,chord,type):
    key = key[:-5]
    start_pos = pitch_to_index[key[0]]
    print(start_pos)

a,b = typeAnalysis(key,chord)
print(a,b)