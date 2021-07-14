# Explanations  
Here we document all explanations of how our code works, which would be useful in our future report.

## Chord To Note Module
Our program is divided into several Submodules: `typeAnalysis, startPosition, noteNaming`.  
   
First, the `typeAnalysis` submodule analyzes the chord type (Major, Minor, Diminished, Augmented, Italian, German, French).    
For inputs which states explicitly the chord type (e.g. DimVII), the program would match the chord type immediately. Otherwise, if only roman numeral is given, the chord type is matched with the Key + Chord combination by a pre-defined list (`major_key_Chordtype` or `minor_key_Chordtype`).      
  
Second, the `startPosition` submodule determines the root note of the chord. The program would first determine the tonic position of the key. From there, it adds or subtracts certain offset accorrding to the Roman numeral of the chord and the `major_root_offset` or `minor_root_offset` lists. It returns an index corresponding to a certain pitch class (0 = C, 11 = B).  

Finally, with the correct chord type and starting position, the program will generate a list of notes (in their corresponding pitch classes) which are included in the chord, then the list will be passed to the `noteNaming` module. This module will determine the correct naming of the notes given several enharmonic equivalents. It works by first assigning the pitch classes to either all sharp notes or all flat notes according to the given key, then changing some of the notes by analyzing its scale degrees. For example, the diminished seventh chord has scale degree of 7,2,4,b6. Hence we would change the final note (b6) to be the flat version of the originial note naming (e.g. G# to Ab, G to Abb).  

## Note To Chord Module
#### loop through all possible chords and sort them by the scoring funcion, finally output the first {NUMOUT} chords
+ noteToChordFast: Create a Dictionary(key-value pair) with all possible key_idx combination as *KEY* and all possible chords corrsponding to each key_idx combination as *VALUE*. Then select the corrsponding key_mapping upon input and loop through them with the scoring function
+ noteToChord : Create a list to store {chord,key,keyname,keyIdx}, then loop through it with the scoring function
-  > variation1: load the Dictionary in noteToChordFast, and extract all possible chords for all input_keys combinations with at least 2 matched key for each chord. Then loop through them with the scoring function

*****

>scoring is based on key_match > key_name_match > edit_distance
> + key_match:    key_match(D#,Eb) === *True*
> + key_name_match: key_name_match(D#,Eb) === *False*
> + edit_distance (smaller the better): __for noteToChord only__
  > > + distance((C,E,G),(C,E,A))  = 2
  > > + distance((C,E,G),(C,E,G#))  = 1
