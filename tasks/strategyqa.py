import re
import os
import sympy
import pandas as pd
import json
from tasks.base import Task, DATA_PATH
from prompts.strategyqa import * 
from fuzzywuzzy import fuzz




class StrategyQA(Task):
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
    def __init__(self, file='StrategyQA.json'):
        super().__init__()
        path = os.path.join(DATA_PATH, 'StrategyQA', file)
        if not os.path.isfile(path):
            raise ValueError(f"File {file} not found at {path}")
        

        # 初始化 self.data 和 self.ground_truth 为空列表
        self.data = []
        self.ground_truth = []

        # 从 JSON 文件中读取数据并将 q 和 a 添加到 self.data 和 self.ground_truth
        with open(path) as f:
            json_data = json.load(f)["examples"]
            for idx, line in enumerate(json_data):
                q = line["input"].strip()
                a = int(line["target_scores"]["Yes"])
                # 转换 a 的值
                a = "yes" if a == 1 else "no"
                
                # 添加到 self.data 和 self.ground_truth
                self.data.append(q)  # 将 q 添加到 self.data
                self.ground_truth.append(a)  # 将 a 添加到 self.ground_truth


        
        self.value_cache = {}
        self.steps = 3
        self.stops = ['.', '.', 'Question']

    def __len__(self) -> int:
        return len(self.data)

    def get_input(self, idx: int) -> str:
        if idx >= len(self.data) or idx < 0:
            raise IndexError(f"Index {idx} out of bounds for data of length {len(self.data)}")
        return self.data[idx]

    def test_output(self, idx: int, output: str):
        # 检查输出是否包含 'answer is'，如果没有则返回0
        if 'answer is' not in output.lower():
            print('====output====')
            print(output)
            return {'r': 0}
        
        # 尝试从输出中提取最终答案
        expression = self.extract_answer(output)
        expression = expression.replace(': ', '').strip()
        ground_truth = str(self.ground_truth[idx])

        # 打印对比信息
        print(f'====GR===={ground_truth}====Pre===={expression}')
        
        # 直接比较 ground_truth 和提取的 expression
        if ground_truth in expression:
            return {'r': 1}
        else:
            # 处理格式化问题，例如去除标点符号等
            expression_ = re.sub(r'\W+', '', expression, flags=re.IGNORECASE)
            ground_truth_ = re.sub(r'\W+', '', ground_truth, flags=re.IGNORECASE)
            
            # 正则表达式匹配去掉非字母数字字符后的表达式
            if re.search(ground_truth_, expression_, re.IGNORECASE):
                return {'r': 1}
            else:
                # 模糊匹配，使用fuzzywuzzy库
                similarity = fuzz.ratio(expression_, ground_truth_)
                if similarity > 95:  # 设置合理的相似度阈值
                    return {'r': 1}
                
                # 如果仍然不匹配，则使用部分匹配策略
                ground_truth_parts = ground_truth.split(' ')
                flag = any(re.search(part, expression, re.IGNORECASE) for part in ground_truth_parts)
                return {'r': 1} if flag else {'r': 0}

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