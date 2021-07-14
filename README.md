# fyp-chord-identification

### Environment setup (Recommended)

#### Using Conda
At your target directory, execute the following:   
```
conda create -n fyp python=3.8 -y
conda activate fyp
git clone https://github.com/tpmmthomas/fyp-chord-identification.git
cd fyp-chord-identification
pip install -r requirements.txt
```

### Chord to Note Module
In `modules` directory:  
```
python chordToNote.py [key] [chord]
```  
Example:   
```
python chordToNote.py Cmajor I
```

### Note to Chord Module
In `modules` directory:  
```
python noteToChord.py [notes ...] [-o NUMOUT] [-k KEY] [--exactMatch]
```  
Enter 3 to 4 notes, optionally specify "-o" argument to control number of output matches, "-k" argument to force match only the given key, "--exactMatch" to only output chords that match completely with provided notes.  
Example:   
```
python noteToChord.py C E G -o 5 -k Cmajor
```
>scoring is based on key_match > key_name_match > edit_distance
> + key_match:    key_match(D#,Eb) === *True*
> + key_name_match: key_name_match(D#,Eb) === *False*
> + edit_distance: 
> > distance((C,E,G),(C,E,A))  =20
> > distance((C,E,G),(C,E,G#))  =30

#### If only exact match is needed, use `noteToChordFast.py` instead:  
```
python noteToChordFast.py [notes ...] [-o NUMOUT] [-k KEY]
```

