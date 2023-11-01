from pathlib import Path
import os

EXTENSIONS_A_SUPPRIMER = (
    'aux',
    'synctex.gz',
    'fdb_latexmk',
    'fls',
    'toc',
    'out',
)

for _extension in EXTENSIONS_A_SUPPRIMER : 
    for path in Path('./').rglob(f'*.{_extension}'):
        print(f'Deleting {path}')
        os.remove(path)