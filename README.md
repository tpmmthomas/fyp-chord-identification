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
python noteToChord.py [notes ...] [-o NUMOUT] [-k KEY]
```  
Enter 3 to 4 notes, optionally specify "-o" argument to control number of output matches, and "-k" argument to force match only the given key.  
Example:   
```
python noteToChord.py C E G -o 5 -k Cmajor
```
