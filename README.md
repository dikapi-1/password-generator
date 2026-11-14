# Password Generator

A small, dependency-free Python script that generates cryptographically secure random passwords.

## Features

- Uses Python's `secrets` module for unpredictable randomness
- Every enabled character set (lowercase, uppercase, digits, symbols) is guaranteed to appear at least once
- Optional exclusion of look-alike characters (`l`, `1`, `I`, `O`, `0`, ...)
- Two modes: interactive prompts or command-line flags
- Generate one or many passwords at once

## Requirements

- Python 3.8+
- No third-party dependencies

## Usage

### Interactive mode

Run the script without arguments and answer the prompts:

```bash
python password_gen.py
```

```
Password length (Enter = 16): 20
How many passwords (Enter = 1): 3
Exclude ambiguous characters (l, 1, O, 0)? [y/N]: y
```

### Command-line mode

```bash
# One 16-character password
python password_gen.py -l 16

# Five 24-character passwords without look-alike characters
python password_gen.py -l 24 -n 5 --no-ambiguous

# Letters and digits only
python password_gen.py --no-symbols
```

| Flag | Description |
|------|-------------|
| `-l`, `--length` | Password length (default: 16) |
| `-n`, `--count` | Number of passwords (default: 1) |
| `--no-lower` | Exclude lowercase letters |
| `--no-upper` | Exclude uppercase letters |
| `--no-digits` | Exclude digits |
| `--no-symbols` | Exclude symbols |
| `--no-ambiguous` | Exclude look-alike characters |

### As a module

```python
from password_gen import generate_password

print(generate_password(length=20, exclude_ambiguous=True))
```

## Why `secrets` and not `random`?

The `random` module is a pseudo-random generator designed for simulations and games. Its output can be predicted if enough values are observed, so it must not be used for passwords. The `secrets` module uses the operating system's cryptographically secure random source and is the recommended choice for passwords, tokens and keys.

## License

[MIT](LICENSE)
