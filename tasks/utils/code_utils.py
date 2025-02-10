import json
import os
import re

def extract_code_snippet(input_string):
    """
    Extracts the code block enclosed within <code> and </code> tags from a given string.
    """
    pattern = r"<code>(.*?)</code>"
    match = re.search(pattern, input_string, re.DOTALL)
    return match.group(1).strip() if match else ""

def load_jsonl(input_path):
    """
    Loads a JSONL file and returns a list of parsed JSON objects.
    """
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def save_jsonl(output_path, data):
    """
    Saves a list of dictionaries to a JSONL file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def process_code_test(completation_file, prompt_file, output_file):
    """
    Processes completion and prompt JSON files, extracts relevant information, 
    and saves the results into a new JSONL file.
    """
    # Load completion and prompt data
    with open(completation_file, 'r', encoding='utf-8') as f:
        completation_data = json.load(f)

   
    prompt_data = load_jsonl(prompt_file)
    print("prompt data:", prompt_data)
    # Initialize result list
    results = []

    # Iterate through prompt data and match with completation data
    for i, prompt_item in enumerate(prompt_data):
        task_id = prompt_item.get('task_id')
        
        # Ensure completation_data[i] exists and has the correct structure
        if i < len(completation_data):
            completation_item = completation_data[i]
            completion = completation_item.get("ys", [""])[0]  # Default to empty string if missing
            completion = extract_code_snippet(completion)  # Extract code from completion string

            # Append result
            results.append({"task_id": task_id, "completion": completion})
        else:
            print(f"Warning: No corresponding completion for task_id {task_id}")

    # Save the results to output file
    save_jsonl(output_file, results)
    print(f"Saved {len(results)} results to {output_file}")
