standard_prompt = '''Task: Answer the given question, and conclude with the phrase 'so the final answer is: true or false'.
Question: Jompuses are not shy. Jompuses are yumpuses. Each yumpus is aggressive. Each yumpus is a dumpus. Dumpuses are not wooden. Dumpuses are wumpuses. Wumpuses are red. Every wumpus is an impus. Each impus is opaque. Impuses are tumpuses. Numpuses are sour. Tumpuses are not sour. Tumpuses are vumpuses. Vumpuses are earthy. Every vumpus is a zumpus. Zumpuses are small. Zumpuses are rompuses. Max is a yumpus. Is the following statement true or false? Max is sour.
Answer: so the final answer is: false. End of answer.

Question: Each brimpus is small. Lorpuses are liquid. Vumpuses are zumpuses. Every lempus is bright. Every sterpus is a lorpus. Grimpuses are yumpuses. Sterpuses are snowy. Grimpuses are sterpuses. Sterpuses are impuses. Every yumpus is fruity. Every brimpus is a gorpus. Lempuses are rompuses. Every brimpus is a grimpus. Every grimpus is angry. Every zumpus is a jompus. Each gorpus is loud. Jompuses are opaque. Vumpuses are brown. Each zumpus is a brimpus. Every vumpus is a dumpus. Every dumpus is feisty. Every zumpus is slow. Sam is a lempus. Sam is a zumpus. Is the following statement true or false? Sam is slow.
Answer:  so the final answer is: true. End of answer

Question: Every tumpus is not angry. Tumpuses are rompuses. Every numpus is not bright. Rompuses are not luminous. Rompuses are yumpuses. Yumpuses are transparent. Yumpuses are zumpuses. Each zumpus is not bitter. Zumpuses are impuses. Impuses are red. Each impus is a dumpus. Every dumpus is happy. Each dumpus is a vumpus. Vumpuses are bright. Every vumpus is a jompus. Jompuses are large. Each jompus is a wumpus. Stella is a yumpus. Is the following statement true or false? Stella is bright.
Answer: so the final answer is: true. End of answer.

Question: {input}
'''





cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is: true or false'.

Question: Jompuses are not shy. Jompuses are yumpuses. Each yumpus is aggressive. Each yumpus is a dumpus. Dumpuses are not wooden. Dumpuses are wumpuses. Wumpuses are red. Every wumpus is an impus. Each impus is opaque. Impuses are tumpuses. Numpuses are sour. Tumpuses are not sour. Tumpuses are vumpuses. Vumpuses are earthy. Every vumpus is a zumpus. Zumpuses are small. Zumpuses are rompuses. Max is a yumpus. Is the following statement true or false? Max is sour.
Answer:
Step 1, Max is a yumpus. 
Step 2, Each yumpus is a dumpus, so Max is a dumpus. Dumpuses are wumpuses, so Max is a wumpus. Every wumpus is an impus, so Max is an impus. Impuses are tumpuses, so Max is a tumpus.
Step 3, Tumpuses are not sour, so Max is not sour.
Step 4, so the final answer is: false. End of answer.


Question: Each brimpus is small. Lorpuses are liquid. Vumpuses are zumpuses. Every lempus is bright. Every sterpus is a lorpus. Grimpuses are yumpuses. Sterpuses are snowy. Grimpuses are sterpuses. Sterpuses are impuses. Every yumpus is fruity. Every brimpus is a gorpus. Lempuses are rompuses. Every brimpus is a grimpus. Every grimpus is angry. Every zumpus is a jompus. Each gorpus is loud. Jompuses are opaque. Vumpuses are brown. Each zumpus is a brimpus. Every vumpus is a dumpus. Every dumpus is feisty. Every zumpus is slow. Sam is a lempus. Sam is a zumpus. Is the following statement true or false? Sam is slow.
Answer: Step 1, Sam is a zumpus.
Step 2, Every zumpus is slow.
Step 3, Sam is slow.
Step 4, so the final answer is: true.
End of answer

Question: Every tumpus is not angry. Tumpuses are rompuses. Every numpus is not bright. Rompuses are not luminous. Rompuses are yumpuses. Yumpuses are transparent. Yumpuses are zumpuses. Each zumpus is not bitter. Zumpuses are impuses. Impuses are red. Each impus is a dumpus. Every dumpus is happy. Each dumpus is a vumpus. Vumpuses are bright. Every vumpus is a jompus. Jompuses are large. Each jompus is a wumpus. Stella is a yumpus. Is the following statement true or false? Stella is bright.
Answer:
Step 1, Stella is a yumpus. 
Step 2, Yumpuses are zumpuses, so Stella is a zumpus. Each zumpus is an impus, so Stella is an impus. Each impus is a dumpus, so Stella is a dumpus.
Step 3, Every dumpus is a vumpus, so Stella is a vumpus. Vumpuses are bright, so Stella is bright.
Step 4, so the final answer is: true. End of answer.

Question: {input}
'''





reflect_cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is: true or false'.
Ensure that each step is followed by a "Reflection:" line, considering the accuracy and reliability of the process.

Question: Jompuses are not shy. Jompuses are yumpuses. Each yumpus is aggressive. Each yumpus is a dumpus. Dumpuses are not wooden. Dumpuses are wumpuses. Wumpuses are red. Every wumpus is an impus. Each impus is opaque. Impuses are tumpuses. Numpuses are sour. Tumpuses are not sour. Tumpuses are vumpuses. Vumpuses are earthy. Every vumpus is a zumpus. Zumpuses are small. Zumpuses are rompuses. Max is a yumpus. Is the following statement true or false? Max is sour.
Answer:
Step 1, Max is a yumpus.
Reflection: The premise is clear: Max is a yumpus, as stated in the question.
Step 2, Each yumpus is a dumpus, so Max is a dumpus. Dumpuses are wumpuses, so Max is a wumpus. Every wumpus is an impus, so Max is an impus. Impuses are tumpuses, so Max is a tumpus.
Reflection: I correctly follow the relationships defined in the question from one type of creature to the next. The logical progression seems accurate.
Step 3, Tumpuses are not sour, so Max is not sour.
Reflection: The relationship between tumpuses and sourness is explicitly mentioned, so this step appears correct. ** Error:**  Based on the steps, the reasoning is valid. Max is not sour because tumpuses (which Max is) are not sour. However, I realize that I skipped a crucial check in the relationships between the creatures: *Max being a yumpus* means Max could also be aggressive (based on the property of yumpuses being aggressive). However, this aggression does not directly affect whether Max is sour. Since the rest of the reasoning is valid, my initial conclusion of "false" still stands. 
so the final answer is: false. 
End of answer.

Question: Each brimpus is small. Lorpuses are liquid. Vumpuses are zumpuses. Every lempus is bright. Every sterpus is a lorpus. Grimpuses are yumpuses. Sterpuses are snowy. Grimpuses are sterpuses. Sterpuses are impuses. Every yumpus is fruity. Every brimpus is a gorpus. Lempuses are rompuses. Every brimpus is a grimpus. Every grimpus is angry. Every zumpus is a jompus. Each gorpus is loud. Jompuses are opaque. Vumpuses are brown. Each zumpus is a brimpus. Every vumpus is a dumpus. Every dumpus is feisty. Every zumpus is slow. Sam is a lempus. Sam is a zumpus. Is the following statement true or false? Sam is slow.
Answer: 
Step 1, Sam is a zumpus.
Reflection: The first statement is directly given, Sam is a zumpus.
Step 2, Every zumpus is slow.
Reflection: The condition that every zumpus is slow is provided, so I can directly deduce this.
Step 3, Sam is slow.
Reflection: Given that Sam is a zumpus and every zumpus is slow, the conclusion follows logically.
so the final answer is: true. 
End of answer.

Question: Every tumpus is not angry. Tumpuses are rompuses. Every numpus is not bright. Rompuses are not luminous. Rompuses are yumpuses. Yumpuses are transparent. Yumpuses are zumpuses. Each zumpus is not bitter. Zumpuses are impuses. Impuses are red. Each impus is a dumpus. Every dumpus is happy. Each dumpus is a vumpus. Vumpuses are bright. Every vumpus is a jompus. Jompuses are large. Each jompus is a wumpus. Stella is a yumpus. Is the following statement true or false? Stella is bright.
Answer: 
Step 1, Stella is a yumpus. 
Reflection: This is given in the question and is correctly noted.
Step 2, Yumpuses are zumpuses, so Stella is a zumpus. Each zumpus is an impus, so Stella is an impus. Each impus is a dumpus, so Stella is a dumpus.
Reflection: Following the properties from yumpus to zumpus to dumpus is logically consistent, with no ambiguity in the relationships.
Step 3, Every dumpus is a vumpus, so Stella is a vumpus. Vumpuses are bright, so Stella is bright.
Reflection: The chain of reasoning here is sound. Since Stella is a vumpus and vumpuses are bright, this conclusion is reliable.
so the final answer is: true.
Reflection: The logical flow of reasoning is correct, and Stella must indeed be bright based on the properties established.
End of answer.

Question: {input}
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