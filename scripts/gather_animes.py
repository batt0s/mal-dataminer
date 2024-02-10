from mal import anime
import csv
import sys
import os

def continue_id(csv_file: str) -> int:
   with open(csv_file, "r", newline='', encoding="utf-8") as csvfile:
       reader = csv.DictReader(csvfile)
       rows = list(reader)
       if rows is None:
           return
       last_row = rows[-1]
       return last_row['id']

def main() -> int:
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        newfile = True
    else:
        newfile = False
    start_id = sys.argv[2]
    stop_id = sys.argv[3]
    if start_id == "continue":
        start_id = continue_id(filepath)
    anime.gather_animes_and_write_to_csv(csv_file=filepath,
                                         start_id=int(start_id),
                                         stop_id=int(stop_id),
                                         new_file=newfile)
    return 0

if __name__ == "__main__":
    main()