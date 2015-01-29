# Lab 2: Hashing, Signing, and Encrypting

The purpose of this lab is to gain experience using public-key (asymmetric) cryptography tools.

# Reading

- [GnuPG](https://www.gnupg.org/index.html)
- [GnuPG Mini Howto](http://www.dewinter.com/gnupg_howto/english/GPGMiniHowto.html)

# Lab Requirements

## GPG

- Install GPG
- Create a public/private key pair.
- Publish your public key on ```hkp://pgp.mit.edu```
- Use the key server to find the public key of one or more class members.
	- Validate the keyID.
	- What is their key's fingerprint
- Exchange and validate signed messages with another class member. 
- Send a secret message to another class member. Don't tell them what it says in plaintext.
- Sign someone's public key (i.e. participate in a keysigning)

## Keybase.io

You should have received an invitation from Dr. Windley to sign up for Keybase.io.

- Sign up and create an account
- Download and install keybase.io
- Push the public key you created in the GPG portion of this lab to Keybase
- Add one of more identity proofs (for a Website you control, a Twitter account you own, etc.)
- Track Dr. Windley and the TA
- Track at least three other people you know
- Exchange an encrypted message with at least one other person in the class (not the TA or the Dr. Windley)

## Deliverables

Send the following to the TA:

0. Statement that you've completed all the preceding steps.
1. Your public key, key ID, and key fingerprint. *Do NOT send your private key!*
2. The name of the class member you sent a secret message with and the content of the message.
3. The name of the class member you got a secret message from and the content of their message.
4. Your Keybase.io identifier.
5. Answer the following questions:
	0. What is a key signing party?
	1. What is a personal digital certificate?
	2.  What is the purpose of Keybase.io (i.e. what problem is it solving)?
	3. How does Keybase.io accomplish social proof (i.e. knowing you've got the right public key)?
	4. What are the advantages and disadvantages of the Keybase approach compared with PGP and Certificates?


