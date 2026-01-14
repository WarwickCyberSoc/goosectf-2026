# Noncense Writeup

These challenges are both possible since the same nonce us used for all encryption/decryption. 


## Challenge 1

With AES-GCM, the formula for the ciphertext is as follows:

```
C = P ⊕ KS
```

Where C is the ciphertext, P is the plaintext, KS is the keystream and ⊕ denotes XOR.

The formula for the keystream is as follows:

```
Eₖ(counterᵢ)
```

Where Eₖ is AES encryption on one block, using the key ₖ and the formula for the counter is:

```
inc₃₂(J0)
```

Where inc₃₂ just increments the counter by 1 and this only affects the last 4 bytes and the formula J0 holds the nonce concatonated with the block number for the block that is being encrypted.

In other words, if the nonce was `aabbccddeeff001122334455` the value of inc₃₂(J0) would be `aabbccddeeff00112233445500000001`. This would then be encrypted using the key. This is then the keystream. For the second block, the value of inc₃₂(J0) would then be `aabbccddeeff00112233445500000002`. As the nonce is reused, J0 is constant and therefore the keystream is the same for every ciphertext.

In this challenge, all three ciphertexts are each 9 bytes (less than a block) and each uses the same cipher with the same nonce. This means that the value of keystream will be the same for each block.

We can work out the value of the keystream used for all three blocks therefore, if we know one of the plaintexts and the corresponding ciphertext. As we are decrypting the flag, we know the first 9 characters (the first ciphertext) must decrypt to `GooseCTF{`. To solve for the keystream, the formula used earlier:

```
C = P ⊕ KS
```

Can be rearranged to:

```
C ⊕ P = KS
```

If you XOR `GooseCTF{` with the first ciphertext (`5e773dcb6983545de0`), you get the first 9 bytes of the keystream (`191852b80cc0001b9b`).

This keystream can then be used to recover the other plaintexts using the rearranged version of the previous formula:

```
C ⊕ KS = P
```

XORing the second ciphertext (`297631dd538d655af5`) with the keystream results in the plaintext: `0nce_MeAn`.

XORing the third ciphertext (`6a473df66fa53f24e6`) with the keystream results in the plaintext `s_oNce??}`.

The whole flag is therefore `GooseCTF{0nce_MeAns_oNce??}`.

A [solve1.py](./solve1.py) is a solve script for this challenge.

## Challenge 2

The ciphertext can be obtained using the formula from challenge 1:

```
C = P ⊕ KS
```

In other words, to get the ciphertext, you can XOR the plaintext (`password1`) with the keystream recovered in challenge 1 (`191852b80cc0001b9b`) to get the ciphertext value `697921cb7baf727faa`.
(This is only possible if the plaintext to encode is not longer than the number of known keystream bytes.)

The tag can then be forged but it requires a lot more maths so if you can't be bothered to read the rest of this, [solve2.py](./solve2.py) is a solve script for the challenge.

It also worth noting that this maths can drop some steps since all the plaintexts are the same length (9 characters). I think this challenge would still be possible if they weren't but I have not tried.

Here's a list of terms used in the maths below:

- ⊕ - XOR
- || - concatenation
- C - ciphertext (where C₁ denotes the ciphertext for the first plaintext)
- P - plaintext (where P₁ denotes the first plaintext)
- T - authentication tag (where T₁ denotes the tag for the first ciphertext)
- Eₖ() - AES encryption on one block, using the key ₖ
- J0 - nonce || current block number
- len() - the length of a value in bits
- H - Eₖ(0¹²⁸) (the encrypted version of 128 zeros)
- A - data that is not to be encrypted, only authenticated (with the auth tag)
- L - len(A) || len(c)
- ()⁻¹ - denotes the inverse of a term

The formula for an authentication tag is as follows:

```
T = GHASH(H,A,C) ⊕ Eₖ(J0)
```

However, we know Eₖ(J0) is a constant for all the tags we already have and the one we will generate since J0 depends on the nonce and the block number. The nonce used is the same throughout and we are only ever dealing with 1 block. H is also a constant since it depends on the key, which is also the same throughout. In addition, as there is no data to be authenticated but not encrypted, A is none. This means the formula can be simplified to:

```
T = GHASH(H,C) ⊕ Eₖ(J0)
```

The GHASH function is more complex in definition when dealing with multiple blocks but for just one block it has the following formula:

```
GHASH(H,C) = ((H•C)⊕L)•H
```

• denotes multiplication but where each term is interpreted as a polynomial first. This polynomial is in the form `y = x¹²⁸ ⊕ x¹²⁷ ⊕ ... ⊕ x¹ ⊕ x⁰`. The binary value at the corresponding bit determines if a term is present in the polynomial or not. For example `0101` would become `x² ⊕ x⁰`.
The polynomials for the 2 terms are then multiplied. A reduction is then carried out to remove any terms with an order greater than 128. This term is then converted back from a polynomial to an actual value doing the reverse of before i.e. `x² ⊕ x⁰` would become `0101`.

Using the equation for the authentication tag, we know that:

```
T₁ = GHASH(H,C₁) ⊕ Eₖ(J0)
T₂ = GHASH(H,C₂) ⊕ Eₖ(J0)
```

We can rearrange these to the following:

```
T₁ ⊕ GHASH(H,C₁) = Eₖ(J0)
T₂ ⊕ GHASH(H,C₂) = Eₖ(J0)
```

Since the nonce was reused, J0 and therefore Eₖ(J0) are constant. This means the 2 equations can be combined to eliminate Eₖ(J0):

```
T₁ ⊕ GHASH(H,C₁) = T₂ ⊕ GHASH(H,C₂)
```

This can be rearranged to give:

```
T₁ ⊕ T₂ = GHASH(H,C₁) ⊕ GHASH(H,C₂)
```

We can then substitute in the GHASH formula for one block to give:

```
T₁ ⊕ T₂ = (((H•C₁)⊕L)•H) ⊕ (((H•C₂)⊕L)•H)
```

This expands to:

```
T₁ ⊕ T₂ = (H²•C₁) ⊕ (L•H) ⊕ (H²•C₂) ⊕ (L•H)
```

H is a constant since the same key is used throughout and L is a constant since the ciphertexts in this challenge have the same length. This means (L•H) is constant. As it is XORed twice, it cancels itself out and can be dropped from the equation to give the following:

```
T₁ ⊕ T₂ = (H²•C₁) ⊕ (H²•C₂)
```

Which can be factorised into:

```
T₁ ⊕ T₂ = H²•(C₁⊕C₂)
```

We can rearrange this to solve for H²:

```
(T₁⊕T₂)•(C₁⊕C₂)⁻¹ = H²
```

Therefore, if we have 2 known authentication tags and the corresponding ciphertext, we can solve for H². Luckily, from challenge 1, we have 3 pairs of ciphertexts and authentication tags which can be substituted into the equation to get a value for H².

We can then use a variation of an earlier formula where x is used to indicate the tag and ciphertext for the phrase `password1`:

```
T₁ ⊕ Tₓ = H²•(C₁⊕Cₓ)
```

We can rearrange this formula to get:

```
Tₓ = (H²•(C₁⊕Cₓ)) ⊕ T₁
```

We can then substitute in the following values to get Tₓ:

- H² - the value we solved for previously
- C₁ - the value of a ciphertext provided in challenge 1
- Cₓ - the previously calcualted ciphertext for `password1` (`697921cb7baf727faa`)
- T₁ - the corresponding authentication tag for the ciphertext provided in challenge 1

This gives a final Tₓ value of `b1f20252c31de9ed99b9b15c2bd9c65e`. Providing the values of Cₓ and Tₓ to the instance running the challenge results in the following flag being printed: `GooseCTF{dont_reuse_nonces_in_your_ISS_coursework}`.

As previously mentioned, there is a solve script in [solve2.py](./solve2.py) which implements these mathematical calculations to encrypt the plaintext and forge the tag as required.