import re
import os
import sympy
import pandas as pd
import json
from tasks.base import Task, DATA_PATH
from prompts.gsm8k import * 
from fuzzywuzzy import fuzz
import jsonlines

#unfinished 
class MATH(Task):
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
    def __init__(self, file='gsm8k_perturbed.json'):
        super().__init__()
        path = os.path.join(DATA_PATH, 'gsm8k', file)
        if not os.path.isfile(path):
            raise ValueError(f"File {file} not found at {path}")
        

        # 初始化 self.data 和 self.ground_truth 为空列表
        self.data = []
        self.ground_truth = []

        # Load data from JSON file
        with open(path) as f:
            json_data = json.load(f)
            for item in json_data:
                question = item.get("question")
                answer = item.get("answer")
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
        ground_truth = float(self.ground_truth[idx])
        tolerance = 0.01

        # 提取答案
        expression = self.extract_answer(output).replace(': ', '').strip()

        # 使用改进的正则表达式提取数字
        extracted_numbers = re.findall(r'[-+]?\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+', expression)
        # 去掉千分位分隔符并转换为浮点数
        extracted_numbers = [float(num.replace(',', '')) for num in extracted_numbers]

        print(f'====GR===={ground_truth}====Extracted===={extracted_numbers}')

        # 比较提取的数字与 ground_truth
        for num in extracted_numbers:
            if abs(num - ground_truth) <= tolerance:
                return {'r': 1}

        return {'r': 0}

    def extract_answer(self, output: str) -> str:
        """
        尝试从输出中提取答案，支持多种格式，并处理换行符和其他格式问题。
        """
        output = output.replace('\n', ' ').strip()  # 移除换行符，并清除首尾的空格
        
        # 优先寻找 "the final answer is" 格式
        if 'the final answer is' in output.lower():
            return output.lower().split('the final answer is')[-1].strip().split('.')[0].strip()
        elif 'final answer' in output.lower():
            return output.lower().split('final answer')[-1].strip().split('.')[0].strip()
        elif 'final refined solution' in output.lower():
            return output.lower().split('final refined solution')[-1].strip().split('.')[0].strip()
        elif 'refined solution' in output.lower():
            return output.lower().split('refined solution')[-1].strip().split('.')[0].strip()
        else:
            # 如果没有明确的标记，则尝试返回最后一句话作为默认答案
            return output.strip().split('.')[-1].strip()

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
