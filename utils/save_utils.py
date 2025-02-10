
import os
import json

def append_to_json_list(file, new_object):
    # Check if the file exists
    if not os.path.exists(file):
        # Initialize the file with an empty list
        with open(file, 'w') as f:
            f.write('[]')
    
    # Open the file in read+write mode
    with open(file, 'r+') as f:
        f.seek(0, os.SEEK_END)  # Go to the end of the file
        pos = f.tell() - 1      # Move one character back to find the closing bracket ']'
        
        # Move backward until a non-whitespace character is found
        while pos > 0:
            f.seek(pos, os.SEEK_SET)
            char = f.read(1)
            if char not in [' ', '\n', '\r']:
                break
            pos -= 1
        
        if char == ']':  # Valid closing bracket
            if pos > 1:  # File is not empty (contains objects)
                f.seek(pos, os.SEEK_SET)
                f.write(',\n')  # Add a comma and newline before the new object
            else:  # File is empty (only contains [])
                f.seek(pos, os.SEEK_SET)
        else:
            raise ValueError("Invalid JSON format in file.")
        