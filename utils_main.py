import datetime
import os

# -----------------------------------------------------------------
# Generic utilika slouzici pro zavolani vsemoznych funkci a method
# -----------------------------------------------------------------

# Metoda pro logovani udalosti do souboru
file_time = datetime.date.today()

def log2file(status, msg, log_file_name): 
    '''
    Pouzite pro logovani zprav do souboru
    
    status (str) => Status volani INFO, WARN, ERROR 
    msg (str) => Zprava volani nejaky text ci cokoliv
    log_file_name (str) => Nazev log souboru
    '''
    # Logovani souboru 
    file_log_path = "C:\\DecinkaApp\\Logs\\" + log_file_name + "-" + file_time.strftime("%Y-%m-%d") + ".txt"

    timestamp = datetime.datetime.today()
    with open(file_log_path, 'a') as file_txt:
        file_txt.write("["+ timestamp.strftime("%Y-%m-%d %H:%M:%S:%f") +"] [" + status + "] - " + msg + "\n")

# Dohledani google disku na PC
def get_gdrive():
    '''
    Slouzi pro nalezeni google drive disku na PC
    '''
    # Iterace nad pismeny
    for drive_letter in range(ord('A'), ord('Z') + 1):
        drive = chr(drive_letter) + ":\\Můj disk\\Vycetka"
        if os.path.exists(drive):
            return drive
    return None