from pathlib import Path
from shutil import move
import os
import json
import requests
from zipfile import ZipFile
import time

CURRENT_PATH = str(Path.cwd())
DATA_PATH = CURRENT_PATH + "/data"
GENOME_PATH = CURRENT_PATH + "/file.zip"
ALPHABET = ['a', 'c', 'g', 't', 'n', 'A', 'C', 'G', 'T', 'N']

def load(body):
    return json.loads(body)

def createPath(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# Format antibiotic for api
def formatAntibiotic(antibiotic):
    formatted = ""
    parts = antibiotic.split(".") #If antibiotic is of form A/B
    first = parts[0].split(" ")
    if len(parts) == 2:
        # If one of the antibiotics is an acid, i.e clauvalanic acid
        second = parts[1].split(" ")
        if len(first) == 2: 
            formatted = f"{second[0]}%2520{second[1]}%252F{first[0]}"
        elif len(second) == 2:
            formatted = f"{first[0]}%252F{second[0]}%2520{second[1]}"
        else:
            formatted = f"{first}%252F{second}"
    elif len(first) == 2:
        formatted = f"{first[0]}%2520{first[1]}"
    else:
        formatted = first[0]

    return formatted

def readMetadata(bacterium, antibiotic):
    path = f"{DATA_PATH}/{bacterium}/{antibiotic}"
    with open(path+"/meta.csv", 'r') as metadata:
        next(metadata)
        for line in metadata:
            parts = line.split(",")
            genomeID = parts[1].strip("\"")
            file = f"/{genomeID}.fna"
            downloadGenome(path+file, genomeID)
            break

def downloadMetadata(path, antibiotic, id, amount):
    URL = "https://www.bv-brc.org/api/genome_amr/?&http_accept=text/csv&http_download=true"
    formattedAntibiotic = formatAntibiotic(antibiotic)
    body = {
        "rql": f"eq(genome_id%2C*)%26genome(eq(taxon_lineage_ids%2C{id}))%26and(eq(evidence%2C%2522Laboratory%2520Method%2522)%2Ceq(antibiotic%2C%2522{antibiotic}%2522))%26sort(id)%26limit({amount})"
    }
    response = requests.post(URL, data=body)
    with open(path, mode="wb") as file:
        file.write(response.content)

def downloadGenome(path, genomeID):
    URL = "https://www.bv-brc.org/api/bundle/genome/" 
    body = {
        "archiveType": "zip",
        "types": "*.fna",
        "q": f"in(genome_id,({genomeID}))"
    }
    response = requests.post(URL, data=body)
    with open(GENOME_PATH, mode="wb") as file:
            file.write(response.content)
    unZip(path)

# unzip and move contents somewhere else
def unZip(dest):
    contents = ""
    with ZipFile(GENOME_PATH, 'r') as zip_ref:
        contents = zip_ref.namelist()
        if len(contents) == 0: return
        contents = contents[0] 
        zip_ref.extractall(CURRENT_PATH)
    parent, content = contents.split("/")
    src = f"{CURRENT_PATH}/{parent}/{content}"
    with open(f"{dest}/downloaded.csv", 'a') as downloadedFiles:
        withoutExtension = content.split(".fna")[0]
        downloadedFiles.write(f"{withoutExtension}\n")
    dest = f"{dest}/{content}"
    move(src, dest)
    os.rmdir(parent)
    # remove all lines that arent to do with the genome itself
    with open(dest, "r+") as genome:
        data = genome.readlines()
        genome.seek(0)
        for line in data:
            if line[0] in ALPHABET:
                genome.write(line)
        genome.truncate()

def getInitialFileSize(response, folder, id):
        contents = os.listdir(folder)
        found = False
        for file in contents:
            if file == "meta.csv" or file == "downloaded.csv" or file=="counts.csv": continue
            found = True
            file_stats = os.stat(f"{folder}/{file}")
            return file_stats.st_size / 3 # unzipped
        if not found:
            with open(GENOME_PATH, mode="wb") as file:
                file.write(response.content)
                with ZipFile(GENOME_PATH, 'r') as zip_ref:
                    contents = zip_ref.namelist()
                    if len(contents) == 0: return 0
                unZip(folder)
                os.remove(f"{folder}/{id}.fna")
                return file.tell()