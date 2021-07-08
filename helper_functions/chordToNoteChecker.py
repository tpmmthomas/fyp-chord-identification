import os,sys
p = os.path.abspath('../modules')
sys.path.append(p)
from chordToNote import ChordToNote
#import numpy as np
import pandas as pd

major_keys = ["C","G","D","A","E","B","F","Bb","Eb","Ab","Db","Gb"]
minor_keys = ["a","e","b","f#","c#","g#","d","g","c","f","bb",'"eb']

major_chords = ["I","I7","bII","II","II7","III","III7","IV","IV7","V","V7","bVI","GerVI","FreVI","ItaVI","VI","VI7","VII","VII7","DimVII"]
minor_chords = ["I","I+","bII","II","II7","III","IV","IV+","V","V+","V+7","VI","GerVI","FreVI","ItaVI","VII","DimVII","DimVII7"]