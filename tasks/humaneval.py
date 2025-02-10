import re
import os
import sympy
import pandas as pd
import json
from tasks.base import Task, DATA_PATH
from prompts.humaneval import * 
from fuzzywuzzy import fuzz
import jsonlines


import re

def extract_code_snippet(input_string):
    """
    Extracts the code block enclosed within <code> and </code> tags from a given string.

    Args:
        input_string (str): The string containing the code block.

    Returns:
        str: The extracted code block, or an empty string if no code block is found.
    """
    pattern = r"<code>(.*?)</code>"
    match = re.search(pattern, input_string, re.DOTALL)
    return match.group(1).strip() if match else ""

#unfinished 
class HumanEval(Task):
    """
    Input (x)   : A question comparing the number of people related to Genghis Khan and Julius Caesar
    Output (y)  : A logical reasoning process leading to the answer
    Reward (r)  : 0 or 1, depending on whether the reasoning is correct
    Input Example: 
        Are more people today related to Genghis Khan than Julius Caesar?
    Output Example: 
        1. Determine the descendants of Genghis Khan (many modern individuals have DNA traced to him).
        2. Determine the known descendants of Julius Caesar (limited, mainly historical).
        3. Compare the two numbers: Genghis Khan's descendants significantly outnumber Caesar's.
        Final Answer: Yes, more people today are related to Genghis Khan than to Julius Caesar.
    """   
    def __init__(self, file='HumanEval.jsonl'):
        super().__init__()
        path = os.path.join(DATA_PATH, 'humaneval', file)
        if not os.path.isfile(path):
            raise ValueError(f"File {file} not found at {path}")
        

        self.data = []
        self.ground_truth = []

        # 加载数据从 JSON 文件
        with open(path, 'r', encoding='utf-8') as f:
            # 读取文件中的每一行，并将其作为 JSON 解析
            for line in f:
                item = json.loads(line.strip())  # 解析每行的 JSON 数据
                question = item.get("prompt")
                answer = item.get("canonical_solution")

                # 将 question 和 answer 分别添加到对应的列表中
                self.data.append(question)
                self.ground_truth.append(answer)

        
        self.value_cache = {}
        self.steps = 3
        self.stops = ['.', '.', 'End of answer.']

    def __len__(self) -> int:
        return len(self.data)

    def get_input(self, idx: int) -> str:
        if idx >= len(self.data) or idx < 0:
            raise IndexError(f"Index {idx} out of bounds for data of length {len(self.data)}")
        return self.data[idx]

    def test_output(self, idx: int, output: str) -> dict:
        # if 'answer is' not in output.lower():
        #     print('====output====')
        #     print(output)
        #     return {'r': 0}

        # Ground truth
        ground_truth = self.ground_truth[idx]
   
        # 提取答案
        answer = self.extract_answer(output)


        print(f'====GR====\n:{ground_truth}====Extracted====\n:{answer}')


        return {'r': 0}

    def extract_answer(self, output: str) -> str:
        """
        尝试从输出中提取答案，支持多种格式，并处理换行符和其他格式问题。
        如果返回的代码较短，说明不是完整的代码，则返回空字符串。
        """

        # 提取代码片段
        code_snippet = extract_code_snippet(output)

        # 判断代码片段长度是否足够完整
        if len(code_snippet) < 10:  # 这里的长度阈值可以根据需要调整
            return ""

        return code_snippet


    @staticmethod
    def standard_prompt_wrap(x: str, y: str = '') -> str:
        return standard_prompt.format(input=x) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y: str = '') -> str:
        return cot_prompt.format(input=x) + y

    @staticmethod
    def reflect_cot_prompt_wrap(x: str, y: str = '') -> str:
        return reflect_cot_prompt.format(input=x) + y
        
    @staticmethod
    def agent_cot_prompt_wrap(x: str, y: str = '', step: int = 1,knowledge: str = '') -> str:
        if step > 1:
            return agent_cot_prompt.format(input=x) + '\n' + y + "End of step." + "\nShared information: "+ knowledge
        else:
            return agent_cot_prompt.format(input=x) + '\n' + y + "End of step."

    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        if 'the final answer is' not in y.lower():
            return value_evaluate + x + '\nThought Process: ' + y + '\nEvaluation Process:\n'
        else:
            return final_evaluate + x + '\n' + y + '\nEvaluation Process: \n'
    @staticmethod
    def self_process_value_prompt_wrap(x: str, y: str) -> str:
        return value_evaluate + x + '\nThought Process: ' + y + '\nEvaluation Process:\n'

    @staticmethod
    def self_result_value_prompt_wrap(x: str, y: str) -> str:
        return final_evaluate + x + '\nSo the final answer is:' + y + '\nEvaluation Process: \n'  
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        # Value map for scoring with probabilities between 0 and 1
        value_map = {'Impossible': 0.0, 'Likely': 0.5, 'Sure': 1.0}
        
        # Extract value_names using regex to match the words Sure, Impossible, Likely
        value_names = []
        for entry in value_outputs:
            # Find all occurrences of 'Sure', 'Impossible', or 'Likely' using regex
            matches = re.findall(r'\b(Sure|Impossible|Likely)\b', entry, re.IGNORECASE)
            # Normalize the matches to match the keys in value_map
            value_names.extend([match.capitalize() for match in matches])
        
        # If no matches were found, return 0
        if not value_names:
            return 0.0
        
        # Calculate the total value based on the occurrences of 'Impossible', 'Likely', and 'Sure'
        total_score = 0.0
        count = 0
        for name in value_names:
            if name in value_map:
                total_score += value_map[name]
                count += 1
        
        # Return the average score
        if count == 0:
            return 0.0
        average_score = total_score / count
        return average_score
