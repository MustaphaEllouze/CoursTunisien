import json
import os
from dataclasses import dataclass
from collections import defaultdict
from typing import ClassVar, Self

from constants import (
    LEXION_FILE, SOUNDS_FILE, ROOTS_FILE, LOAN_FILE
)


# --------------- Classes
@dataclass
class Sound : 
    representation : str
    id             : int

    sounds_from_repr : ClassVar[dict[str, Self]] = {}
    sounds_from_id   : ClassVar[dict[int, Self]] = {}

    def __post_init__(self):
        Sound.sounds_from_repr[self.representation] = self
        Sound.sounds_from_id[self.id]               = self

@dataclass
class Root:
    meaning    : str
    id         : int
    first      : str = None
    second     : str = None
    third      : str = None
    fourth     : str = None
    still_used : bool = True

    roots_from_id : ClassVar[dict[int, Self]] = {}

    def __post_init__(self):
        if self.id in Root.roots_from_id : 
            raise ValueError(f'Root ID {self.id} already exists')
        Root.roots_from_id[self.id] = self
        self.representation = str(self)
    
    def __str__(self)->str:
        result = ''

        for i,letter in enumerate(
            (self.first, self.second, self.third, self.fourth)
        ):
            if i in (1,2) or (i==3 and letter): result += '-'
            if letter or i< 3 : 
                result += letter if letter else '*'

        return result

@dataclass
class LoanWord :
    writing : str
    origin  : str
    id      : int

    loanwords_from_id : ClassVar[dict[int, Self]] = {}

    def __post_init__(self):
        if self.id in LoanWord.loanwords_from_id : 
            raise ValueError(f'LoanWord ID {self.id} already exists')
        LoanWord.loanwords_from_id[self.id] = self

@dataclass
class Word : 
    writing         : str
    id              : int
    meaning         : str
    function        : str
    root_id         : int = None
    is_feminine     : bool = False
    feminine        : str = None
    plural          : str = None
    loanword_id     : int = None

    # automatic
    root            : Root = None
    loanword        : LoanWord = None

    # Class variables
    words_from_id : ClassVar[dict[int, Self]] = {}
    all_words     : ClassVar[list[Self]] = []

    def __post_init__(self):
        if self.id in Word.words_from_id : 
            raise ValueError(f'Word ID {self.id} already exists')
        Word.words_from_id[self.id] = self
        Word.all_words.append(self)

        # Linking via IDs
        if self.root_id : 
            self.root = Root.roots_from_id[self.root_id]
        if self.loanword_id : 
            self.loanword = LoanWord.loanwords_from_id[self.loanword_id]

# ---------------- Functions
def load_json(file_path:str, access_key:str)->dict:
    assert os.path.isfile(file_path)
    data= json.load(open(file=file_path, mode='r'))
    assert access_key in data

    return data[access_key]

def gather_words_via_roots()->dict[Root, list[Word]]:
    result = defaultdict(list)
    for word in Word.words_from_id.values():
        if word.root_id : 
            result[word.root_id].append(word)
    return result

def gather_words_without_roots()->list[Word]:
    return [w for w in Word.words_from_id.values() if not w.root]

def check_word_uniqueness()->bool:
    return len(Word.all_words) == len(set([w.writing for w in Word.all_words]))

def find_duplicate_words()->list[Word]:
    return [
        w for w in Word.all_words
        if [w.writing for w in Word.all_words].count(w.writing) > 1
    ]

def check_root_uniqueness()->bool:
    return len(Root.roots_from_id) == len(set([str(r) for r in Root.roots_from_id.values()]))

def find_duplicate_roots()->list[Root]:
    return [
        r for r in Root.roots_from_id.values()
        if [str(r) for r in Root.roots_from_id.values()].count(str(r))>1
    ]


# ---------------- Main script
def main()->None:

    # --- Load all data files
    lexicon = load_json(LEXION_FILE, "lexicon")
    roots = load_json(ROOTS_FILE, "roots")
    loan_words = load_json(LOAN_FILE, "loan_words")
    sounds = load_json(SOUNDS_FILE, "sounds")

    # --- Create all sounds 
    sounds_objects = [Sound(**s) for s in sounds]

    # --- Create all roots
    roots_objects = [Root(**r) for r in roots]

    # --- Create all loan words
    loan_objects = [LoanWord(**lw) for lw in loan_words]

    # --- Create lexicon
    words_objets = [Word(**w) for w in lexicon]

    # --- Check there are no duplicates in words, roots
    if not check_root_uniqueness():
        print('There are duplicate roots: ')
        for r in find_duplicate_roots():
            print(f'    {str(r)}, ID={r.id}')
        raise ValueError('There are duplicate roots.')

    if not check_word_uniqueness():
        print('There are duplicate words: ')
        for w in find_duplicate_words():
            print(f'    {w.writing}, ID={w.id}')
        raise ValueError('There are duplicate words.')

    # --- Assemble words by common root, and without any root
    words_by_roots = gather_words_via_roots()
    words_rootless = gather_words_without_roots()

# ---------------- Execute 
if __name__ == '__main__':
    main()