import datetime
import os
import subprocess
import mysql.connector
from Settings import mysql_host, mysql_username, mysql_password
from Utilities.utils_main import log2file
import zipfile

# ---------------------------------------------
# Utilitka pro vytvoreni dump souboru databaze
# ---------------------------------------------

# Promenne 
timestamp = datetime.datetime.today()
db_dump_folder = "C:\\DecinkaApp\\DB_Backup"
db_dumb_file = "DecinkaDB_backup_" + timestamp.strftime("%Y%m%d_%H%M%S") + ".sql"
db_log_file = "database_dump_log"
zip_file = "DecinkaDB_backup_" + timestamp.strftime("%Y%m%d_%H%M%S") + ".zip"
mysql_dir = "C:\\Program Files\\MySQL\\MySQL Workbench 8.0\\"
database_schema_name = "vinarnadzakaznici"

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
        log2file("INFO", 
                 "Úspěšné připojení do databáze! Mohu pokračovat s dumpem databáze...", 
                 db_log_file)
        connection.close()

        # Vratim status true ze jsem se pripojil
        return True

    # Pokud nastane chyba zaloguju
    except mysql.connector.Error as ex:

        # Vypisu chybu + ji zaloguju do souboru
        print("Chyba při připojení do DB!" + ex)
        log2file("ERROR", 
                 "Chyba při připojení do DB! Nemohu pokračovat s dumpem databáze... MySQL Chyba: " + str(ex), 
                 db_log_file)

        # Vratim false, ze jsem se nepripojil
        return False

# Kontrola jestli existuje adresar  
def check_directory():
    print("Kontroluji jestli existuje adresar DB_Backup...")

    if(os.path.exists(db_dump_folder)):
        
        # Vypis do logu
        print("Adresar " + db_dump_folder + " existuje a tak ukoncuji kontrolu adresare...")
        log2file("INFO", 
                 "Adresar " + db_dump_folder + " existuje a tak ukoncuji kontrolu adresare...", 
                 db_log_file)
        return
    
    else: 
        # Vypis do logu
        print("Adresar neni na disku... Bude vytvoren.")
        log2file("INFO", 
                 "Adresář není na disku... Bude vytvořen.", 
                 db_log_file)
        
        # Vytvoreni adresare + log do souboru
        try:
            os.makedirs(db_dump_folder)
            log2file("INFO", 
                 "Adresár byl vytvořen....", 
                 db_log_file)
            
        # Pokud se vyskytne chyba loguj   
        except OSError as ex:
            log2file("ERROR", 
                 "Adresár se nepodařilo vytvořit.... Chyba je: " + ex, 
                 db_log_file)
        
# Zaloha databaze    
def run_database_backup():
    
    # Log do souboru
    log2file("INFO", 
             "Začíná záloha databáze...", 
             db_log_file)
    
    # Priprava prikazu pro vytvoreni zalohy
    command = [
        mysql_dir +
        'mysqldump',
        '--user=' + mysql_username,
        '--password=' + mysql_password,
        '--host=' + mysql_host,
        '--all-databases',
        '--single-transaction',
        '--routines',
        '--events'
    ]
    
    command = [
        mysql_dir + 'mysqldump',
        '--user=' + mysql_username,
        '--password=' + mysql_password,
        '--host=' + mysql_host,
        '--databases',  # This is optional but good for clarity
        database_schema_name,
        '--single-transaction',
        '--routines',
        '--events',
]

    # Log do souboru
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
            print("Záloha se úspěšně provedla do souboru: "+ db_dumb_file)
            
            # Log do souboru
            log2file("INFO", 
                     "Záloha databáze byla úspěšně vytvořena! A byla uložena do " + db_dump_folder + "\\" + db_dumb_file, 
                     db_log_file)

        # Zachyceni chyby     
        except subprocess.CalledProcessError as ex:
            
            # Nastala chyba pri zalohovani
            print("Nastala chyba pri vytvareni zalohy: " + ex.stderr.decode())

            # Log do souboru
            log2file("ERROR", 
                     "Chyba při tvorbě zálohy databáze! Chyba byla: " + str(ex), 
                     db_log_file)
            
            raise Exception("DBUTIL_1 - Nepovedlo se vytvořit zálohu DB")

# Zazipovani souboru           
def zip_backup_file():
    try:
        # Log do souboru
        print("Zacina ZIPovani souboru") 
        log2file("INFO", 
                 "Začíná zipování backup souboru", 
                 db_log_file)
        
        # Zacatek zipovani
        with zipfile.ZipFile(db_dump_folder + "\\" + zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(db_dump_folder + "\\" + db_dumb_file, os.path.basename(db_dumb_file))

        # Log do souboru
        print("ZIPovani souboru uspesne dokonceno!") 
        log2file("INFO", 
                 "ZIPování backupu DB bylo úspěšně dokončeno!", 
                 db_log_file)

    except zipfile.BadZipfile as ex:
        # Log do souboru
        print("Chyba pri ZIPovani souboru " + str(ex))
        log2file("ERROR", 
                 "Nastala chyba při ZIPování souboru... Chyba byla: " +str(ex), 
                 db_log_file)
        
# Odmazani souboru pokud vse dobehne
def del_sql_file():

    # Log do souboru 
    log2file("INFO", 
             "Začíná smazaní souboru .sql", 
             db_log_file)
    
    # Kontrola 
    if os.path.exists(db_dump_folder + "\\" + db_dumb_file):
        os.remove(db_dump_folder + "\\" + db_dumb_file)
        
        # Log do souboru 
        print("Soubor se zalohou .sql byl smazan")
        log2file("INFO", 
             "Soubor se zalohou .sql byl úspěšně smazán", 
             db_log_file)

# Spusteni programu    
def main():
    if check_db_connection(): 

        # Log do souboru 
        log2file("INFO", 
                "########################################################################", 
                db_log_file)

        # Spusteni zalohy
        run_database_backup()

        # Spusteni zazipovani vytvoreneho backupu
        zip_backup_file()

        # Odmazani .sql souboru
        del_sql_file()

        # Log do souboru 
        print("Konec zálohy DB. Ukončuji utiliku...")
        log2file("INFO", 
                "Konec zálohy DB. Ukončuji utiliku...", 
                db_log_file)