from subprocess import run as os_run
from re import match as match_regex
from math import floor, log, pow
from datetime import datetime
import os

from pprint import pprint

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
    if path == "": return None
    os.startfile(path, 'open')

def showInExplorer(path):
    if path == "": return None
    os_run([
        os.path.join(os.getenv('WINDIR'), 'explorer.exe'),
        '/select,', os.path.normpath(path)
    ])

def isAccepted(event):
    if event.mimeData().hasUrls():
        paths = [f.toLocalFile() for f in event.mimeData().urls()]
        return paths[0] if all([os.path.isdir(p) for p in paths]) else 0
    return False

def find_nearest(n, d):
    for k, v in d.items():
        if n >= v: return k
    return None

def format_res(size, print_name = False):
    types = {'Ultra HD': 2160, 'Full HD': 1080, 'HD': 720, 'Poor': 1}
    names = {'12K+' : 6480, '10K' : 5760, '8K'  : 4320,
             '7K'   : 3780, '6K'  : 3240, '5K'  : 2700,
             '4K'   : 2160, '3K'  : 1620, '2K'  : 1440,
             '1080p': 1080, '720p': 720,  '480p': 480,
             '360p' : 360,  '240p': 240,  '144p': 144}

    if size[0] == 0 or size[1] == 0:
        return 'Zero'

    ratio, min_s = max(size) / min(size), min(size)
    if ratio > 4: return 'Thin'

    return find_nearest(min_s, types) + (f" {find_nearest(min_s, names)}" if print_name else "")
