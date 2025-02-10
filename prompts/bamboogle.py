# # 3-shot
standard_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is: .
Question: Who lived longer, Theodor Haecker or Harry Vaughan Watkins? Answer: so the final answer is: Harry Vaughan Watkins. End of answer.
Question: Why did the founder of Versus die? Answer: so the final answer is: Shot. End of answer.
Question: Who is the grandchild of Dambar Shah? Answer: so the final answer is: Rudra Shah. End of answer.
Question: {input} 
'''


# 3-shot
# standard_prompt = '''Task: Answer the given question below strictly in the format "Answer: [your answer here]", without repeating the question. Conclude with the phrase 'so the final answer is: '

# Few-shot examples:
# Question: Who lived longer, Theodor Haecker or Harry Vaughan Watkins? Answer: so the final answer is: Harry Vaughan Watkins.
# Question: Why did the founder of Versus die? Answer: so the final answer is: Shot.
# Question: Who is the grandchild of Dambar Shah? Answer: so the final answer is: Rudra Shah.

# Now answer the question below in the specified format:
# Question: {input} Answer:
# '''


#3-shot
cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is: .
Question: Who lived longer, Theodor Haecker or Harry Vaughan Watkins? Answer: Step 1, when did Theodor Haecker die? Theodor Haecker was 65 years old when he died. Step 2, when did  Harry Vaughan Watkins die? Harry Vaughan Watkins was 69 years old when he died. Step 3, so the final answer is: Harry Vaughan Watkins. End of answer.
Question: Why did the founder of Versus die? Answer: Step 1, who is the funder of Versus? The founder of Versus was Gianni Versace. Step 2, why did Gianni Versace die? Gianni Versace was shot and killed on the steps of his Miami Beach mansion on July 15, 1997. Step 3, so the final answer is: Shot. End of answer.
Question: Who is the grandchild of Dambar Shah? Answer: Step 1, who is the son of  Dambar Shah? Dambar Shah (? - 1645) was the father of Krishna Shah. Step 2, who is the son of Krishna Shah? Krishna Shah (? - 1661) was the father of Rudra Shah. Step 3, so the final answer is: Rudra Shah. End of answer.
Question: {input}
'''

reflect_cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is: [answer]. End of answer.'
Ensure that each step is followed by a "Reflection:" line, considering the accuracy and reliability of the process.

Question: Who lived longer, Theodor Haecker or Harry Vaughan Watkins?
Answer:
Step 1: When did Theodor Haecker die? Theodor Haecker was 65 years old when he died.
Reflection: The age at death is directly given and is considered accurate without needing further verification.

Step 2: When did Harry Vaughan Watkins die? Harry Vaughan Watkins was 69 years old when he died.
Reflection: This fact is simple and consistent with the question. It is directly verified.

Step 3: Compare the ages at death. 65 (Haecker) vs. 69 (Watkins).
Reflection: The comparison clearly shows that Harry Vaughan Watkins lived longer than Theodor Haecker.
So the final answer is: Harry Vaughan Watkins. End of answer.

Question: Why did the founder of Versus die?
Answer:
Step 1: Who is the founder of Versus? The founder of Versus was Gianni Versace.
Reflection: Gianni Versace is the well-known founder of the Versus brand, which is part of the Versace fashion house.

Step 2: Why did Gianni Versace die? Gianni Versace was shot and killed on the steps of his Miami Beach mansion on July 15, 1997.
Reflection: This fact is clear, well-documented, and does not need further elaboration.

Step 3: Conclude with the cause of death. Gianni Versace was shot.
Reflection: The cause of death is unambiguous and matches the historical record.
So the final answer is: Shot. End of answer.

Question: Who is the grandchild of Dambar Shah?
Answer:
Step 1: Who is the son of Dambar Shah? Dambar Shah (? - 1645) was the father of Krishna Shah.
Reflection: The relationship between Dambar Shah and Krishna Shah is correctly identified.

Step 2: Who is the son of Krishna Shah? Krishna Shah (? - 1661) was the father of Dambar Shah's grandchild. (Error: The explanation mistakenly assumes Krishna Shah's son is the grandchild.)
Reflection: **Error**: This explanation is incorrect. Krishna Shah is the **son** of Dambar Shah, not his **grandchild**. The grandson must be Krishna Shah's son, not Krishna Shah himself.

Step 3: The grandchild of Dambar Shah is Rudra Shah.
Reflection: After correcting Step 2, we find that the grandchild of Dambar Shah is **Rudra Shah**, who is the son of Krishna Shah. This correction aligns with the family tree.
So the final answer is: Rudra Shah. End of answer.

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


choose_evaluate = '''Evaluate whether the provided answer matches any of the options listed in the question  (Likely/Impossible).

Question: You are presented with the question "What do veins carry?" and the following answer choices:  - copper  - glucose  - Energy  - Length  - oxygen  - warmth  - Cells  - voltage  Now knowing that veins generally carry deoxygenated blood and blood carries blood cells, choose the best answer.
Answer: Blood
Evaluation Process: The listed choices include copper, glucose, energy, length, oxygen, warmth, cells, and voltage, but blood is not among these options.
Evaluation Result:
Impossible
End of answer.

Question: Please answer the following question: You are presented with the question "What converts chemical energy into sound?" and the following answer choices:  - a firework  - sensory neurons  - Gunshots  - a bottle  - a battery  - animals  - a flashlight  - engines  Now knowing that afirecracker converts chemical energy into sound and fireworks are illegal, including firecrackers, choose the best answer.
Answer: a firework
Evaluation Process: Among the provided options, which include sensory neurons, gunshots, a bottle, a battery, animals, a flashlight, and engines, a firework is indeed one of the choices.
Evaluation Results:
Likely
End of answer.

Question: You are presented with the question "A good way for older adults to strengthen bones is to " and the following answer choices:  - Through play  - drive more slowly  - exercise  - use a hearing aid  - quadriceps  - donate bone marrow  - sweating  - movement  Now knowing that exercise increases a body 's strength and strength training is also effective for increasing bone strength in older adults, choose the best answer.
Answer: exercise
Evaluation Process: Among the options listed, such as through play, driving more slowly, using a hearing aid, quadriceps, donating bone marrow, sweating, and movement, exercise is indeed included.
Evaluation Results:
Likely
End of answer.

Question: You are presented with the question "what is a negative impact on an organism" and the following answer choices:  - malnutrition  - plants  - hyperthyroidism  - sweat  - laughter  - smallpox  - leukemia  Now knowing that disease has a negative impact on an organism and infectious diseases and diseases of malnutrition are prevalent, choose the best answer.
Answer: cancer
Evaluation Process: The options provided include malnutrition, plants, hyperthyroidism, sweat, laughter, smallpox, and leukemia, but cancer is not listed among these choices.
Evaluation Results:
Impossible
End of answer.

Question: '''

wiki_evaluate = '''Evaluate whether the language model can effectively decompose the question into relevant sub-questions, and assess whether this decomposition helps in partially or directly answering the original question. The outcome will determine if this process of decomposition is "Likely" or "Impossible" to aid in finding the answer.

Evaluation Steps: Check if the language model can identify and decompose key sub-questions that are directly related to the original question.
Evaluation Process: 1. Analyze whether each sub-question identified by the model is directly relevant to the answer to the original question. 2. Determine if the decomposition of these sub-questions forms a reasonable response to the original question.
Evaluation Result: 1. Likely: If the language model successfully decomposes the original question into relevant sub-questions that help construct the final answer. 2. Impossible: If the language model fails to effectively decompose the question, or if the decomposed sub-questions are not directly relevant to finding the answer.

Question: Who lived longer, Theodor Haecker or Harry Vaughan Watkins?
Thought Process: Step 1, when did Theodor Haecker die? Theodor Haecker was 65 years old when he died. Step 2, when did  Harry Vaughan Watkins die? Harry Vaughan Watkins was 69 years old when he died.
Evaluation Process:
Relevance of Sub-Questions: The sub-question regarding Theodor Haecker's age at death is directly relevant to the main question, as it provides necessary information to determine his lifespan. Similarly, the sub-question about Harry Vaughan Watkins' age at death is also directly relevant for the same reason.
Effectiveness of Decomposition: The decomposition into two key sub-questions (ages at death of both individuals) is an effective strategy. It breaks down the main question (comparison of lifespans) into specific, answerable elements. Each sub-question contributes a crucial piece of information required to compare the lifespans of the two individuals.
Evaluation Result:
Likely
End of answer.

Question: When did the last king from Britain's House of Hanover die?
Thought: Step 1, when did the last king from Britain's House of Hanover born? 
Evaluation Process:
The thought process focuses on the birth date of the last king from Britain's House of Hanover. However, knowing the birth date does not directly help in determining the date of death, which is the actual question. The lifespan of an individual can vary widely and cannot be accurately inferred from their birth date alone. Therefore, this thought process is unlikely to lead to the correct answer without additional information.
So the evaluation result is: this thought is impossible to help pariticially or directly answer the question.
Evaluation Results:
Impossible
End of answer.

Question: What is the highest mountain in the world?
Thought Process: Step 1, identify the tallest mountains known globally. Mount Everest is commonly known as the highest mountain peak in the world.
Evaluation Process:
The thought process begins with identifying the tallest mountains known globally, which is a logical first step. Since Mount Everest is commonly known and recognized as the highest mountain peak in the world, this thought directly leads to the answer to the question. Therefore, this approach is very likely to help in answering the question correctly.
So, the evaluation result is: this thought is likely to help partially or directly answer the question.
Evaluation Results:
Likely
End of answer.

Question: How many planets are in our solar system?
Thought Process: Step 1, consider the composition of the Sun and its impact on the solar system.
Evaluation Process:
The thought process of considering the composition of the Sun and its impact on the solar system does not directly lead to an answer for the number of planets in our solar system. The Sun's composition and its effects are more relevant to solar physics and do not provide specific information about the count or existence of planets. The question requires knowledge about the classification and count of planets in the solar system, which is unrelated to the Sun's composition.
So, the evaluation result is: this thought is impossible to help partially or directly answer the question.
Evaluation Results:
Impossible
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
