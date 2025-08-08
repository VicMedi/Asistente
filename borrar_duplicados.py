import os
import hashlib

def hash_file(filename):
    hasher = hashlib.md5()
    with open(filename, "rb") as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(filename):
    hashes = {}
    duplicates = []
    for dirpath, _, filenames in os.walk(filename):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            file_hash = hash_file(full_path)
            if file_hash in hashes:
                duplicates.append((full_path, hashes[file_hash]))
            else:
                hashes[file_hash] = full_path
    return duplicates
def delete_file(filepath):
    try:
        os.remove(filepath)
        return True
    except Exception as e:
        return False