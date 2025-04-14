import csv
from typing import List, Dict

def write_to_csv(filename: str, data: List[Dict[str, str]], fieldnames: List[str]):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
