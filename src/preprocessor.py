import re
from functools import reduce

def preprocess_url(text: str):
    return re.sub(r"https?://(([a-zA-Z0-9]-)*[a-zA-Z0-9]+.)*[a-zA-Z0-9](-[a-zA-Z0-9]+)*(/[a-zA-Z0-9-.]+)*(\?[a-zA-Z0-9%=-]*)?/?", "URL省略", text)


def preprocess_text(text: str):
    processors = [
        preprocess_url
    ]

    return reduce(lambda p, c: c(p), processors, text)