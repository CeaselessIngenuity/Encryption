"""
cipher.py - the ONLY file you need to change to plug in your own encryption.

Core principle: every cipher class has encrypt(text) -> text and decrypt(text) -> text.
The chat code never looks inside; it just calls these two methods.
"""
import base64

SHARED_KEY = 3  # placeholder key, both clients must use the same one for now


class Cipher:
    """Base class. Your classes should extend this."""
    # NOTE: This is an abstract class; NotImplementedError if for overriding with subclass,
    # hence this class is simply a template, and defines which functions must be there in a cipher class.
    

    def encrypt(self, plaintext: str) -> str:
        raise NotImplementedError

    def decrypt(self, ciphertext: str) -> str:
        raise NotImplementedError


class CaesarCipher(Cipher):
    """Placeholder; Replace with cipher later"""

    def __init__(self, shift: int):
        self.shift = shift

    def _shift_text(self, text: str, shift: int) -> str:
        result = []
        for ch in text:
            if ch.isalpha() and ch.isascii():
                base = ord("A") if ch.isupper() else ord("a")
                result.append(chr((ord(ch) - base + shift) % 26 + base))
            else:
                result.append(ch)
        return "".join(result)

    def encrypt(self, plaintext: str) -> str:
        return self._shift_text(plaintext, self.shift)

    def decrypt(self, ciphertext: str) -> str:
        return self._shift_text(ciphertext, -self.shift)


def make_cipher() -> Cipher:
    """The single plug-in point. Swap this line when your cipher is ready;
    Ex:  return MyCipher(public_key, private_key)
    """
    return CaesarCipher(SHARED_KEY)


# --- Wire helpers ---
# Messages travel as one line each. Base64(converts all the basic charactres into unicode and back) guarantees the ciphertext has no
# newlines or odd characters, whatever your algorithm outputs.

def to_wire(cipher: Cipher, plaintext: str) -> str:
    return base64.b64encode(cipher.encrypt(plaintext).encode("utf-8")).decode("ascii")


def from_wire(cipher: Cipher, line: str) -> str:
    return cipher.decrypt(base64.b64decode(line).decode("utf-8"))
