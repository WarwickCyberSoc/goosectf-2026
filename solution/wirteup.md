# How 2 learn writeup

I made this challenge cause I was bad at steg and wanted to get better at audio forensics, so come with me as I do both.

## Step 1 - What are we dealing with?

We have two files, 0119.wav and OptimalLearning.mp4. Running the "file" command on both is a really good place to start, this enables us to identify anything strange or unusual with the files from the off. From this we get:


![alt text](img101.png)

So we have a basic ISO media file, but the audio file denotes it is "little endian" wave file right from the off. Pay close attention to "16 bit" as that is also important as it tells us how many bits are in an audio sample. More on why we need this later.

This isn't actually *that* interesting really as all wave files return their encoding status but at least we have identified the file as an uncompressed wave file. This is a file type you can hide data in.

A quick check with strings reveals.... nothing! so what now?


## Step 2 - A bit of inference and deduction
I will admit a bit of inference is required here. There is something hidden in one of these files. But hiding in the files you can inspect them with other reconeissance tools, whilst strings and file didn't reveal anything there are other tools (the exiftool) that could reveal meatdata information within the file, running the video through exiftool we get:

![alt text](dunga.png)

It is well hidden, but a video file does not have the parameter "filekey" and what is a DungaDungaDunga anyway? Hopefully that jumped out at you and it's label of filekey within the metadata seems to regard it to some kind of key but we haven't found anything to unlock so hold onto that for a second.

## Step 3 - Think powerful thoughts
Ok so with the little hints here and there you know about the encoding of the files, the lack of any plaintext strings hiding in either file and a key --> something is encrypted here. 
So we've found an encryption key so inspecting the audio file is the next step of things, as that's likely where the thing we need to decrypt may such lie.
Going for this looking at online resources about hiding information in audio files is great (https://medium.com/analytics-vidhya/get-secret-message-from-audio-file-8769421205c3) is a good example resource. Unless you are cracked beyond measure **you probably won't innately know this**, so researching things you do not understand is a great place to learn concepts and then apply them when solving any ctf challenges.

Dumping the file into hexdump or HxD in my case reveals something else too, if you followed the article.

![alt text](implication.png)

It shows the file header of the file but the anomaly here is the sparse 0s and then 1s that appear at the top of the data without altering the hex content of the file, this is unusual in audio data. These 0 and 1s indicate some data is hidden by being encoded in some way within the file.

So we've got to extract these bits and decode the message, and then decrypt it (as there's a key remeber.)


## Step 4 - The big long explanation.

So to do this we have to do some **coding**. (see my solution in solvescript.py!)
The wave module in Python allows us to mess around with audio files, it's the bread and butter for trying to extract this information out of the audio file (https://docs.python.org/3/library/wave.html) -- documentation is always good.

**frame_bytes = wave.readframes(wave.getnframes())**
Once we open the wave file we need to extract the "frames" of the audio - these are the little chunks of audio that combine together to make the full length of a wavefile. We read this as bytes, as it's a byte level encoding we deal with we wanna be able to mess with them. Frame_bytes is a sequence of bytes now totalling the complete audio file.


**sample = np.frombuffer(frame_bytes, dtype=np.int16)**
We use numpy module to extract these frame bytes and place them into an NumPy array that we can iterate over (cause we need to do some mass operations to them.), the dtype=np.int16 here is determined by what we saw in the 'file' command i mentioned earlier.wav files tend to store audio as 16-bit PCM integers, so now we collect values.


**bits = [str(s & 1) for s in sample]**

Bitwise AND between address value and 1 11001010 & 1 → 0, this will extract the LSB (the last bit in a string) from each, 

This LSB value is stored as a string so we can concatinate it together later. We now have a set of 0's and 1's strings of the LSBs of each audio sample. So lets start bringing them together

LSB is the LEAST signficiant bit, it gets hidden here as the difference in audio quality in every frame/sample is minimal and not audible, this makes it optimal to hide information.

Currently stored as a list like: ['0', '1', '0'] etc where each value is the LSB of an address collected


**for i in range(0, len(bits), 8):**
    **byte = int("".join(bits[i:i+8]), 2)**
    **cipher.append(byte)**

So now we iterate over the LSB 'bits' that we have collected. In this case for their total length iterating x8. Why x8? 8 bits in a byte so combining them together in sets of 8 allows us to reform the original hidden bytes that were originally stored in the sound file before being obfuscated (and thus stiching back together the hidden message), as text is stored in byte by byte representiation not bit by bit.

**byte = int("".join(bits[i:i+8]), 2)**
**cipher.append(byte)**

Then we made it into a binary string through the "".join()then to a decimal integer so it interprets our value as a byte value. Then we add it to the bytearray "cipher" to have all combined lsb bytes in one location to translate it.

**flag = de_xor(cipher, key)**

**def de_xor(flag, key):**
    **return bytes(**
        **flag[i] ^ key[i % len(key)]**
        **for i in range(len(flag)))**

With the supplied key in bytes format (because encryption is at bytes level). This is XOR encryption, xoring each byte of the supplied flag in this case our big long bytearray we appended the combined LSB bits too with the corresponding byte in the key value.

Then with some smart printing you output the flag! yipee wow your sooo smart.
**print(flag.decode)**
 GooseCtf{UR_BRA1N_I5_R0TTED}












