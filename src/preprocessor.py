import re, json
from os import path
from functools import reduce

def load_romanization_table(paths: list[str]):
    tables: dict[str, str] = {}
    for path in paths:
        with open(path) as f:
            for k, v in json.load(f).items():
                tables[k] = v

    tables = dict(sorted(tables.items(), key = lambda x: -len(x[0])))

    return tables

romanization_table = load_romanization_table([
    path.join(path.dirname(__file__), "romanization/hepburn.json"),
    path.join(path.dirname(__file__), "romanization/japanese.json")
])

romanization_table_key_regexp = "|".join(map(re.escape, romanization_table.keys()))

def preprocess_url(text: str):
    return re.sub(r"https?://(([a-zA-Z0-9]-)*[a-zA-Z0-9]+.)*[a-zA-Z0-9](-[a-zA-Z0-9]+)*(/[a-zA-Z0-9-.]+)*(\?[a-zA-Z0-9%=-]*)?/?", "URL省略", text)

def preprocess_emoji(text: str):
    return re.sub(r"<a?:([_a-zA-Z0-9-]+):[0-9]+>", r"\1", text)

def preprocess_alphabet(text: str):
    return re.sub(romanization_table_key_regexp, lambda k: romanization_table[k.group()], text)

def preprocess_text(text: str):
    processors = [
        preprocess_url,
        preprocess_emoji,
        preprocess_alphabet,
    ]

    return reduce(lambda p, c: c(p), processors, text)