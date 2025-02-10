#unfinshed
# 3-shot
standard_prompt = '''Task: Answer the given question, and conclude with the phrase 'so the final answer is: .
Question: What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into? Answer: so the final answer is: 1,800 to 7,000 ft. End of answer.
Question: What profession does Nicholas Ray and Elia Kazan have in common? Answer: so the final answer is: director, screenwriter, actor. End of answer.
Question: Which magazine was started first Arthur's Magazine or First for Women? Answer: so the final answer is: Rudra Shah. End of answer.
Question: {input}
'''


#3-shot
cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is: .
Question: Who lived longer, Theodor Haecker or Harry Vaughan Watkins? Answer: Step 1, the eastern sector of Colorado orogeny extends into the High Plains. Step 2, high Plains rise in elevation from around 1,800 to 7,000 ft. Step 3, so the final answer is: 1,800 to 7,000 ft. End of answer.
Question: What profession does Nicholas Ray and Elia Kazan have in common? Answer: Step 1, professions of Nicholas Ray are director, screenwriter, and actor. Step 2, professions of Elia Kazan are director, producer, screenwriter, and actor. Step 3, so the final answer is: director, screenwriter, actor. End of answer.
Question: Which magazine was started first Arthur's Magazine or First for Women? Answer: Step 1, who is the son of  Dambar Shah? Dambar Shah (? - 1645) was the father of Krishna Shah. Step 2, who is the son of Krishna Shah? Krishna Shah (? - 1661) was the father of Rudra Shah. Step 3, so the final answer is: Rudra Shah. End of answer.
Question: {input}
'''


reflect_cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is: [answer]. End of answer.'
Ensure that each step is followed by a "Reflection:" line, considering the accuracy and reliability of the process.

Question: Who lived longer, Theodor Haecker or Harry Vaughan Watkins? 
Answer:
Step 1: When did Theodor Haecker die? Theodor Haecker was 65 years old when he died.
Reflection: The age at death is given directly, so no further refinement is needed.

Step 2: When did Harry Vaughan Watkins die? Harry Vaughan Watkins was 69 years old when he died.
Reflection: This fact is straightforward and provides a direct comparison to Theodor Haecker's age.

Step 3: Compare the ages at death: 65 (Haecker) vs. 69 (Watkins).
Reflection: The comparison shows that Harry Vaughan Watkins lived longer. This is a clear and accurate conclusion.

So the final answer is: Harry Vaughan Watkins. End of answer.

Question: What profession does Nicholas Ray and Elia Kazan have in common? 
Answer:
Step 1: What are Nicholas Ray’s professions? Nicholas Ray was a director, screenwriter, and actor.
Reflection: These are well-known professions for Nicholas Ray, so this information is accurate.

Step 2: What are Elia Kazan’s professions? Elia Kazan was a director, producer, screenwriter, and actor.
Reflection: This also accurately reflects Elia Kazan’s professions. Both individuals share the professions of director, screenwriter, and actor.

Step 3: Conclude the common professions. Both Nicholas Ray and Elia Kazan were directors, screenwriters, and actors.
Reflection: The professions of both individuals overlap in director, screenwriter, and actor.

So the final answer is: director, screenwriter, actor. End of answer.

Question: Which magazine was started first: Arthur's Magazine or First for Women?

Step 1: When was Arthur’s Magazine started? Arthur’s Magazine was first published in 1853.
Reflection: This is an accurate fact. No further verification needed.

Step 2: When was First for Women started? First for Women was first published in 1990.
Reflection: **Error**: The publication date I initially provided for First for Women was 1990, but after further checking, it was actually first published in 1989, not 1990. So, the corrected date is 1989.

Step 3: Compare the start dates. Arthur’s Magazine (1853) vs. First for Women (1989).
Reflection: Now that I have the correct publication date for First for Women (1989), it's clear that Arthur’s Magazine was started first, over a century earlier than First for Women.

Final Answer: Arthur’s Magazine was started first. End of answer.


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