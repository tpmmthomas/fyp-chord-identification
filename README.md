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
```
cd modules
python chordToNote.py [key] [chord]
```  
example:   
```
python modules/chordToNote.py Cmajor I
```

### Note to Chord Module
#### Require to load the Dictionary(Hash Table) First
- key_chord_name_mapping.pickle
```
#function call
#threshold ~= number of note satisify the chord
keys2chords(keys,threshold)
```  
example:   
```
keys2chords(['c','e','g'],3)
```
