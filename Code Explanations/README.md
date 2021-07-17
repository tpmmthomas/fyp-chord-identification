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
+ `noteToChordFast`: First we created a Dictionary (stored as pickle files) that maps every possible pitch class combination (*KEY*) to all possible chords corrsponding to the combination (*VALUE*), as well as a dictionary (stored as JSON) that maps each chord to its corresponding note names and pitch classes. Once users input a set of notes, it will be converted into their corresponding pitch class. Then a list of possible chords will be obtained using the first  dictionary. We then loop through those possible chords, retrieve their pitch classes and note names with the second dictionary, rank it according to the scoring function, and filtering specific keys if necessary. Finally it will return the first {NUMOUT} highest-scored chords as a list. 
+ `noteToChord` : . Once users input a set of notes, we will consider all possible combinations of pitch classes which has at least 2 pitches match with the input notes. Using the dictionaries as defined above , it will then loop through all the possibilities while rating each chord with the scoring function, and output the first {NUMOUT} highest-scored chords as a list. This allows searching for similar but not exacct chords. 

****** 
Scoring is based on pitch class match > pitch naming match > edit distance. 
 + pitch_class_match:    pitch_class_match(D#,Eb) === *True*
 + pitch_naming_match: pitch_naming_match(D#,Eb) === *False*
 + edit_distance (smaller the better): __for noteToChord only__
   +  distance((C,E,G),(C,E,A))  = 2
   +  distance((C,E,G),(C,E,G#))  = 1

>__Update (17/7/2021)__ : The root note of each chord is now part of the consideration. For any chords whose root note appear in the input notes are more likely to be the true prediction.
> > 50 extra marks were given to the chords whose root note is in the input notes.
******
While `noteToChordFast` provides a faster performance as it uses a dictionary to significantly reduce the number of chords to be considered, it only allows an exact match between the chord and the given keys. `noteToChord` is slower but allows searching for similar chords (e.g. chords that differ by one note).
> __Update 17/7/2021 'noteToChord'__ : To strike a balance between efficency and accurancy, we roll back to the dictionary approach while allowing an extended combination of given note. Duplicated chords are filtered by set(). The overall time cost was improved by ~5-15x compared to the old version. Threshold =2 is recommended to filter out unreliable predictions.
