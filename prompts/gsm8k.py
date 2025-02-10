# 3-shot
standard_prompt = '''Task: Answer the given question, and conclude with the phrase 'so the final answer is: .
Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May? Answer: so the final answer is: 72. End of answer.
Question: Lizzy: Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn? Answer: so the final answer is: 10. End of answer.
Question: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet? Answer: so the final answer is: 5. End of answer.
Question: {input}
'''


#3-shot
cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is: .
Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May? Answer: Step 1, natalia sold 48 / 2 = 24 clips in May. Step 2: Natalia sold 48 + 24 = 72 clips altogether in April and May.  Step 3: so the final answer is: 72. End of answer.
Question: Lizzy: Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn? Answer: Step 1, weng earns 12 / 60 = $0.2 per minute.  Step 2, working 50 minutes, she earned 0.2 x 50 = $10. Step 3, so the final answer is: 10. End of answer.
Question: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet? Answer: Step 1, in the beginning, Betty has only 100 / 2 = $50. Step 2, betty's grandparents gave her 15 * 2 = $30. This means, Betty needs 100 - 50 - 30 - 15 = $5 more. Step 3, so the final answer is: 5. End of answer.
Question: {input}
'''


reflect_cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is: [answer]. End of answer.'
Ensure that each step is followed by a "Reflection:" line, considering the accuracy and reliability of the process.

Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?
Answer:
Step 1: Determine the number of clips sold in April: 48.
Reflection: The initial data point is given and used directly. No modification needed.

Step 2: Calculate the number of clips sold in May, which is half of April's total: 48 ÷ 2 = 24.
Reflection: Half of 48 is indeed 24, correct and straightforward.

Step 3: Add the numbers sold in April and May: 48 + 24 = 72.
Reflection: The addition is correct; 72 is the total number of clips sold.

So the final answer is: 72. End of answer.


Question: Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?
Answer:
Step 1: Convert Weng’s hourly rate into a per-minute rate: $12 ÷ 60 minutes = $0.20 per minute.
Reflection: Dividing 12 by 60 is correct, and 0.20 per minute makes sense.

Step 2: Multiply the per-minute rate by the total minutes worked: $0.20 × 50 = $10.
Reflection: 0.20 times 50 is indeed 10, which fits the expected proportion of an hour’s earnings.

Step 3: Verify if the logic aligns with expectations. 50 minutes is just under an hour, so earning $10 is reasonable.
Reflection: The logic holds up — since 50 minutes is less than an hour, earning $10 instead of $12 is consistent.

So the final answer is: 10. End of answer.


Question: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet?
Answer:
Step 1: Determine how much Betty initially has. Half of $100 is $50.
Reflection: Half of $100 is correctly calculated as $50.

Step 2: Calculate the total additional money Betty receives from her parents and grandparents. Parents give $15, and grandparents give $30.
Reflection: The grandparents' contribution is correctly calculated as $30, which is twice what the parents gave.

Step 3: Add up all the money Betty has: $50 (initial) + $15 (parents) + $30 (grandparents) = $80. Then subtract this total from the price of the wallet: $100 - $80 = $20.
Reflection: **Error**: The total money Betty has should be $50 + $15 + $30 = $95, not $80. The error here is that the total amount Betty has was miscalculated as $80. The correct calculation should be $100 - $95 = $5, not $100 - $80.

Step 4: Correct the error and subtract the accurate total: $100 - $95 = $5.
Reflection: Now that the correct total is used, the calculation is accurate: Betty needs $5 more to buy the wallet.

So the final answer is: 5. End of answer.


Question: {input}
'''







agent_cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is: '.

Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?
Answer:
Shared information: no shared information.
Step 1, calculate how many clips Natalia sold in May. Natalia sold 48 / 2 = 24 clips in May. End of step.
Shared information: Natalia sold 24 clips in May.
Step 2, calculate the total clips sold in April and May. Natalia sold 48 + 24 = 72 clips in total. End of step.
Shared information: Natalia sold 72 clips in total in April and May.
Step 3, so the final answer is: 72.
End of answer.

Question: Lizzy: Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?
Answer:
Shared information: no shared information.
Step 1, calculate how much Weng earns per minute. Weng earns 12 / 60 = $0.2 per minute. End of step.
Shared information: Weng earns $0.2 per minute.
Step 2, calculate how much Weng earned for 50 minutes. Weng earned 0.2 x 50 = $10. End of step.
Shared information: Weng earned $10 for 50 minutes.
Step 3, so the final answer is: 10.
End of answer.

Question: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet?
Answer:
Shared information: no shared information.
Step 1, determine how much Betty initially has and how much her grandparents gave her. Betty has 100 / 2 = $50, and her grandparents gave her 15 * 2 = $30. End of step.
Shared information: Betty has $50 initially, and her grandparents gave her $30.
Step 2, calculate how much more money Betty needs. Betty needs 100 - 50 - 30 - 15 = $5. End of step.
Shared information: Betty needs $5 more to buy the wallet.
Step 3, so the final answer is: 5.
End of answer.

Question: {input}
Answer:
Shared information: no shared information.
'''


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




