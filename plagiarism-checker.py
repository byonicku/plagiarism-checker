import glob
import os
import csv
from pyunpack import Archive

#base directory dimana file plagiarism-checker.py berada
base = os.path.dirname(os.path.realpath(__file__))

def check_zipped():
    for filepath in glob.glob(os.path.join(base, ".unzipped")):
        if filepath.endswith(".unzipped"):
            return 1
    
    return 0

def check_scanned():
    for filepath in glob.glob(os.path.join(base, "*")):
        relativeBase = os.path.relpath(filepath, base).split(os.sep)[0]
        
        if relativeBase.startswith("dolos-report"):
            return 1
        
    return 0

#cek ada compressed file atau tidak
def find_compress():
    for filepath in glob.glob(os.path.join(base, "**", "*"), recursive=True):
        if filepath.endswith(".zip") or filepath.endswith(".rar"):
            return 1

    return 0

def find_report():
    for filepath in glob.glob(os.path.join(base, "*")):
        relativeBase = os.path.relpath(filepath, base).split(os.sep)[0]
        
        if relativeBase.startswith("dolos-report"):
            return relativeBase

#extract compressed file in main folder
def extract_compress_main():
    for filepath in glob.glob(os.path.join(base, "*.zip")):
        Archive(filepath).extractall(base)
        os.remove(filepath)

#extract compressed file inside each folder
def extract_compress():
    for filepath in glob.glob(os.path.join(base, "**", "*"), recursive=True):
        relativeBase = os.path.relpath(filepath, base).split(os.sep)[0]
        
        if filepath.endswith(".zip") or filepath.endswith(".rar"):
            Archive(filepath).extractall(relativeBase)
            os.remove(filepath)

#convert ke csv
def to_csv():
    with open('info.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=("full_name", "filename"))
        writer.writeheader()
        for filepath in glob.glob(os.path.join(base, "**", "*"), recursive=True):
            relativeBase = os.path.relpath(filepath, base).split(os.sep)[0]
                
            if filepath.endswith(".c") or filepath.endswith(".cpp"):
                full_name = relativeBase.split("_")[0]
                writer.writerow({"full_name": full_name, "filename": filepath})

def __main__():
    if(check_zipped() == 0):
        open(".unzipped", "x")
        
        print("Processing main archive ...")
        extract_compress_main()

        print("Processing archive ...")
        extract_compress()

        if find_compress() == 1 :
            print("Processing sub archive ...")
            extract_compress()
    
    print("Running!")

    if(check_scanned() == 0):
        print("Processing to csv ...")
        to_csv()
        os.system("dolos -f web -l c info.csv")
    else:    
        os.system("dolos serve " + find_report())
    
    
if __name__ == "__main__":
    __main__()