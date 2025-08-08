import os
import shutil

def organize_folder(folder):
    files_type = {
        'Imagenes': ['.jpeg', '.jpg', '.png', '.gif'],
        'Video': ['.mov', '.mp4', 'mkv', 'avi'],
        'Audio': ['.mp3', '.wav', '.aiff'],
        'Documentos': ['.pdf', '.doc', '.docx'],
        'Excel': ['.xlsx', '.xls', '.xlsm'],
        'Comprimidos': ['.zip', '.rar'],
        'Ejecutables': ['.exe', '.bat'],
    }

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            for folder_name, extensions in files_type.items():
                if ext in extensions:
                    target_folder = os.path.join(folder, folder_name)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_folder, filename))
                    print(f"Moving {filename} to {target_folder}")
