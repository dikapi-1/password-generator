"""Secure random password generator.

Uses the `secrets` module, which draws randomness from the operating
system's cryptographically secure source.

Run without arguments for interactive mode, or pass flags (see --help).
"""

import argparse
import secrets
import string
import sys

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/~"
AMBIGUOUS = set("Il1O0o|`'\"")


def generate_password(
    length: int = 16,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    """Generate a cryptographically secure random password.

    The password is guaranteed to contain at least one character from
    every enabled character set.
    """
    pools = []
    if use_lower:
        pools.append(LOWERCASE)
    if use_upper:
        pools.append(UPPERCASE)
    if use_digits:
        pools.append(DIGITS)
    if use_symbols:
        pools.append(SYMBOLS)

    if exclude_ambiguous:
        pools = ["".join(c for c in p if c not in AMBIGUOUS) for p in pools]

    pools = [p for p in pools if p]
    if not pools:
        raise ValueError("At least one character set must be enabled.")
    if length < len(pools):
        raise ValueError(f"Length must be at least {len(pools)}.")

    # Guarantee at least one character from each enabled set
    chars = [secrets.choice(p) for p in pools]

    # Fill the rest from the combined alphabet
    alphabet = "".join(pools)
    chars += [secrets.choice(alphabet) for _ in range(length - len(chars))]

    # Shuffle with a cryptographically secure RNG
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def interactive() -> None:
    """Ask the user for options in the console."""
    length = int(input("Password length (Enter = 16): ") or 16)
    count = int(input("How many passwords (Enter = 1): ") or 1)
    no_ambiguous = input("Exclude ambiguous characters (l, 1, O, 0)? [y/N]: ").strip().lower() == "y"

    print()
    for _ in range(count):
        print(generate_password(length=length, exclude_ambiguous=no_ambiguous))


def main() -> None:
    if len(sys.argv) == 1:
        interactive()
        return

    parser = argparse.ArgumentParser(description="Generate secure random passwords.")
    parser.add_argument("-l", "--length", type=int, default=16, help="password length (default: 16)")
    parser.add_argument("-n", "--count", type=int, default=1, help="number of passwords (default: 1)")
    parser.add_argument("--no-lower", action="store_true", help="exclude lowercase letters")
    parser.add_argument("--no-upper", action="store_true", help="exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true", help="exclude digits")
    parser.add_argument("--no-symbols", action="store_true", help="exclude symbols")
    parser.add_argument("--no-ambiguous", action="store_true", help="exclude look-alike characters (l, 1, O, 0, ...)")
    args = parser.parse_args()

    try:
        for _ in range(args.count):
            print(generate_password(
                length=args.length,
                use_lower=not args.no_lower,
                use_upper=not args.no_upper,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
                exclude_ambiguous=args.no_ambiguous,
            ))
    except ValueError as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
