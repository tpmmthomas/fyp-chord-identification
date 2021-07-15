# Explanations  
Here we document all explanations of how our code works, which would be useful in our future report.

## Chord To Note Module
Our program is divided into several Submodules: `typeAnalysis, startPosition, noteNaming`.  
   
First, the `typeAnalysis` submodule analyzes the chord type (Major, Minor, Diminished, Augmented, Italian, German, French).    
For inputs which states explicitly the chord type (e.g. DimVII), the program would match the chord type immediately. Otherwise, if only roman numeral is given, the chord type is matched with the Key + Chord combination by a pre-defined list (`major_key_Chordtype` or `minor_key_Chordtype`).      
  
Second, the `startPosition` submodule determines the root note of the chord. The program would first determine the tonic position of the key. From there, it adds or subtracts certain offset accorrding to the Roman numeral of the chord and the `major_root_offset` or `minor_root_offset` lists. It returns an index corresponding to a certain pitch class (0 = C, 11 = B).  

Finally, with the correct chord type and starting position, the program will generate a list of notes (in their corresponding pitch classes) which are included in the chord, then the list will be passed to the `noteNaming` module. This module will determine the correct naming of the notes given several enharmonic equivalents. It works by first assigning the pitch classes to either all sharp notes or all flat notes according to the given key, then changing some of the notes by analyzing its scale degrees. For example, the diminished seventh chord has scale degree of 7,2,4,b6. Hence we would change the final note (b6) to be the flat version of the originial note naming (e.g. G# to Ab, G to Abb).  

## Note To Chord Module
We have two approaches when implementing this module: 
+ `noteToChordFast`: First we created a Dictionary (stored as JSON files) that maps every possible pitch class combination (*KEY*) to all possible chords corrsponding to the combination (*VALUE*). Once users input a set of notes, it will be converted into their corresponding pitch class. Then a list of possible chords will be obtained using the dictionary. We then loop through those possible chords, rank it according to the scoring function, filtering specific keys if necessary. Finally it will return the first {NUMOUT} highest-scored chords as a list. 
+ `noteToChord` : First we created a list to store ALL possible {chord,key,keyname,keyIdx} combinations (stored as JSON). Once users input a set of notes, it will then loop through all the chords within the file while rating each chord with the scoring function, and output the first {NUMOUT} highest-scored chords as a list. 
> a variation for `noteToChord` module : load the Dictionary in `noteToChordFast`, and extract all possible chords for all input_keys combinations with at least 2 matched key for each chord. Then loop through them with the scoring function.

****** 
Scoring is based on pitch class match > pitch naming match > edit distance. 
> + pitch_class_match:    pitch_class_match(D#,Eb) === *True*
> + pitch_naming_match: pitch_naming_match(D#,Eb) === *False*
> + edit_distance (smaller the better): __for noteToChord only__
  > > + distance((C,E,G),(C,E,A))  = 2
  > > + distance((C,E,G),(C,E,G#))  = 1
******
While `noteToChordFast` provides a faster performance as it uses a dictionary to significantly reduce the number of chords to be considered, it only allows an exact match between the chord and the given keys. `noteToChord` is slower but allows searching for similar chords (e.g. chords that differ by one note).
