

#!/usr/bin/env python3
"""Palindrome checker logic."""

def normalize_text(text):
    """Normalize text by removing non-alphanumeric characters and lowercasing."""
    return ''.join(ch for ch in text.lower() if ch.isalnum())


def is_palindrome(text):
    """Return True if the normalized text is a palindrome."""
    normalized = normalize_text(text)
    return normalized == normalized[::-1]


if __name__ == "__main__":
    user_input = input("Enter phrase to check>>> ").strip()
    if is_palindrome(user_input):
        print("correct")
    else:
        print("incorrect")