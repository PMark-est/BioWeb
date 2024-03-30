# Webapp to make downloading files from the website https://www.bv-brc.org/ easier.

## Only fasta files that are categroized under "amr_phenotype" are downloaded

## Prerequisites

- Python installed (Definitely works with 3.10.12)
  - Pip installed
- requirements.txt installed
  - `pip install -r requirements.txt`
- node installed
- npm installed
- run `npm install` inside the folder "frontend"

## How to run

To start the backend, run

```bash
python manage.py runserver
```

To start the frontend, inside the frontend folder run

```bash
npm run dev
```

# Useful to use with https://github.com/PMark-est/Kmer-Counter.
