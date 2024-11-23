import os, subprocess, mysql.connector, zipfile, time
from Utilities.utils_main import log2file, PrintMSG
from datetime import datetime, timedelta
from dotenv import load_dotenv

# ---------------------------------------------
# Utilitka pro vytvoreni dump souboru databaze
# ---------------------------------------------

# Promenne 
timestamp = datetime.today()
db_dump_folder = "C:\\DecinkaApp\\DB_Backup"
db_dumb_file = "DecinkaDB_backup_" + timestamp.strftime("%Y%m%d_%H%M%S") + ".sql"
db_log_file = "database_dump_log"
zip_file = "DecinkaDB_backup_" + timestamp.strftime("%Y%m%d_%H%M%S") + ".zip"
mysql_dir = "C:\\Program Files\\MySQL\\MySQL Workbench 8.0\\"
database_schema_name = "vinarnadzakaznici"

# Ziskani promennych z enviromentu
load_dotenv()
mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST", "localhost")
mysql_port = os.getenv("MYSQL_PORT", "3306")

# Tridy
class Dumb_File:
    def __init__(self, file_name, file_created, file_size, file_size_kb, file_extension, file_location):
        self.file_name = file_name
        self.file_created = file_created
        self.file_size = file_size
        self.file_size_kb = file_size_kb
        self.file_extension = file_extension
        self.file_location = file_location

# Test pripojeni do databaze
def check_db_connection():

    # Pokusim se o pripojeni do DB
    try:
        connection = mysql.connector.connect(
            host = mysql_host,
            user = mysql_username,
            password = mysql_password
        )

        # Ukoncim pripojeni + zaloguju uspesny test
        PrintMSG('Debug', 'util_db_dump', 'Úspěšné připojení do databáze! Mohu pokračovat s dumpem databáze...')
        log2file("INFO", 
                 "Úspěšné připojení do databáze! Mohu pokračovat s dumpem databáze...", 
                 db_log_file)
        connection.close()

        # Vratim status true ze jsem se pripojil
        return True

    # Pokud nastane chyba zaloguju
    except mysql.connector.Error as ex:

        # Vypisu chybu + ji zaloguju do souboru
        PrintMSG('ERROR', 'util_db_dump', f'Chyba při připojení do DB! Chyba: {ex}')
        log2file("ERROR", 
                 "Chyba při připojení do DB! Nemohu pokračovat s dumpem databáze... MySQL Chyba: " + str(ex), 
                 db_log_file)

        # Vratim false, ze jsem se nepripojil
        return False

# Kontrola jestli existuje adresar  
def check_directory():
    PrintMSG('Debug', 'util_db_dump', 'Kontroluji jestli existuje adresar DB_Backup...')

    if(os.path.exists(db_dump_folder)):
        
        # Vypis do logu
        PrintMSG('Debug', 'util_db_dump', f'Adresar {db_dump_folder} existuje a tak ukoncuji kontrolu adresare...')
        log2file("INFO", 
                 "Adresar " + db_dump_folder + " existuje a tak ukoncuji kontrolu adresare...", 
                 db_log_file)
        return
    
    else: 
        # Vypis do logu
        PrintMSG('Debug', 'util_db_dump', f'Adresar neni na disku... Bude vytvoren.')
        log2file("INFO", 
                 "Adresář není na disku... Bude vytvořen.", 
                 db_log_file)
        
        # Vytvoreni adresare + log do souboru
        try:
            os.makedirs(db_dump_folder)
            PrintMSG('Debug', 'util_db_dump', f'Adresár byl vytvořen....')
            log2file("INFO", 
                 "Adresár byl vytvořen....", 
                 db_log_file)
            
        # Pokud se vyskytne chyba loguj   
        except OSError as ex:
            PrintMSG('ERROR', 'util_db_dump', f'Adresár se nepodařilo vytvořit.... Chyba je: {ex}')
            log2file("ERROR", 
                 "Adresár se nepodařilo vytvořit.... Chyba je: " + ex, 
                 db_log_file)
        
# Zaloha databaze    
def run_database_backup():
    
    # Log do souboru
    PrintMSG('Debug', 'util_db_dump', f'Začíná záloha databáze...')
    log2file("INFO", 
             "Začíná záloha databáze...", 
             db_log_file)
    
    # Pripava zalohovaciho commandu
    command = [
        mysql_dir + 'mysqldump',
        '--user=' + mysql_username,
        '--password=' + mysql_password,
        '--host=' + mysql_host,
        '--databases',
        database_schema_name,
        '--single-transaction',
        '--routines',
        '--events',
]

    # Log do souboru
    PrintMSG('Debug', 'util_db_dump', f'Byl připraven command pro spuštění zálohy do souboru {db_dumb_file}! Dále se bude už zálohovat DB...')
    log2file("INFO", 
             "Byl připraven command pro spuštění zálohy do souboru " + db_dumb_file + "! Dále se bude už zálohovat DB...", 
             db_log_file)
    
    # Kontrola jestli existuje adresar DB_Backup
    check_directory()

    # Spusteni podprocesu pro vytvoreni dumpu
    with open(db_dump_folder + "\\" + db_dumb_file, 'w') as dump:
        try:
            
            # Spusteni procesu
            subprocess.run(command, stdout=dump, stderr=subprocess.PIPE, check=True)
            PrintMSG('Debug', 'util_db_dump', f'Záloha se úspěšně provedla do souboru: {db_dumb_file}')
            
            # Log do souboru
            PrintMSG('Debug', 'util_db_dump', f'Záloha databáze byla úspěšně vytvořena! A byla uložena do {db_dump_folder}\\{db_dumb_file}')
            log2file("INFO", 
                     "Záloha databáze byla úspěšně vytvořena! A byla uložena do " + db_dump_folder + "\\" + db_dumb_file, 
                     db_log_file)

        # Zachyceni chyby     
        except subprocess.CalledProcessError as ex:
            
            # Nastala chyba pri zalohovani
            PrintMSG('Debug', 'util_db_dump', f'Nastala chyba pri vytvareni zalohy: {ex.stderr.decode()}')

            # Log do souboru
            log2file("ERROR", 
                     "Chyba při tvorbě zálohy databáze! Chyba byla: " + str(ex), 
                     db_log_file)
            
            raise Exception("DBUTIL_1 - Nepovedlo se vytvořit zálohu DB")

# Zazipovani souboru           
def zip_backup_file():
    try:
        # Log do souboru
        PrintMSG('Debug', 'util_db_dump', f'Zacina ZIPovani souboru')
        log2file("INFO", 
                 "Začíná zipování backup souboru", 
                 db_log_file)
        
        # Zacatek zipovani
        with zipfile.ZipFile(db_dump_folder + "\\" + zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(db_dump_folder + "\\" + db_dumb_file, os.path.basename(db_dumb_file))

        # Log do souboru
        PrintMSG('Debug', 'util_db_dump', f'ZIPovani souboru uspesne dokonceno!')
        log2file("INFO", 
                 "ZIPování backupu DB bylo úspěšně dokončeno!", 
                 db_log_file)

    except zipfile.BadZipfile as ex:
        # Log do souboru
        PrintMSG('Debug', 'util_db_dump', f'Chyba pri ZIPovani souboru {str(ex)}')
        log2file("ERROR", 
                 "Nastala chyba při ZIPování souboru... Chyba byla: " +str(ex), 
                 db_log_file)
        
# Odmazani souboru pokud vse dobehne
def del_sql_file():

    # Log do souboru 
    PrintMSG('Debug', 'util_db_dump', f'Začíná smazaní souboru .SQL')
    log2file("INFO", 
             "Začíná smazaní souboru .sql", 
             db_log_file)
    
    # Kontrola 
    if os.path.exists(db_dump_folder + "\\" + db_dumb_file):
        os.remove(db_dump_folder + "\\" + db_dumb_file)
        
        # Log do souboru 
        PrintMSG('Debug', 'util_db_dump', f'Soubor se zalohou .SQL byl smazan')
        log2file("INFO", 
             "Soubor se zalohou .sql byl úspěšně smazán", 
             db_log_file)
        
# Odmazani starych zaloh vice jak specifikovane mnozstvi
def del_old_dumps(days: int):
    # Log do souboru 
    PrintMSG('Debug', 'util_db_dump', f'Budu mazat zálohy co jsou starsi jak {days} dnu')
    log2file("INFO", 
            f"Budu mazat zálohy co jsou starsi jak {days} dnu", 
            db_log_file)
    
    # Pomocna promenna 
    Dumb_Files = {}
    
    # Ulozim si vsechny soubory do dictionary
    for file in os.listdir(db_dump_folder):
        
        # Kontrola jestli se jedna o soubor
        file_path = f'{db_dump_folder}\\{file}'
        if os.path.isfile(file_path):
            
            # Ulozeni do objektu
            BackUP_Files = Dumb_File(
                file_name = file,
                file_created = datetime.fromtimestamp(os.path.getctime(file_path)),
                file_size = os.path.getsize(file_path),
                file_size_kb = round(os.path.getsize(file_path) / 1024, 2),
                file_extension = os.path.splitext(file_path)[1],
                file_location = file_path
            )
            
            # Ulozim si je do dict
            Dumb_Files[BackUP_Files.file_name] = BackUP_Files

    # Projdu soubory a smazu ty ktere jsou vytvorene dele jak stanovena doba
    date_to_check = datetime.now() - timedelta(days=days)
    
    for file_name, file_data in Dumb_Files.items():
        # provedu kontrolu jestli soubory jsou starsi jak nastavene datum
        if file_data.file_created < date_to_check:
            # pokud jsou smazu je 
            PrintMSG('Debug', 'util_db_dump', f'Mazu zalohu {file_name}, ktera je  starsi jak 14 dnu....')
            log2file("INFO", 
                    f"Zaloha {file_name} starsi jak 14 dnu byla smazana...", 
                    db_log_file)
            
            # Smazani souboru
            os.remove(file_data.file_location)
            
    # Log do souboru 
    PrintMSG('Debug', 'util_db_dump', f'Zalohy starsi jak 14 dnu byly smazany')
    log2file("INFO", 
            f"Zalohy starsi jak 14 dnu byly smazany", 
            db_log_file)

# Spusteni programu    
def Start_DB_Dump():
    
    if check_db_connection(): 

        # Log do souboru 
        PrintMSG('Info', 'util_db_dump', f'Zacina script pro vytvoreni zalohy DB...')
        log2file("INFO", 
                "########################################################################", 
                db_log_file)

        # Spusteni zalohy
        run_database_backup()

        # Spusteni zazipovani vytvoreneho backupu
        zip_backup_file()

        # Odmazani .sql souboru
        del_sql_file()
        
        # Smazani starsich zaloh jak 14 dnu
        del_old_dumps(days=14)

        # Log do souboru 
        PrintMSG('Info', 'util_db_dump', f'Konec zálohy DB. Ukončuji utiliku...')
        log2file("INFO", 
                "Konec zálohy DB. Ukončuji utiliku...", 
                db_log_file)
        
    print