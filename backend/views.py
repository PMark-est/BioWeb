from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
import time
from .functions import *
from django.views.decorators.csrf import csrf_exempt
    
# Create your views here.
def home(request):
    return HttpResponse()

@csrf_exempt 
def metadataDownload(request):
    body = load(request.body)
    antibiotic = body["antibiotic"]
    amount = body["amount"]
    id = body["id"]
    bacterium = body["bacterium"]
    antibiotic = antibiotic.split("/")
    if len(antibiotic) == 2:
        antibiotic = f"{antibiotic[0]}.{antibiotic[1]}"
    else:
        antibiotic = antibiotic[0]
    path = f"{DATA_PATH}/{bacterium}/{antibiotic}"
    metaPath = f"{path}/meta.csv"
    createPath(path)
    downloadMetadata(metaPath, antibiotic, id, amount)
    summaryPath = f"{DATA_PATH}/{bacterium}/metadataSummary.csv"
    susceptibles = 0
    resistants = 0
    with open(metaPath, "r") as metadata:
        next(metadata)
        for line in metadata:
            parts = line.split(",")
            pheno = parts[4].strip("\"")
            if pheno == "Resistant": resistants += 1
            elif pheno == "Susceptible": susceptibles += 1
    lines = []
    with open(summaryPath, "a+") as metadataSummary:
        metadataSummary.seek(0)
        lines = metadataSummary.readlines()

    repeat = False
    for i, line in enumerate(lines):
        parts = line.split(",")
        if parts[0] == antibiotic:
            lines[i] = f"{parts[0]},{resistants},{susceptibles}\n"
            repeat = True
            break
    if not repeat:
        lines.append(f"{antibiotic},{resistants},{susceptibles}\n")

    with open(summaryPath, "w") as metadataSummary:
        for line in lines:
            metadataSummary.write(line)
    return HttpResponse()

def viewContents(requests):
    bacterium = requests.GET.get("bacterium")
    files = []
    path = f"{DATA_PATH}/{bacterium}/metadataSummary.csv"
    if not os.path.exists(path):
        filesDict = {"files": []}
        return JsonResponse(filesDict)
    with open(f"{DATA_PATH}/{bacterium}/metadataSummary.csv", "r") as summary:
        for line in summary:
            parts = line.split(",")
            files.append(f"{parts[0]},{parts[1]},{parts[2].strip()}")
    filesDict = {"files": files}
    return JsonResponse(filesDict)

def viewFolders(requests):
    Path(DATA_PATH).mkdir(parents=True, exist_ok=True)
    folders = {"folders" : os.listdir(DATA_PATH)}
    return JsonResponse(folders)

def stream_data(bacterium, antibiotic, res, sus):
    # Generate data in chunks
    URL = "https://www.bv-brc.org/api/bundle/genome/" 
    body = {
                    "archiveType": "zip",
                    "types": "*.fna",
                    "q": f"in(genome_id,())"
                }
    folder = f"{DATA_PATH}/{bacterium}/{antibiotic}"
    path = f"{folder}/meta.csv"
    downloadedBytes = 0
    secs = 0.03
    size = 32768
    existingFiles = set()
    if os.path.exists(f"{folder}/downloaded.csv"):
        with open(f"{folder}/downloaded.csv", 'r') as downloadedFiles:
            for line in downloadedFiles:
                existingFiles.add(line.strip())
    
    with open(path, 'r') as metadata:
        next(metadata)
        parts = metadata.readline().split(",")
        id = parts[1].strip("\"")
        pheno = parts[4].strip("\"")
        body["q"] = f"in(genome_id,({id}))"
        response = requests.post(URL, data=body, stream=True)
        downloadedBytes = getInitialFileSize(response, folder, id)
        yield downloadedBytes
        dx = 100/((res + sus) * downloadedBytes)
        progress = size * dx
        metadata.seek(0)
        next(metadata)
        for line in metadata:
            parts = line.split(",")
            id = parts[1].strip("\"")
            if id in existingFiles: continue
            pheno = parts[4].strip("\"")
            if pheno == "Susceptible" and sus > 0:
                sus -= 1
                body["q"] = f"in(genome_id,({id}))"
                response = requests.post(URL, data=body, stream=True)
                with open(GENOME_PATH, mode="wb") as file:
                    for chunk in response.iter_content(chunk_size=size):
                        time.sleep(secs)
                        yield progress
                        file.write(chunk)
                unZip(folder)
            elif pheno == "Resistant" and res > 0:
                res -= 1
                body["q"] = f"in(genome_id,({id}))"
                response = requests.post(URL, data=body, stream=True)
                with open(GENOME_PATH, mode="wb") as file:
                    for chunk in response.iter_content(chunk_size=size):
                        time.sleep(secs)
                        yield progress
                        file.write(chunk)
                unZip(folder)
            if res == 0 and sus == 0: break
    os.remove(GENOME_PATH)

def stream(requests):
    bacterium = requests.GET.get("bacterium")
    antibiotic = requests.GET.get("antibiotic")
    res = int(requests.GET.get("resAmount"))
    sus = int(requests.GET.get("susAmount"))
    response = StreamingHttpResponse(stream_data(bacterium, antibiotic, res, sus))
    response['Content-Type'] = 'text/plain'
    return response