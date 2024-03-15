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
s_timestamp = datetime.datetime.today() - datetime.timedelta(30)

# Promenna pro napocet poctu souboru
pocet = 0
pocet_kopir = 0
pocet_move = 0

# methoda
def log2file(file, status, msg): 
    # Logovani souboru 
    timestamp = datetime.datetime.today()
    with open(file_path, 'a') as file_txt:
        file_txt.write("["+ timestamp.strftime("%Y-%m-%d %H:%M:%S:%f") +"] [" + status + "] - Soubor " + file + " " + msg + "\n")

# Cyklus prochazeni souboru
for file in vycetka_files:
    
    # kontrola jestli je soubor vycetka
    if file.__contains__("Vycetka"):
        
        # pocitani souboru
        pocet = pocet + 1
        
        # Presun souboru na google drive 
        try:
            # Ziskani modifikace souboru
            modify_timestamp = os.path.getmtime(vycetka_path + "\\" + file)
            m_timestamp = datetime.datetime.fromtimestamp(modify_timestamp)

            # Pokud je soubor starsiho data tak se presune a nebude uz na disku
            if m_timestamp > s_timestamp:
                # Pokusi se prekopirovat soubor na Google DRIVE
                shutil.copy(vycetka_path + "\\" + file, googledrive_path)
                log2file(file, "INFO", "prekopirovan na Google Drive")
                pocet_kopir = pocet_kopir + 1

            else:
                # Pokusi se prekopirovat soubor na Google DRIVE
                shutil.move(vycetka_path + "\\" + file, googledrive_path)
                log2file(file, "INFO", "presunut na Google Drive")
                pocet_move = pocet_move + 1

        # Odchyceni chyby 
        except Exception as ex:
            log2file(file, "ERROR", "se nepodařilo presunout " + str(ex))
            raise Exception("ERROR - " + str(ex))

# konec 
file_time = datetime.datetime.today()
print("[" + file_time.strftime("%Y-%m-%d %H:%M:%S:%f") +"]" + " - Celkem presunuto " + str(pocet_move) + " vycetek a prekopirovano " + str(pocet_kopir) + " vycetek")
