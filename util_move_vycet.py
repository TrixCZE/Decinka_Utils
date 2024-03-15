import os
import shutil
import datetime

# -------------------------------------------
# Utilitka pro presun Vycetek na Google Drive
# -------------------------------------------

# Promenne 
vycetka_path = "C:\\DecinkaApp\Vycetka"
vycetka_files = os.listdir(vycetka_path)
googledrive_path = "H:\\Můj disk\Vycetka"
file_time = datetime.date.today()
file_path = "C:\\DecinkaApp\\Logs\\file_2_gdrive-" + file_time.strftime("%Y-%m-%d") + ".txt"

# Promenna pro napocet poctu souboru
pocet = 0

# methoda
def log2file(file, status): 
    # Logovani souboru 
    timestamp = datetime.datetime.today()
    with open(file_path, 'a') as file_txt:
        file_txt.write("["+ timestamp.strftime("%Y-%m-%d %H:%M:%S:%f") +"] [" + status + "] - Soubor " + file + " presunut na Google Drive" + "\n")

for file in vycetka_files:
    
    # kontrola jestli je soubor vycetka
    if file.__contains__("Vycetka"):
        
        # pocitani souboru
        pocet = pocet + 1
        
        # Presun souboru na google drive 
        try:
            # Pokusi se prekopirovat soubor na Google DRIVE
            shutil.copy(vycetka_path + "\\" + file, googledrive_path)
            log2file(file, "INFO")

        except Exception as ex:
            log2file(file, "ERROR")
            raise Exception("ERROR 1001 - " + ex)

# konec 
file_time = datetime.datetime.today()
print("[" + file_time.strftime("%Y-%m-%d %H:%M:%S:%f") +"]" + " - Celkem presunuto " + str(pocet) + " souboru")
