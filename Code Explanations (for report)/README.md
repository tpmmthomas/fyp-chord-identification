# Explanations  
Here we document all explanations of how our code works, which would be useful in our future report.

## Chord To Note Module
Our program is divided into several Submodules: `typeAnalysis, startPosition, noteNaming`.   
First, the `typeAnalysis` submodule analyzes the chord type (Major, Minor, Diminished, Augmented, Italian, German, French).    
For inputs which states explicitly the chord type (e.g. DimVII), the program would match the chord type immediately. Otherwise, if only roman numeral is given, the chord type is matched with the Key + Chord combination by a pre-defined list (`major_key_Chordtype` or `minor_key_Chordtype`).    


