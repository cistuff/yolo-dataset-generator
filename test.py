import os

file_path = r'C:\Users\maxsc\Downloads\pokemon-card-test-data'

file_path = os.fsencode(file_path)

file_path = os.fsdecode(file_path)

print(file_path)