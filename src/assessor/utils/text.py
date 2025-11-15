def normalize_text(text):
    """Normalize text by converting to lowercase and stripping whitespace."""
    return text.lower().strip()

def extract_words(text):
    """Extract words from a given text, returning a list of words."""
    return text.split()

def count_words(text):
    """Count the number of words in a given text."""
    words = extract_words(text)
    return len(words)

def is_empty(text):
    """Check if the given text is empty or contains only whitespace."""
    return not text or text.isspace()