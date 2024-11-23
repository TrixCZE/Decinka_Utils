"""
Decinka Utils Manager Launcher
----------------------
Utils Manager launcher is responsible for launching and executing usefull utilites for Decinka.

The script executes:
- Database Automatic Dump File Utility
- Vycetka Files Managment Utility
"""

# -----------------------------------------------------------
# Libraries
# -----------------------------------------------------------
import threading
from Scripts.util_db_dump import Start_DB_Dump
from Scripts.util_move_vycet import main as Start_Vycetka_Move

# Execution of utilites
if __name__ == "__main__":
    # Ending - Log
    print("[INFO] - Decinka Utils Manager Launcher is starting....")
    
    # Multithreading execution setup
    job1 = threading.Thread(target=Start_DB_Dump)
    job2 = threading.Thread(target=Start_Vycetka_Move)

    # Start execution
    job1.start()
    job2.start()
    
    # Wait for threads to complete
    job1.join()
    job2.join()

    # Ending - Log
    print("[INFO] - Decinka Utils Manager Launcher have been executed succesfully!")