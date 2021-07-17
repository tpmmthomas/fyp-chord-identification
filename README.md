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
Enter 3 to 4 notes, optionally specify "-o" argument to control number of output matches, "-k" argument to force match only the given key, "-t" to decide the minimum required matching notes.

Example:   
```
python noteToChord.py C E G -o 3 -k Cmajor   #output:  CMajorI  CMajorI7  CMajorVI7
```

```
python noteToChord.py C E D -o 3 -k Cmajor   #output:  CMajorI  CMajorVI  CMajorVI7
```

#### If only exact match is needed, use `noteToChordFast.py` for faster performance:  
```
python noteToChordFast.py [notes ...] [-o NUMOUT] [-k KEY]
```
Example:
```
python noteToChordFast.py C E G -o 3 -k Cmajor   #output:  CMajorI  CMajorI7  CMajorVI7
```

```
python noteToChordFast.py C E D -o 3 -k Cmajor   #output:  EMPTY
```
