## Very necessary script used to create the main challenge file, hello.py

challenge = """flag = "GooseCTF{real_actual_flag}"

print("Hello World!")

print(flag)"""

with open("hello.py", "w") as challenge-file:
    challenge-file.write(challenge)
