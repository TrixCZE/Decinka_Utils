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
    
def check_drive_and_directory(drive_letter: str = None, full_directory: str = None) -> bool:
    """
    Checks if a specified drive and/or directory exists.

    Args:
        drive_letter (str, optional): Drive letter to check (e.g., 'C', 'D')
        full_directory (str, optional): Full directory path to check
        
    Returns:
        bool: True if the specified drive and/or directory exists, False otherwise
    """
    if not drive_letter and not full_directory:
        raise ValueError("At least one parameter (drive_letter or full_directory) must be provided")

    # Check drive if specified
    drive_exists = True
    if drive_letter:
        # Normalize drive letter format
        drive_path = f"{drive_letter.upper()}:\\"
        drive_exists = os.path.exists(drive_path)
        
        # If only drive check was requested, return result
        if not full_directory:
            return drive_exists

    # Check directory if specified
    directory_exists = True
    if full_directory:
        directory_exists = os.path.exists(full_directory)
        
        # If only directory check was requested, return result
        if not drive_letter:
            return directory_exists

    # If both were specified, return True only if both exist
    return drive_exists and directory_exists