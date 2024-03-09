from django.shortcuts import render
from django.http import JsonResponse
from pathlib import Path
import os
import requests
from zipfile import ZipFile
CURRENT_PATH = str(Path.cwd())
DATA_PATH = CURRENT_PATH + "/data"
ZIP_PATH = CURRENT_PATH + "/meta.zip"

def createPath(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# Format antibiotic for api
def formatAntibiotic(antibiotic):
    formatted = ""
    parts = antibiotic.split("/") #If antibiotic is of form A/B
    first = parts[0].split(" ")
    if len(parts) == 2:
        # If one of the antibiotics is an acid, i.e clauvalanic acid
        second = parts[1].split(" ")
        if len(first) == 2: 
            formatted = f"{second[0]}%2520{second[1]}%252F{first}"
        elif len(second) == 2:
            formatted = f"{first}%252F{second[0]}%2520{second[1]}"
        else:
            formatted = f"{first}%252F{second}"
    elif len(first) == 2:
        formatted = f"{first[0]}%2520{first[1]}"
    else:
        formatted = first[0]

    return formatted



def downloadMetadata(antibiotic, id, amount):
    print("started download")
    URL = "https://www.bv-brc.org/api/genome_amr/?&http_accept=text/csv&http_download=true"
    formattedAntibiotic = formatAntibiotic(antibiotic)
    fileName = "meta.csv"
    print(formattedAntibiotic)
    body = {
        "rql": f"eq(genome_id%2C*)%26genome(eq(taxon_lineage_ids%2C{id}))%26eq(antibiotic%2C%2522{formattedAntibiotic}%2522)%26sort(id)%26limit({amount})"
    }
    #"eq(genome_id%2C*)%26genome(eq(taxon_lineage_ids%2C1763))%26eq(antibiotic%2C%2522amoxicillin%2522)%26sort(id)%26limit(766)"
    response = requests.post(URL, data=body)
    with open(fileName, mode="wb") as file:
        file.write(response.content)
    print("downloaded")

def downloadGenome(genomeID):
    URL = "https://www.bv-brc.org/api/bundle/genome/" 
    fileName = "meta.zip"
    body = {
        "archiveType": "zip",
        "types": "*.fna",
        "q": f"in(genome_id,({genomeID}))"
    }
    response = requests.post(URL, data=body)
    with open(fileName, mode="wb") as file:
        file.write(response.content)
    print("downloaded")
    
def unZip(path):
    contents = ""
    with ZipFile(ZIP_PATH, 'r') as zip_ref:
        contents = zip_ref.namelist()[0]
        zip_ref.extractall(CURRENT_PATH)
    parent, content = contents.split("/")
    src = CURRENT_PATH+"/"+contents
    dest = DATA_PATH + "/" + content
    parent = CURRENT_PATH + "/" + parent
    os.rename(src, dest)
    os.rmdir(parent)
    
    

# Create your views here.
def home(request):
    return JsonResponse({'b': 'a'})

def test(request):
    antibiotic = request.GET.get("antibiotic")
    bacterium = request.GET.get("bacterium")
    amount = request.GET.get("amount")
    id = request.GET.get("id")
    path = DATA_PATH + "/" + bacterium + "/" + antibiotic
    #createPath(path)
    #downloadMetadata(antibiotic, id, amount)
    #unZip(path)
    #os.remove(ZIP_PATH)
    return JsonResponse({'antibiotic': antibiotic, "bacterium": bacterium})
