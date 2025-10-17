# String Tool Module

**Source:** `jsktoolbox/stringtool/crypto.py`

**High-Level Introduction:**
SimpleCrypto collects lightweight helpers that let you experiment with Caesar-style shifts, ROT13, and Base64 routines on plain strings. The module targets user-entered keyboard data, extending built-in alphabets so European characters and other common scripts survive round-trips through the encoders.

## Getting Started

Import the utility class and pick the helper that matches your use case. The package-level `jsktoolbox.stringtool` exposes lazy exports, so the heavy `crypto` module is only loaded when `SimpleCrypto` is touched. Salts influence Caesar rotations, while `multiple_encrypt` chains all available codecs into a single call.

```python
from jsktoolbox.stringtool import SimpleCrypto
```

---

## `SimpleCrypto` Class

**Class Introduction:**
Exposes stateless class methods for generating salts, translating characters, and running the supported encoders. Each helper enforces type checks and raises domain-specific errors via `raisetool.Raise`.

### `SimpleCrypto.chars_table_generator()`

**Detailed Description:**
Produces the ordered character table that Caesar operations rely on. The table merges ASCII printables with selected Unicode ranges (Latin Extended, Greek, Cyrillic, Armenian, Hebrew, Arabic) and preserves insertion order while removing duplicates. Callers rarely need it directly, yet exposing the table helps with custom analyses or diagnostics.

**Signature:**

```python
@staticmethod
def chars_table_generator() -> str
```

- **Returns:**
  - `str` - Deduplicated string containing all supported characters.

**Usage Example:**

```python
table = SimpleCrypto.chars_table_generator()
print(len(table))  # Inspect supported alphabet size
```

---

### `SimpleCrypto.salt_generator()`

**Detailed Description:**
Builds numeric salts of a fixed digit length using `secrets.randbelow`, which offers stronger randomness than the standard `random` module. Invalid lengths trigger a ValueError through the Raise helper.

**Signature:**

```python
@classmethod
def salt_generator(cls, length: int = 8) -> int
```

- **Arguments:**
  - `length: int` - Desired number of digits; must be at least 1.
- **Returns:**
  - `int` - Salt within the inclusive range `[10**(length-1), 10**length - 1]`.
- **Raises:**
  - `ValueError`: Provided length is below the acceptable threshold.

**Usage Example:**

```python
salt = SimpleCrypto.salt_generator(length=6)
print(salt)
```

---

### `SimpleCrypto.caesar_encrypt()` / `SimpleCrypto.caesar_decrypt()`

**Detailed Description:**
Encode and decode messages by shifting characters within the generated table. The shift comes from the salt modulo table length, ensuring consistent wrap-around behaviour no matter the alphabet size. Both methods validate parameter types before attempting the translation.

**Signature:**

```python
@classmethod
def caesar_encrypt(cls, salt: int, message: str) -> str

@classmethod
def caesar_decrypt(cls, salt: int, message: str) -> str
```

- **Arguments:**
  - `salt: int` - Rotation seed; any integer is accepted.
  - `message: str` - Text to transform.
- **Returns:**
  - `str` - Encoded (encrypt) or decoded (decrypt) message.
- **Raises:**
  - `TypeError`: Salt is not an integer.
  - `TypeError`: Message is not a string instance.

**Usage Example:**

```python
salt = SimpleCrypto.salt_generator()
encoded = SimpleCrypto.caesar_encrypt(salt, "Kryptos")
decoded = SimpleCrypto.caesar_decrypt(salt, encoded)
assert decoded == "Kryptos"
```

---

### `SimpleCrypto.rot13_codec()`

**Detailed Description:**
Wraps Python's built-in ROT13 codec with Raise-based validation. ROT13 acts as its own inverse, so calling the method twice returns the original message.

**Signature:**

```python
@classmethod
def rot13_codec(cls, message: str) -> str
```

- **Arguments:**
  - `message: str` - ASCII-compatible text to encode or decode.
- **Returns:**
  - `str` - ROT13-transformed message.
- **Raises:**
  - `TypeError`: Message is not a string instance.

**Usage Example:**

```python
cipher = SimpleCrypto.rot13_codec("uryyb")
plain = SimpleCrypto.rot13_codec(cipher)
assert plain == "hello"
```

---

### `SimpleCrypto.b64_encrypt()` / `SimpleCrypto.b64_decrypt()`

**Detailed Description:**
Round-trip strings through Base64 using UTF-8 bytes on encode and ASCII payloads on decode. The decoder validates input so malformed data raises a ValueError with a consistent error message.

**Signature:**

```python
@classmethod
def b64_encrypt(cls, message: str) -> str

@classmethod
def b64_decrypt(cls, message: str) -> str
```

- **Arguments:**
  - `message: str` - Text to encode or decode.
- **Returns:**
  - `str` - Encoded or decoded value, depending on direction.
- **Raises:**
  - `TypeError`: Message is not a string instance.
  - `ValueError`: Provided payload is not valid Base64 (decrypt only).

**Usage Example:**

```python
encoded = SimpleCrypto.b64_encrypt("payload")
decoded = SimpleCrypto.b64_decrypt(encoded)
assert decoded == "payload"
```

---

### `SimpleCrypto.multiple_encrypt()` / `SimpleCrypto.multiple_decrypt()`

**Detailed Description:**
Provide a convenience wrapper that chains ROT13, Caesar, and Base64. The decrypt counterpart reverses the sequence and propagates Base64 validation errors, making it simple to store or transmit ASCII-safe ciphertexts.

**Signature:**

```python
@classmethod
def multiple_encrypt(cls, salt: int, message: str) -> str

@classmethod
def multiple_decrypt(cls, salt: int, message: str) -> str
```

- **Arguments:**
  - `salt: int` - Caesar rotation seed reused across the chain.
  - `message: str` - Plain-text (encrypt) or chained ciphertext (decrypt).
- **Returns:**
  - `str` - Fully encoded or decoded message.
- **Raises:**
  - `TypeError`: Message is not a string instance.
  - `ValueError`: Base64 payload embedded inside the chain is invalid.

**Usage Example:**

```python
salt = SimpleCrypto.salt_generator(5)
secret = SimpleCrypto.multiple_encrypt(salt, "Sensitive data")
original = SimpleCrypto.multiple_decrypt(salt, secret)
assert original == "Sensitive data"
```
