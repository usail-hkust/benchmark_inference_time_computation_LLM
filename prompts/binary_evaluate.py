
binary_evaluate = '''\
Evaluate whether the language model can effectively decompose the question into relevant sub-questions, determine if this decomposition aids in partially or directly answering the original question, assess the correctness of the thought process, and verify if the final answer accurately answers the question. The evaluation result should be either "Yes" or "No."

**Evaluation Steps:**
1. Verify if the language model identifies and breaks down the original question into key sub-questions that are directly related to answering it.

**Evaluation Process:**
1. **Relevance of Sub-Questions:**
    - Assess whether each sub-question identified by the model is directly pertinent to solving the original question.
2. **Effectiveness of Decomposition:**
    - Determine if the breakdown of the original question into sub-questions logically contributes to constructing a complete and accurate answer.
3. **Correctness of Thought Process:**
    - Check if the model's thought process is logically sound and correctly leads to the final answer.
4. **Correctness of Final Answer:**
    - Verify if the final answer provided by the model accurately and correctly answers the original question.

**Evaluation Criteria:**
- **Yes:**
    - If the language model successfully decomposes the original question into relevant and appropriately structured sub-questions, the thought process is logically correct, and the final answer accurately answers the question.
- **No:**
    - If the language model fails to effectively decompose the question, the sub-questions are irrelevant, the thought process contains logical errors, or the final answer is incorrect.


Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?
Thought Process: Step 1: Natalia sold 48 / 2 = 24 clips in May. Step 2: Natalia sold 48 + 24 = 72 clips altogether in April and May. Step 3: So the final answer is: 72.
Evaluation Process:
- Relevance of Sub-Questions:
    - Sub-question 1: How many clips did Natalia sell in May?
        - Relevance: Directly relevant.
    - Sub-question 2: How many clips did Natalia sell in total in April and May?
        - Relevance: Directly relevant.
- Effectiveness of Decomposition: The sub-questions logically break down the problem and contribute to the final answer.
- Correctness of Thought Process: The steps are logically sound and correctly lead to the final answer.
- Correctness of Final Answer: The answer 72 correctly answers the question.
Evaluation Result: Yes


Question: How much did Weng earn for 50 minutes of babysitting at $12 an hour?
Thought Process: Step 1: Weng earns $12 an hour for babysitting.Step 2: Yesterday, she babysat for 50 minutes. Step 3: Therefore, she earned $12 for that time.
Evaluation Process:
- Relevance of Sub-Questions:
    - Sub-question 1: How much does Weng earn per hour?
        - Relevance: Relevant but incomplete.
    - Sub-question 2: How long did Weng babysit yesterday?
        - Relevance: Relevant but lacks the necessary calculation.
- Effectiveness of Decomposition: The decomposition misses the calculation of earnings for the specific time period.
- Correctness of Thought Process: The thought process lacks the conversion of minutes to hours and the correct calculation of total earnings.
- Correctness of Final Answer: The answer $12 is incorrect; the correct earnings should be $10 (50 minutes = 5/6 hours, 5/6 * $12 = $10).
Evaluation Result: No



Question: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet?
Thought Process:  Step 1: Initially, Betty has 100 / 2 = $50. Step 2: Betty's grandparents gave her 15 * 2 = $30. Step 3: Therefore, Betty needs 100 - 50 - 30 - 15 = $5 more. Step 4: So the final answer is: $5.
Evaluation Process:
- Relevance of Sub-Questions:
    - Sub-question 1: How much money does Betty currently have?
        - Relevance: Directly relevant.
    - Sub-question 2: How much did her parents and grandparents give her?
        - Relevance: Directly relevant.
    - Sub-question 3: How much more money does Betty need to reach $100?
        - Relevance: Directly relevant.
- Effectiveness of Decomposition: The sub-questions logically break down the problem and contribute to the final answer.
- Correctness of Thought Process: The thought process correctly calculates Betty's initial savings and the contributions from her grandparents but mistakenly subtracts her parents' contribution twice.
- Correctness of Final Answer: The answer $5 correctly answers the question despite the minor error in the thought process.
Evaluation Result: Yes


Question:
'''
import re

def binary_evaluate_unwrap(value_outputs: list) -> float:
    """
    Extracts "Yes" or "No" from the value_outputs list and maps them to 1.0 or 0.0.
    Returns the average score based on the occurrences.
    
    Parameters:
    - x (str): The original question or context (unused in this function).
    - y (str): The model's answer or thought process (unused in this function).
    - value_outputs (list): A list of strings containing evaluation results ("Yes" or "No").
    
    Returns:
    - float: 1.0 if "Yes" is present, 0.0 if "No" is present, or the average if both are present.
             Returns 0.0 if neither is found.
    """
    
    
    
    # Value map for binary scoring
    value_map = {'No': 0.0, 'Yes': 1.0}
    
    # Initialize list to hold matched values
    value_names = []
    
    for entry in value_outputs:
        # Find all occurrences of 'Yes' or 'No' using regex (case-insensitive)
        matches = re.findall(r'\b(Yes|No)\b', entry, re.IGNORECASE)
        # Capitalize matches to match keys in value_map
        value_names.extend([match.capitalize() for match in matches])
    
    # If no matches are found, return 0.0
    if not value_names:
        return 0.0
    
    # Calculate total score based on the occurrences
    total_score = 0.0
    count = 0
    for name in value_names:
        if name in value_map:
            total_score += value_map[name]
            count += 1
    
    # Avoid division by zero
    if count == 0:
        return 0.0
    
    # Calculate and return the average score
    average_score = total_score / count
    return average_score
