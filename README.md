# fyp-chord-identification

## Environment setup (Recommended)

### Using Conda
At your target directory, execute the following:   
```
conda create -n fyp python=3.8 -y
conda activate fyp
git clone https://github.com/tpmmthomas/fyp-chord-identification.git
cd fyp-chord-identification
pip install -r requirements.txt
```

## Chord to Note Module
```
python modules/chordToNote.py [key] [chord]
```  
example:   
```
python modules/chordToNote.py Cmajor I
```
