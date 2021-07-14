# Note to Chord Module
>scoring is based on key_match > key_name_match > edit_distance
> + key_match:    key_match(D#,Eb) === *True*
> + key_name_match: key_name_match(D#,Eb) === *False*
> + edit_distance (smaller the better): 
  > > + distance((C,E,G),(C,E,A))  = 2
  > > + distance((C,E,G),(C,E,G#))  = 1
