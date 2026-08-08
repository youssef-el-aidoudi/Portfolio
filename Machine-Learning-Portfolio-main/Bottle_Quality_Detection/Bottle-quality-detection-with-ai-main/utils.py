import os
import json

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_class_names(class_names, filepath="models/class_names.json"):
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)
