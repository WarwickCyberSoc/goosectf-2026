# Run my NUT

There are more than a couple ways of solving this challenge. Some easier, some harder:

- Using an online interpreter to run the script
- Downloading the interpreter and running it locally
- Turning the code into valid Javascript (or any other language) and running it
- Manually de-obfuscating
- Use an LLM (LAME but easy)

I am going to discuss the first one.

## Step 1: What is a .nut?

The [first result](https://fileinfo.com/extension/nut) says that:

> A NUT file is a text file that contains Squirrel code written in the Squirrel programming language.

So we know that we are looking at an obfuscated script of a certain language.

## Step 2: Online Interpreter

Searching for 'Squirrel interpreter online' sends you to [tio.run](https://tio.run/#squirrel) which is an online compiler/interpreter for more than 681 languages, one of which is Squirrel. So, we can simply copy/paste the code into the website and get the flag in the output window: `GooseCTF{r8_my_nu7}`.