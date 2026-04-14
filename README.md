# File Encryptor (Python + Tkinter)

A simple desktop app that encrypts and decrypts files using symmetric encryption. Built in Python with a small Tkinter GUI — pick a file, click a button, get an encrypted copy.

Built as a self-study project to learn how symmetric encryption actually works in code, and how the `cryptography` library handles the parts that are easy to get wrong.

> ⚠️ **Learning project — not for sensitive data.** This is intentionally simple so I could focus on understanding the crypto primitives. See [Known limitations](#known-limitations) for an honest list of why you shouldn't use it to protect anything that actually matters.

## Features

- **Generate a key** — creates a fresh 256-bit Fernet key and saves it to disk
- **Encrypt a file** — pick any file with the file picker, get an encrypted copy with `.encrypted` appended
- **Decrypt a file** — pick an encrypted file, get the original back
- **Friendly errors** — pop-ups instead of cryptic stack traces if something goes wrong (key missing, wrong key, corrupted file, etc.)

## Tech

- **Python 3**
- **[cryptography](https://cryptography.io/)** — uses [Fernet](https://cryptography.io/en/latest/fernet/), which is AES-128 in CBC mode with HMAC-SHA256 for authentication, all wrapped up so you can't accidentally use it wrong
- **Tkinter** — Python's built-in GUI library, no extra install needed

## Running it

1. Clone the repo:
   ```bash
   git clone https://github.com/Bapirlo07/file-encryptor.git
   cd file-encryptor
   ```
2. Install the one dependency:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python file_encryptor.py
   ```
4. In the app:
   - Click **Generate Key** first (only needed once — it creates `encryption_key.key`)
   - Click **Encrypt File** and pick something to encrypt
   - Click **Decrypt File** and pick the `.encrypted` file to get the original back

The key file lives next to the script. **Keep it safe** — if you lose it, the encrypted files are gone forever. If someone else gets it, they can decrypt your files.

## How it works

Symmetric encryption means the *same key* is used to encrypt and decrypt. Fernet handles the trickier parts under the hood:

1. When you encrypt, Fernet generates a fresh random initialisation vector (IV) for the AES-CBC cipher
2. It encrypts your file's bytes with the key + IV
3. It signs the result with HMAC-SHA256 so any tampering is detected on decryption
4. It packages the IV, ciphertext and signature together in one base64-encoded blob

When you decrypt, it does all of that in reverse and verifies the signature first — if anyone has changed even one byte of the encrypted file, decryption fails loudly instead of silently giving you garbage.

## Known limitations

These are real and I'm aware of them. They're on the roadmap.

- **The key file lives next to the encrypted files.** If an attacker can read one, they can probably read the other — so in practice this app is mostly defending against someone who casually opens the encrypted file in a text editor. The proper fix is to derive the key from a password the user types in (using PBKDF2 or scrypt) and never store the key on disk at all.
- **No password protection.** Anyone who can run the app and click "Decrypt File" with the key file present can decrypt anything.
- **Whole file is loaded into memory.** Fine for documents and photos, will struggle with multi-gigabyte files. A streaming approach would fix this.
- **Decryption assumes the original extension can be reconstructed by stripping `.encrypted`.** If the file gets renamed in between, you have to put the name back manually.
- **No salt, no key rotation, no secure key wiping.** All things real-world tools handle.

## Roadmap

- [ ] Replace the static key file with a **password-derived key** using PBKDF2
- [ ] Add a "verify password" step so the user knows immediately if they typed it wrong
- [ ] Stream files in chunks instead of loading the whole thing
- [ ] Drag-and-drop support in the GUI
- [ ] Pack the original filename into the encrypted blob so renaming doesn't break decryption
- [ ] Build a CLI version for use in scripts

## What I learned

- How symmetric encryption differs from hashing and from public-key encryption
- Why "roll your own crypto" is a bad idea — even something as small as how you generate an IV is a footgun, and libraries like `cryptography` exist precisely to stop you from making those mistakes
- That **key management is the hard problem in cryptography**, not the encryption itself. Encrypting bytes is easy; deciding where the key lives and who can see it is where almost every real-world breach happens.
- How to wire up Tkinter buttons to functions and use file dialogs

---

Built by [Albaraa Boukna](https://github.com/Bapirlo07) — first-year Computer Science, Brunel University London. Interested in security, which is what got me building this in the first place.
