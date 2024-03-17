import os
import shutil
import datetime

# -------------------------------------------
# Utilitka pro presun Vycetek na Google Drive
# -------------------------------------------

# Dohledani google disku na PC
def get_gdrive():
    # Iterace nad pismeny
    for drive_letter in range(ord('A'), ord('Z') + 1):
        drive = chr(drive_letter) + ":\\Můj disk\\Vycetka"
        if os.path.exists(drive):
            return drive
    return None

# Promenne 
vycetka_path = "C:\\DecinkaApp\\Vycetka"
vycetka_files = os.listdir(vycetka_path)
googledrive_path = get_gdrive()
file_time = datetime.date.today()
file_log_path = "C:\\DecinkaApp\\Logs\\file_2_gdrive-" + file_time.strftime("%Y-%m-%d") + ".txt"
s_timestamp = datetime.datetime.today() - datetime.timedelta(30)

# Promenna pro napocet poctu souboru
pocet = 0
pocet_kopir = 0
pocet_move = 0
pocet_del = 0
pocet_arch = 0

# metoda pro logovani co se deje
def log2file(status, msg): 
    # Logovani souboru 
    timestamp = datetime.datetime.today()
    with open(file_log_path, 'a') as file_txt:
        file_txt.write("["+ timestamp.strftime("%Y-%m-%d %H:%M:%S:%f") +"] [" + status + "] - " + msg + "\n")

# Kontrola na nalezeni google disku
if googledrive_path != None:

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

                # dohledani jestli je již soubor archivovan
                file_exist = os.path.exists(googledrive_path + "\\" + file)

                # Pokud je soubor novejsi nez 30 dnu a neni na google drive, tak se zkopiruje
                if file_exist == False and m_timestamp > s_timestamp:
                    shutil.copy(vycetka_path + "\\" + file, googledrive_path)
                    log2file("INFO", "Soubor " + file + " byl prekopirovan na Google Drive")
                    pocet_kopir = pocet_kopir + 1

                # Pokud je soubor starsi jak 30 dnu a neni na disku, tak se presune a nezustane na disku
                elif file_exist == False:
                    shutil.move(vycetka_path + "\\" + file, googledrive_path)
                    log2file("INFO", "Soubor " + file + " presunut na Google Drive")
                    pocet_move = pocet_move + 1

                # Pokud soubor je jiz na disku a je starsi jak 30 dnu, tak se odmaze
                elif file_exist == True and m_timestamp < s_timestamp: 
                    os.remove(vycetka_path + "\\" + file)
                    pocet_del = pocet_del + 1
                    log2file("INFO", "Soubor " + file + " je jiz archivovan na Google Drive, tak byl smazan z disku")

                # Pokud je file novejsi jak 30 dnu, je již na disku, tak se pouze zaloguje
                else:
                    log2file("INFO", "Soubor " + file + " je jiz archivovan na Google Drive, ale je novejsi jak 30 dnu, tak nebyl smazan")
                    pocet_arch = pocet_arch + 1

            # Pokud je jiz vycetka na Google Drive nebo problem s shutil knihovnou
            except shutil.Error as ex:
                log2file("ERROR", "Soubor " + file + " se nepodarilo presunout/zkopirovat na Google Drive " + str(ex))
                pocet_move = pocet_move + 1
                os.remove(vycetka_path + "\\" + file)

            # Odchyceni jinych chyb 
            except Exception as ex:
                log2file("ERROR", "Soubor " + file + " se nepodařilo presunout z důvodu chyby: " + str(ex))
                raise Exception("ERROR - " + str(ex))

        # Pokud neni co k presunuti, tak se to zaloguje    
        else:
            log2file("INFO", "Neni co k presunuti, utilitka se ukončí")

    # konec utiliky + vypsani do logu
    file_time = datetime.datetime.today()
    print("[" + file_time.strftime("%Y-%m-%d %H:%M:%S") +"]" + " [INFO] - CELKEM DENNÍCH VÝČETEK: " + str(pocet))
    print("[" + file_time.strftime("%Y-%m-%d %H:%M:%S") +"]" + " [INFO] - PRESUNUTO: " + str(pocet_move))
    print("[" + file_time.strftime("%Y-%m-%d %H:%M:%S") +"]" + " [INFO] - PREKOPIROVANO: " + str(pocet_kopir))
    print("[" + file_time.strftime("%Y-%m-%d %H:%M:%S") +"]" + " [INFO] - ARCHIVOVÁNO: " + str(pocet_arch))
    print("[" + file_time.strftime("%Y-%m-%d %H:%M:%S") +"]" + " [INFO] - SMAZÁNO: " + str(pocet_del))

# Pokud se nenajde disk, tak se to zaloguje a vyhodi chyba
else:
    log2file("ERROR", "Nenalezen google disk na danem pc!")
    raise RuntimeError