import datetime
import os

# -----------------------------------------------------------------
# Generic utilika slouzici pro zavolani vsemoznych funkci a method
# -----------------------------------------------------------------

# Metoda pro logovani udalosti do souboru
file_time = datetime.date.today()
file_log_path = "C:\\DecinkaApp\\Logs\\file_2_gdrive-" + file_time.strftime("%Y-%m-%d") + ".txt"

def log2file(status, msg): 
    # Logovani souboru 
    timestamp = datetime.datetime.today()
    with open(file_log_path, 'a') as file_txt:
        file_txt.write("["+ timestamp.strftime("%Y-%m-%d %H:%M:%S:%f") +"] [" + status + "] - " + msg + "\n")

# Dohledani google disku na PC
def get_gdrive():
    # Iterace nad pismeny
    for drive_letter in range(ord('A'), ord('Z') + 1):
        drive = chr(drive_letter) + ":\\Můj disk\\Vycetka"
        if os.path.exists(drive):
            return drive
    return None