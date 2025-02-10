
standard_prompt = '''Task: Answer the given question, and conclude with the phrase 'so the final answer is: .  Please put your final answer within \\boxed{{}}.
Question: The points $P,$ $Q,$ and $R$ are represented by the complex numbers $z,$ $(1 + i) z,$ and $2 \\overline{{z}},$ respectively, where $|z| = 1.$ When $P,$ $Q,$ and $R$ are not collinear, let $S$ be the fourth vertex of the parallelogram $PQSR.$ What is the maximum distance between $S$ and the origin of the complex plane?
Answer: so the final answer is: \\boxed{{3}}.  End of answer.

Question: Given a cylinder of fixed volume $V,$ the total surface area (including the two circular ends) is minimized for a radius of $R$ and height $H.$ Find $\\frac{{H}}{{R}}.$
Answer: so the final answer is: \\boxed{{2}}.  End of answer.

Question: Suppose that $(u_n)$ is a sequence of real numbers satisfying $u_{{n+2}}=2u_{{n+1}}+u_n$ and that $u_3=9$ and $u_6=128$. What is $u_5$?
Answer: so the final answer is: \\boxed{{53}}.  End of answer.

Question: {input}
'''





cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is:'. Please reason step by step, and put your final answer within \\boxed{{}}.

Question: The points $P,$ $Q,$ and $R$ are represented by the complex numbers $z,$ $(1 + i) z,$ and $2 \\overline{{z}},$ respectively, where $|z| = 1.$ When $P,$ $Q,$ and $R$ are not collinear, let $S$ be the fourth vertex of the parallelogram $PQSR.$ What is the maximum distance between $S$ and the origin of the complex plane?
Answer:
step 1: From the parallelogram condition: $S = Q + R - P$. Substitute $P=z$, $Q=(1+i)z$, $R=2\\overline{{z}}$ to get $S: w = iz + 2\\overline{{z}}$.
step 2: Compute $|w|^2 = w\\overline{{w}}$. After simplification with $|z|=1$, we find $|w|^2 = 5 - 8xy$, where $z=x+yi$.
step 3: Using $(x+y)^2\\ge0$, we have $-8xy\\le4$, so $|w|^2\\le9$, thus $|w|\\le3$. Equality can occur, so the maximum distance is 3.
so the final answer is: \\boxed{{3}}.  End of answer.

Question: Given a cylinder of fixed volume $V,$ the total surface area (including the two circular ends) is minimized for a radius of $R$ and height $H.$ Find $\\frac{{H}}{{R}}.$
Answer:
step 1: Let the radius be $r$ and height be $h$. The volume constraint is $\\pi r^2 h = V$.
step 2: The total surface area is $A = 2\\pi r^2 + 2\\pi r h$. Using AM-GM on $2\\pi r^2$, $\\pi r h$, and $\\pi r h$: $A = 2\\pi r^2 + \\pi r h + \\pi r h \\geq 3\\sqrt[3]{{(2\\pi r^2)(\\pi r h)(\\pi r h)}}$.
step 3: Since $\\pi r^2 h=V$, we have $r^2h=V/\\pi$. After simplification, the equality condition gives $2\\pi r^2=\\pi r h$, implying $h=2r$.
so the final answer is: \\boxed{{2}}.  End of answer.

Question: Suppose that $(u_n)$ is a sequence of real numbers satisfying $u_{{n+2}}=2u_{{n+1}}+u_n$ and that $u_3=9$ and $u_6=128$. What is $u_5$?
Answer:
step 1: Let $u_4 = a$. From the recurrence, $u_5 = 2u_4 + u_3 = 2a + 9$.
step 2: Also, $u_6 = 2u_5 + u_4 = 2(2a + 9) + a = 5a + 18$.
step 3: Given $u_6 = 128$, we have $5a +18 =128$. Thus $5a=110$ and $a=22$.
step 4: With $a=22$, $u_5 = 2(22)+9 = 44 + 9 = 53$.
so the final answer is: \\boxed{{53}}.  End of answer.

Question: {input}
'''


reflect_cot_prompt = '''Task: Answer the given question step-by-step, and conclude with the phrase 'so the final answer is:'. Please reason step by step, and put your final answer within \\boxed{{}}.
Ensure that each step is followed by a "Reflection:" line, considering the accuracy and reliability of the process.

Question: The points $P,$ $Q,$ and $R$ are represented by the complex numbers $z,$ $(1 + i) z,$ and $2 \\overline{{z}},$ respectively, where $|z| = 1.$ When $P,$ $Q,$ and $R$ are not collinear, let $S$ be the fourth vertex of the parallelogram $PQSR.$ What is the maximum distance between $S$ and the origin of the complex plane?
Answer:
step 1: From the parallelogram condition: $S = Q + R - P$. Substitute $P=z$, $Q=(1+i)z$, $R=2\\overline{{z}}$ to get $S: w = iz + 2\\overline{{z}}$.
Reflection: The equation $w = iz + 2\\overline{{z}}$ appears correct based on the parallelogram rule, no issues here. 
step 2: Compute $|w|^2 = w\\overline{{w}}$. After simplification with $|z|=1$, we find $|w|^2 = 5 - 8xy$, where $z=x+yi$.
Reflection: **Error:** We should have expanded the expression $w = iz + 2\overline{{z}}$ properly, and the simplification in step 2 was prematurely made. Let’s correct this.
step 3: Let $z = x + iy$, so $w = i(x + iy) + 2(x - iy)$. Expanding this, we get $w = -y + ix + 2x - 2iy = (2x - y) + i(x - 2y)$. Now we compute $|w|^2$:
\[
|w|^2 = (2x - y)^2 + (x - 2y)^2 = 4x^2 - 4xy + y^2 + x^2 - 4xy + 4y^2 = 5x^2 - 8xy + 5y^2
\]
Reflection: After redoing the calculation and simplifying correctly, we obtain $|w|^2 = 5x^2 - 8xy + 5y^2$. This is a better simplification that matches the form we needed. Initially, I was too quick to simplify, but after correcting the steps, we now have a reliable form for $|w|^2$.
step 4: Using $(x+y)^2\\ge0$, we have $-8xy\\le4$, so $|w|^2\\le9$, thus $|w|\\le3$. Equality can occur, so the maximum distance is 3.
Reflection: This step is still valid after the correction. The final distance calculation remains the same, with $|w|$ being bounded by 3.

so the final answer is: \\boxed{{3}}.  End of answer.

Question: Given a cylinder of fixed volume $V,$ the total surface area (including the two circular ends) is minimized for a radius of $R$ and height $H.$ Find $\\frac{{H}}{{R}}.$
Answer:
step 1: Let the radius be $r$ and height be $h$. The volume constraint is $\\pi r^2 h = V$.
Reflection: This is a correct setup for the volume constraint.
step 2: The total surface area is $A = 2\\pi r^2 + 2\\pi r h$. Using AM-GM on $2\\pi r^2$, $\\pi r h$, and $\\pi r h$: $A = 2\\pi r^2 + \\pi r h + \\pi r h \\geq 3\\sqrt[3]{{(2\\pi r^2)(\\pi r h)(\\pi r h)}}$.
Reflection: This is where the error occurs. The AM-GM inequality application here is unnecessary and overly complicated for minimizing the surface area. The correct approach is to differentiate the surface area function directly.
step 3: Since $\\pi r^2 h=V$, we have $r^2h=V/\\pi$. After simplification, the equality condition gives $2\\pi r^2=\\pi r h$, implying $h=2r$.
Reflection: This step is correct, as it derives the relationship between $h$ and $r$ from the first principles of optimization.
so the final answer is: \\boxed{{2}}.  End of answer.

Question: Suppose that $(u_n)$ is a sequence of real numbers satisfying $u_{{n+2}}=2u_{{n+1}}+u_n$ and that $u_3=9$ and $u_6=128$. What is $u_5$?
Answer:
step 1: Let $u_4 = a$. From the recurrence, $u_5 = 2u_4 + u_3 = 2a + 9$.
Reflection: The recurrence relation is applied correctly, and the formula for $u_5$ is accurate.
step 2: Also, $u_6 = 2u_5 + u_4 = 2(2a + 9) + a = 5a + 18$.
Reflection: The formula for $u_6$ is correctly derived, but I will now check for consistency.
step 3: Given $u_6 = 128$, we have $5a +18 =128$. Thus $5a=110$ and $a=22$.
Reflection: The algebra here is correct, and solving for $a$ gives $a = 22$.
step 4: With $a=22$, $u_5 = 2(22)+9 = 44 + 9 = 53$.
Reflection: The calculation for $u_5$ is correct, and the value matches the recurrence relation.
so the final answer is: \\boxed{{53}}.  End of answer.

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


