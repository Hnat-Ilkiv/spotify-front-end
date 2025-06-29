import os
import csv


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f"{num:3.1f} {unit}"
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)
    return 'File Error'

def lines_in_csv(csv_file_path):
    with open(csv_file_path, newline='') as file:
        reader = csv.reader(file)
        lines_in_csv = list(reader)
    return len(lines_in_csv)

