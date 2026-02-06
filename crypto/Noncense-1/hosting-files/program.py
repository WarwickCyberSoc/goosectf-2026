from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag

key_file = open("key.txt", "r")
key_hex = key_file.read()
key_file.close()
KEY = bytes.fromhex(key_hex)

nonce_file = open("nonce.txt", "r")
nonce_hex = nonce_file.read()
nonce_file.close()
NONCE = bytes.fromhex(nonce_hex)

def encrypt_aes_gcm(plaintext: str):
    cipher = Cipher(algorithms.AES(KEY), modes.GCM(NONCE), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return ciphertext, encryptor.tag

def decrypt_and_verify(ciphertext, tag):
    ciphertext = bytes.fromhex(ciphertext)
    tag = bytes.fromhex(tag)
    cipher = Cipher(algorithms.AES(KEY), modes.GCM(NONCE, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

def chal1():
    
    print("\n========== Challenge 1 ==========\n")
    
    # get the flag to encrypt
    flag_file = open("flag1.txt", "r")
    whole_flag = (flag_file.read()).strip()
    flag_file.close()
    strings_to_encrypt = []
    for i in range(0, len(whole_flag), 9):
        chunk = whole_flag[i:i + 9]
        strings_to_encrypt.append(chunk)
    
    ciphertexts = []
    for plaintext in strings_to_encrypt:
        ciphertext, tag = encrypt_aes_gcm(plaintext)
        ciphertexts.append((ciphertext, tag))
    
    print("Encrypted Strings:")
    for (ciphertext, tag) in ciphertexts:
        print(f"\nCiphertext: {ciphertext.hex()}")
        print(f"Authentication Tag: {tag.hex()}")
        
def chal2():
    
    print("\n========== Challenge 2 ==========\n")
    
    # get the flag to encrypt
    flag_file = open("flag2.txt", "r")
    flag = (flag_file.read()).strip()
    flag_file.close()
    
    ciphertext = str(input('Enter your ciphertext for the phrase "password1" (as hex): '))
    tag = str(input("Enter your authentication tag (as hex): "))
    
    try:
        plaintext = decrypt_and_verify(ciphertext, tag)

        if plaintext == "password1":
            print(f"Here's your flag: {flag}")
        else:
            print(f"Authenticated succeeded, but plaintext is wrong: {plaintext}")

    except InvalidTag:
        print("Authentication failed (invalid tag)")
    except:
        print("Congrats, you've managed to trigger an error I can't be bothered to specifically handle")
        print("(That probably means you didnt enter the plaintext/tag as hex or that the tag was the wrong length)")

        
def main():
    while True:
        print("\n========== Challenge Menu ==========")
        print("1) Challenge 1")
        print("2) Challenge 2")
        print()
        
        choice = input("Select a challenge (1 or 2): ").strip()
        if choice == "1":
            chal1()
        elif choice == "2":
            chal2()
        else:
            print("You had one job...")

if __name__ == "__main__":
    main()
