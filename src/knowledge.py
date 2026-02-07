import os 

def load_knowledge_base():
    file_path = "knowledge_base/my_info.text"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: the knowledge Base file is missing. Please create 'knowledge_base/my_info.txt'."