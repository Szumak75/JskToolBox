# StringTool

The project contains sets of classes for various operations on string.

## Public classes

1. [SimpleCrypto](https://github.com/Szumak75/JskToolBox/blob/1.0.21/docs/StringTool.md#simplecrypto)

## SimpleCrypto

The class for simple cryptographic operation on string.

### Import

```
from jsktoolbox.stringtool.crypto import SimpleCrypto
```

### Static methods

```
.chars_table_generator(): str
```

The method returns an extended string of printable characters for internal use.

### Public methods

```
.salt_generator(length: int = 8): int
```

A helper method that returns a random number with the given number of digits.
The 'salt' is used to calculate the offset in the translation table for 'caesar' methods and is a constant value required in the encryption/decryption process for a given string.

```
.caesar_encrypt(salt: int, message: str): str
```

The 'caesar' encryption method is based on a translation table with an offset calculated for the given 'salt' parameter. Returns an encrypted string.

```
.caesar_decrypt(salt: int, message: str): str
```

The 'caesar' decryption method is based on a translation table with an offset calculated for the given 'salt' parameter. Returns an decrypted string.

```
.rot13_codec(message: str): str
```

Simple rot13 encryption/decryption algorithm.

```
.b64_encrypt(message: str): str
```

The base64 encryption method. Returns decoded string from bytes.

```
.b64_decrypt(message: str): str
```

The base64 decryption method. Returns decoded string from bytes.

```
.multiple_encrypt(salt: int, message: str): str
```

The encryption method processes multiple cryptographic operations on a given string. Returns an encrypted string.
The 'salt' is a constant value required in the encryption/decryption process for a given string.

```
.multiple_decrypt(salt: int, message: str): str
```

The decryption method processes multiple cryptographic operations on a given string. Returns an decrypted string.
The 'salt' is a constant value required in the encryption/decryption process for a given string.
