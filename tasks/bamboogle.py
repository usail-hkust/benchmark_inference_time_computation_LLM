import re
import os
import sympy
import pandas as pd
from tasks.base import Task, DATA_PATH
from prompts.bamboogle import * 
from fuzzywuzzy import fuzz

def get_current_numbers(y: str) -> str:
    last_line = y.strip().split('\n')[-1]
    return last_line.split('left: ')[-1].split(')')[0]


class Bamboogle(Task):
    def __init__(self, file='Bamboogle Prerelease - Sheet1.csv'):
        super().__init__()
        path = os.path.join(DATA_PATH, 'bamboogle', file)
        if not os.path.isfile(path):
            raise ValueError(f"File {file} not found at {path}")
        

                # 尝试不同的编码格式来避免 'utf-8' 解码错误
        try:
            self.data = list(pd.read_csv(path, encoding='utf-8')['Question'])
            self.ground_truth = list(pd.read_csv(path, encoding='utf-8')['Answer'])
        except UnicodeDecodeError:
            self.data = list(pd.read_csv(path, encoding='ISO-8859-1')['Question'])
            self.ground_truth = list(pd.read_csv(path, encoding='ISO-8859-1')['Answer'])
        
        # self.data = list(pd.read_csv(path)['Question'])
        # self.ground_truth = list(pd.read_csv(path)['Answer'])
        
        self.value_cache = {}
        self.steps = 3
        #self.stops = ['.', '.', 'Question']
        self.stops = ['.', '.', 'End of answer.']
        

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
        print(f'==== Ground Truth: {ground_truth} ====')
        print(f'==== Extracted Answer: {expression} ====')
        
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
        
        #print("before output", output, "\n")

        # 检查 'Question:' 是否出现在句首
        if output.lower().startswith('question:'):
            # 如果 'Question:' 在句首，检查后续是否有第二个 'Question:'
            second_question_index = output.lower().find('question:', len('question:'))
            if second_question_index != -1:
                # 如果有第二个 'Question:'，删除其后的内容
                output = output[:second_question_index].strip()
        else:
            # 如果 'Question:' 出现在其他位置，则删除其后的内容
            question_index = output.lower().find('question:')
            if question_index > -1:
                output = output[:question_index].strip()

        #print("after output", output, "\n")

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
            return wiki_evaluate + x + '\nThought Process: ' + y + '\nEvaluation Process:\n'
        else:
            if 'choose the best answer' in x.lower():
                return choose_evaluate + x + '\nAnswer: ' + y.lower().split('the final answer is')[1].replace(': ', '') + '\nEvaluation Process:\n'
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

        print("\n===== Value Outputs =====")
        for i, value_output in enumerate(value_outputs):
            print(f"Output {i + 1}: {value_output}")
        print("=========================\n")
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