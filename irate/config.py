from pathlib import Path


BASE_PATH:Path = Path(__file__).parent.parent
DATABASE_PATH:Path = Path.joinpath(BASE_PATH, 'jsonDB')

if DATABASE_PATH.exists():
    pass
else:
    DATABASE_PATH.mkdir(exist_ok=True)
