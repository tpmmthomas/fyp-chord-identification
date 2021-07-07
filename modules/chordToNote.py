#0 = C, 12 = B pitch class
major_offset = [0,4,7,10] 
minor_offset = [0,3,7,10]
diminished_offset = [0,3,6,9]
augmented_offset = [0,4,8,10]
german_offset = [0,4,7,10]
french_offset = [0,4,6,10]
italian_offset = [0,4,10]
#Using chart in shared file as reference
major_key_Chordtype = [0,1,1,0,0,1,2]
minor_key_Chordtype = [1,2,0,1,1,0,0]
key_map ={0:"maj",1:"min",2:"dim"}
major_root_offset = [0,2,4,5,7,9,11]
minor_root_offset = [0,2,3,5,7,8,10]
pitch_to_index={"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
index_to_pitch_sharp={0:"C",1:"C#",2:"D",3:"D#",4:"E",5:"F",6:"F#",7:"G",8:"G#",9:"A",10:"A#",11:"B"}
index_to_pitch_flat={0:"C",1:"Db",2:"D",3:"Eb",4:"E",5:"F",6:"Gb",7:"G",8:"Ab",9:"A",10:"Bb",11:"B"}


#Input chord format: I to VII
# Possible suffix:  +, - and 7, +/- precedes 7
# Possible prefix german as "ger", french as "fre", italian as "ita", "dim","aug" , "b", +/- suffix not available
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
    elif chord[0].upper() == "B":
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
    
def startPosition(key,chord,type,isSeven):
    isMajor,isFlat = False,False
    if key[-5:].upper() == "MAJOR":
        isMajor = True
    if chord[0].upper() == "B":
        isFlat = True
        chord = chord[1:]
    key = key[:-5]
    start_pos = pitch_to_index[key[0]]
    if isSeven:
        chord = chord[:-1]
    if chord[-1:] == "+":
        chord = chord[:-1]
    if chord[-1:] == "-":
        chord = chord[:-1]
    if len(key)>=2 and key[1].upper() == "B":
        start_pos -= 1
    elif len(key) >=2 and key[1] == "#":
        start_pos += 1
    if type == "ger" or type == "fre" or type == "ita":
        start_pos -= 4
    elif type == "aug" and isMajor:
        start_pos += major_root_offset[RomanToInt(chord[3:])-1]
    elif type == "aug" and not isMajor:
        start_pos += minor_root_offset[RomanToInt(chord[3:])-1]
    elif type == "dim":
        if chord[:3].upper == "DIM":
            chord = chord[3:]
        if isMajor:
            start_pos += major_root_offset[RomanToInt(chord)-1]
        else:
            start_pos += minor_root_offset[RomanToInt(chord)-1]
        if not isMajor and RomanToInt(chord) == 7:
            start_pos += 1
    elif isMajor:
        start_pos += major_root_offset[RomanToInt(chord)-1]
    else:
        start_pos += minor_root_offset[RomanToInt(chord)-1]
    if isFlat:
        start_pos -= 1
    if start_pos < 0:
        start_pos += 12
    if start_pos >= 12:
        start_pos -= 12
    return start_pos
        
    
def main():
    key = "Cminor"
    chord = "DimVII"
    type,isSeven = typeAnalysis(key,chord)
    print(a,b)
    start = startPosition(key,chord,a,b)
    print(c)
    print(index_to_pitch_sharp[c])
    notes = []
    if type == "ger":
        for offset in german_offset:
            notes.append((start+offset)%12)
    elif type == "fre":
        for offset in french_offset:
            notes.append((start+offset)%12)
    elif type == "ita":
        for offset in italian_offset:
            notes.append((start+offset)%12)
    elif type == "maj":
        if isSeven:
            for offset in major_offset:
                notes.append((start+offset)%12)
        else:
            for i in range(3):
                notes.append((start+major_offset[i])%12)
    elif type == "min":
        if isSeven:
            for offset in minor_offset:
                notes.append((start+offset)%12)
        else:
            for i in range(3):
                notes.append((start+minor_offset[i])%12)
    #elif type == "dim":




if __name__ == "__main__":
    main()