import os
import re


for file_name in os.listdir(os.getcwd()):
    with open(file_name) as f:
        text = f.read()
        words = [w for w in text.split() if w.isalnum()]
        print(file_name, '-', len(words), 'words')
        
input('Press Enter to exit')
        