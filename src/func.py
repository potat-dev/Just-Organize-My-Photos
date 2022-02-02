from math import floor, log, pow
from datetime import datetime
from re import match as match_regex
from subprocess import run as os_run
import os

def convert_size(size_bytes):
    if size_bytes == 0: return "0"
    i = int(floor(log(size_bytes, 1024)))
    s = round(size_bytes / pow(1024, i), 2)
    return f"{s} {('B','KB','MB','GB')[i]}"

def getModifyDate(path):
    ts = os.path.getmtime(path)
    return "Null" if ts < 0 else datetime.fromtimestamp(ts).strftime('%d.%m.%Y')

def smartRename(file):
    regex = r'(.+)_\((\d+)\)\.(.+)' # filename_(0).ext
    make_filename = lambda p: p[0] + f"_({p[1]})." + p[2]
    filename, path = os.path.basename(file), os.path.dirname(file)
    match = match_regex(regex, filename)
    parts = list(match.groups())[::2] if match else filename.split('.')
    parts.insert(1, int(match.group(2)) if match else 0)
    new_path = os.path.join(path, make_filename(parts))
    # ищем свободный индекс дубликата
    while os.path.exists(new_path):
        parts[1] += 1
        new_path = os.path.join(path, make_filename(parts))
    return new_path

def viewFile(path):
    if path == "": return Null
    os.startfile(path, 'open')

def showInExplorer(path):
    if path == "": return Null
    os_run([
        os.path.join(os.getenv('WINDIR'), 'explorer.exe'),
        '/select,', os.path.normpath(path)
    ])

