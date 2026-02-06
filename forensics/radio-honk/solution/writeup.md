# Radio Honk
## Step 1
Firstly the wav file must be recognised as AX.25 frames. 

## Step 2
To decode AX.25 frames either `atest honk.wav` or `multimon-ng -a AFSK1200 -t wav honk.wav` can be used.

This will show a packet containing the flag.