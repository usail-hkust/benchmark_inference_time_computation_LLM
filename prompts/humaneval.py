standard_prompt = """
Task:  
For each given Question:  
1. Answer the question, and end the final output with 'so the final answer is:' and then the final answer. 
4. Ensure the final output includes only the complete code wrapped within `<code>` tags. Do not include any explanatory text, instructions, or comments outside the code solution within the `<code>` tags.  
  

Question:  
\"\"\"
from typing import List

def filter_even(numbers: List[int]) -> List[int]:  
    \"\"\"Return a list containing only the even numbers from the input.\"\"\"
    # fill in the code  
\"\"\"

Answer:   
so the final answer is:  
<code>  
from typing import List

def filter_even(numbers: List[int]) -> List[int]:  
    \"\"\"Return a list containing only the even numbers from the input.\"\"\"  
    return [n for n in numbers if n % 2 == 0]  
</code>  
End of answer.  


Question:  
\"\"\"  
from typing import List

def find_max(numbers: List[int]) -> int:  
    \"\"\"Return the largest number from the list.\"\"\"  
    # fill in the code  
\"\"\"

Answer:  
so the final answer is:  
<code>  
from typing import List

def find_max(numbers: List[int]) -> int:  
    \"\"\"Return the largest number from the list.\"\"\"  
    return max(numbers)  
</code>  
End of answer.


Question:  
\"\"\"
from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:  
    \"\"\"Check if in the given list of numbers, any two numbers are closer to each other than  
    the given threshold.  
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)  
    False  
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)  
    True  
    \"\"\"  
    # fill in the code  
\"\"\"

Answer:  
so the final answer is:  
<code>  
from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:  
    \"\"\"Check if in the given list of numbers, any two numbers are closer to each other than  
    the given threshold.  
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)  
    False  
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)  
    True  
    \"\"\"  
    for idx, elem in enumerate(numbers):  
        for idx2, elem2 in enumerate(numbers):  
            if idx != idx2:  
                distance = abs(elem - elem2)  
                if distance < threshold:  
                    return True  
    return False  
</code>  
End of answer.  

Question: {input}  
"""




cot_prompt = """
Task:  
For each given Question:  
1. First think step-by-step about how to arrive at the final Answer.  
2. Then produce the Answer. The reasoning steps should not appear in the final answer; they are just for the model's internal reasoning.  
3. End the final output with 'so the final answer is:' and then the final answer. 
4. Ensure the final output includes only the complete code wrapped within `<code>` tags. Do not include any explanatory text, instructions, or comments outside the code solution within the `<code>` tags.  
  

Question:  
\"\"\"
from typing import List

def filter_even(numbers: List[int]) -> List[int]:  
    \"\"\"Return a list containing only the even numbers from the input.\"\"\"
    # fill in the code  
\"\"\"

Answer:  
Step 1: We need to filter out the even numbers from the input list.  
Step 2: Use a list comprehension to check if each number is divisible by 2.  
so the final answer is:  
<code>  
from typing import List

def filter_even(numbers: List[int]) -> List[int]:  
    \"\"\"Return a list containing only the even numbers from the input.\"\"\"  
    return [n for n in numbers if n % 2 == 0]  
</code>  
End of answer.  


Question:  
\"\"\"  
from typing import List

def find_max(numbers: List[int]) -> int:  
    \"\"\"Return the largest number from the list.\"\"\"  
    # fill in the code  
\"\"\"

Answer:  
Step 1: We need to find the maximum number in the list.  
Step 2: Initially, I thought to write a custom loop to find the largest number manually. However, on closer inspection, I realized that Python provides a built-in function `max()` which is optimized for this purpose.  
so the final answer is:  
<code>  
from typing import List

def find_max(numbers: List[int]) -> int:  
    \"\"\"Return the largest number from the list.\"\"\"  
    return max(numbers)  
</code>  
End of answer.


Question:  
\"\"\"
from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:  
    \"\"\"Check if in the given list of numbers, any two numbers are closer to each other than  
    the given threshold.  
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)  
    False  
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)  
    True  
    \"\"\"  
    # fill in the code  
\"\"\"

Answer:  
Step 1: We need to compare each number with every other number in the list.  
Step 2: If the absolute difference between any two numbers is less than the threshold, return `True`.  
Step 3: If no such pair is found after comparing all, return `False`.  
so the final answer is:  
<code>  
from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:  
    \"\"\"Check if in the given list of numbers, any two numbers are closer to each other than  
    the given threshold.  
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)  
    False  
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)  
    True  
    \"\"\"  
    for idx, elem in enumerate(numbers):  
        for idx2, elem2 in enumerate(numbers):  
            if idx != idx2:  
                distance = abs(elem - elem2)  
                if distance < threshold:  
                    return True  
    return False  
</code>  
End of answer.  

Question: {input}  
"""


reflect_cot_prompt = """
Task:  
For each given Question:  
1. First think step-by-step about how to arrive at the final Answer.  
2. Then produce the Answer. The reasoning steps should not appear in the final answer; they are just for the model's internal reasoning.  
3. End the final output with 'so the final answer is:' and then the final answer.  
4. Ensure that each step is followed by a "Reflection:" line, considering the accuracy and reliability of the process. 
5. Ensure the final output includes only the complete code wrapped within `<code>` tags. Do not include any explanatory text, instructions, or comments outside the code solution within the `<code>` tags.  
  

Question:  
\"\"\"
from typing import List

def filter_even(numbers: List[int]) -> List[int]:  
    \"\"\"Return a list containing only the even numbers from the input.\"\"\"
    # fill in the code  
\"\"\"

Answer:  
Step 1: We need to filter out the even numbers from the input list.  
Reflection: This step is clear, as the task specifies filtering for even numbers, which is a straightforward requirement.  

Step 2: Use a list comprehension to check if each number is divisible by 2.  
Reflection: A list comprehension is the most efficient and concise way to achieve this, making the code easier to read and maintain.  
 
so the final answer is:  
<code>  
from typing import List

def filter_even(numbers: List[int]) -> List[int]:  
    \"\"\"Return a list containing only the even numbers from the input.\"\"\"  
    return [n for n in numbers if n % 2 == 0]  
</code>  
End of answer.  

Question:  
\"\"\"  
from typing import List

def find_max(numbers: List[int]) -> int:  
    \"\"\"Return the largest number from the list.\"\"\"  
    # fill in the code  
\"\"\"

Answer:  
Step 1: We need to find the maximum number in the list.  
Reflection: Initially, I thought to write a custom loop to find the largest number manually. However, on closer inspection, I realized that Python provides a built-in function `max()` which is optimized for this purpose.  
so the final answer is:  
<code>  
from typing import List

def find_max(numbers: List[int]) -> int:  
    \"\"\"Return the largest number from the list.\"\"\"  
    return max(numbers)  
</code>  
End of answer.



Question:  
\"\"\"
from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:  
    \"\"\"Check if in the given list of numbers, any two numbers are closer to each other than  
    the given threshold.  
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)  
    False  
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)  
    True  
    \"\"\"  
    # fill in the code  
\"\"\"

Answer:  
Step 1: We need to compare each number with every other number in the list.  
Reflection: This is necessary because we need to identify pairs of numbers, so a pairwise comparison is the only approach to solve this problem.

Step 2: If the absolute difference between any two numbers is less than the threshold, return `True`.  
Reflection: This condition is the core of the logic; it ensures we identify if two numbers are "close enough" by the given threshold.

Step 3: If no such pair is found after comparing all, return `False`.  
Reflection: This is the fallback condition. If no close elements are found, we return `False`, ensuring the function behaves as expected.
 
so the final answer is:  
<code>  
from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:  
    \"\"\"Check if in the given list of numbers, any two numbers are closer to each other than  
    the given threshold.  
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)  
    False  
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)  
    True  
    \"\"\"  
    for idx, elem in enumerate(numbers):  
        for idx2, elem2 in enumerate(numbers):  
            if idx != idx2:  
                distance = abs(elem - elem2)  
                if distance < threshold:  
                    return True  
    return False  
</code>  
End of answer.  

Question: {input}  
"""



value_evaluate = '''Evaluate whether the language model can effectively decompose the question into relevant sub-questions, and assess whether this decomposition helps in partially or directly answering the original question. The outcome will determine if this process of decomposition is "Sure," "Likely," or "Impossible" to aid in finding the answer.

Evaluation Steps:
1. Check if the language model can identify and decompose key sub-questions that are directly related to the original question.

Evaluation Process:
1. Analyze whether each sub-question identified by the model is directly relevant to the answer to the original question.
2. Determine if the decomposition of these sub-questions forms a reasonable response to the original question.

Evaluation Result:
1. Sure: If the language model not only successfully decomposes the original question into relevant sub-questions but also ensures that each sub-question is optimally structured to construct a comprehensive and accurate final answer.
2. Likely: If the language model successfully decomposes the original question into relevant sub-questions that help construct the final answer, but there might be minor areas for improvement in structure or relevance.
3. Impossible: If the language model fails to effectively decompose the question, or if the decomposed sub-questions are not directly relevant to finding the answer.

Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?
Thought Process: Step 1: Natalia sold 48 / 2 = 24 clips in May. Step 2: Natalia sold 48 + 24 = 72 clips altogether in April and May. Step 3: So the final answer is: 72.
Evaluation Process:
Relevance of Sub-Questions: Sub-question 1: How many clips did Natalia sell in May?
Relevance: Directly relevant to answering the original question, as this step calculates the number of clips sold in May. Sub-question 2: How many clips did Natalia sell in total in April and May? Relevance: Directly relevant as it adds the number of clips sold in April and May to find the final answer. Effectiveness of Decomposition: The sub-questions effectively break down the original question into logical parts that help construct the complete answer. By calculating the number of clips sold in May and adding it to the number sold in April, the original question is comprehensively addressed.
Evaluation Result: Sure
End of answer.


Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?
Thought Process: Step 1, natalia sold 48 / 2 = 24 clips in May. Step 2: Natalia sold 48 + 24 = 72 clips altogether in April and May.  Step 3: so the final answer is: 72.
Evaluation Process:
Relevance of Sub-Questions: Sub-question 1: How many clips did Natalia sell in May? Relevance: Directly relevant to answering the original question, as this step calculates the number of clips sold in May. Sub-question 2: How many clips did Natalia sell in total in April and May? Relevance: Directly relevant as it adds the number of clips sold in April and May to find the final answer
Effectiveness of Decomposition: The sub-questions effectively break down the original question into logical parts that help construct the complete answer. By calculating the number of clips sold in May and adding it to the number sold in April, the original question is comprehensively addressed.
Evaluation Result: Likely
End of answer.

Question: How much did Weng earn for 50 minutes of babysitting at $12 an hour?
Thought Process: Step 1: Weng earns $12 an hour for babysitting. Step 2: Yesterday, she babysat for 50 minutes. Step 3: Therefore, she earned $12 for that time.
Evaluation Process: 
Relevance of Sub-Questions: Sub-question 1: How much does Weng earn per hour? Relevance: This is known information and does not help in calculating earnings for the specific time period. Sub-question 2: How long did Weng babysit yesterday? Relevance: While it provides context, it doesn't lead to a calculation that answers the original question.
Effectiveness of Decomposition: The thought process fails to effectively break down the original question into useful sub-questions. The steps do not include any calculations for earnings per minute or total earnings for the 50 minutes, which is essential to answer the question correctly.
Evaluation Result: Impossible
End of answer.

Question: What is the highest mountain in the world?
Thought Process: Step 1, identify the tallest mountains known globally. Mount Everest is commonly known as the highest mountain peak in the world.
Evaluation Process:
The thought process begins with identifying the tallest mountains known globally, which is a logical first step. Since Mount Everest is commonly known and recognized as the highest mountain peak in the world, this thought directly leads to the answer to the question. Therefore, this approach is very likely to help in answering the question correctly.
So, the evaluation result is: this thought is likely to help partially or directly answer the question.
Evaluation Results: Likely
End of answer.

Question: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet? 
Thought Process:  Step 1, in the beginning, Betty has only 100 / 2 = $50. Step 2, betty's grandparents gave her 15 * 2 = $30. This means, Betty needs 100 - 50 - 30 - 15 = $5 more. Step 3, so the final answer is: 5. 
Evaluation Process:
Relevance of Sub-Questions: Sub-question 1: How much money does Betty currently have? Relevance: Directly relevant, as it helps determine her current savings.Sub-question 2: How much did her parents and grandparents give her? Relevance: Directly relevant, as this affects the total amount she has. Sub-question 3: How much more money does Betty need to reach $100? Relevance: This is essential for answering the original question.
Effectiveness of Decomposition: The sub-questions effectively break down the original question into logical parts. However, there is a calculation error in the final step. Betty's total after receiving the gifts should be calculated as follows: $50 (her savings) + $15 (from parents) + $30 (from grandparents) = $95. Therefore, she needs $100 - $95 = $5 more.
Evaluation Result: Likely
End of answer.

Question: '''

final_evaluate = '''Evaluate if the given sentence can answer the question effectively using a three-tier evaluation system: "Sure," "Likely," or "Impossible."

Evaluation Criteria:
Sure: The provided sentence directly and accurately answers the question with clear and unambiguous information.
Likely: The provided sentence answers the question, but there may be minor ambiguities or lack of complete information.
Impossible: The provided sentence does not effectively answer the question or contains incorrect information.


Question: Are more people today related to Genghis Khan than Julius Caesar?
So the final answer is: yes.
Evaluation Process: The question is asking for a comparison of the number of descendants or related individuals between Genghis Khan and Julius Caesar. The provided answer, "yes," implies that more people today are related to Genghis Khan than to Julius Caesar, which can be supported by genetic studies.
Evaluation Results: Sure


Question: Would a Monoamine Oxidase candy bar cheer up a depressed friend?
So the final answer is: yes.
Evaluation Process:
The question asks whether a specific type of candy bar, described as "Monoamine Oxidase," can cheer up a depressed friend. The answer "yes" suggests that the candy bar would have a positive effect on mood. However, without scientific backing or clarification on what "Monoamine Oxidase" refers to in this context, it's unclear if the statement is valid.
Evaluation Results: Impossible
End of answer.

Question: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet?
So the final answer is: 5.
Evaluation Process:
1. The wallet costs $100. 2. Betty has half of that amount, which is $50. 3. Her parents give her $15, and her grandparents give her twice that, which is $30. 4. Total money Betty will have after the contributions: $50 (initial) + $15 (parents) + $30 (grandparents) = $95. 5. The remaining amount Betty needs: $100 (cost) - $95 (total) = $5.
Evaluation Results: Likely
End of answer.

Question: '''