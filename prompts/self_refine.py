feedback_prompt = '''Task: There might be one or multiple errors in the solution for the question due to a lack of understanding of the question. To find the error(s), analyze the intermediate steps and provide the feedback. Write "End of answer." when the feedback is complete.  
If the solution has no errors, say "No error."  

Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?  
Solution: Step 1, Natalia sold 48 x 2 = 96 clips in May. Step 2: Natalia sold 48 + 96 = 144 clips altogether in April and May. Step 3: so the final answer is: 144. End of answer.  
Feedback:  
There is an error in Step 1. The solution incorrectly multiplies 48 by 2 instead of dividing it by 2 to calculate the number of clips Natalia sold in May. End of answer.  

Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?  
Solution: Step 1, Natalia sold 48 / 2 = 24 clips in May. Step 2: Natalia sold 48 + 24 = 72 clips altogether in April and May. Step 3: so the final answer is: 72. End of answer.  
Feedback:  
No error. End of answer.  

Question: {question}  
Solution: {solution}  
Feedback:  
'''

refine_prompt = '''TTask: Given the feedback on the question and solution pair, refine the reasoning process to provide the corrected solution.  
Ensure the refined solution follows the same format as the original Solution. Write "End of answer." when the refined solution is complete.  

Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?  
Solution: Step 1, Natalia sold 48 x 2 = 96 clips in May. Step 2: Natalia sold 48 + 96 = 144 clips altogether in April and May. Step 3: so the final answer is: 144. End of answer.  
Feedback:  
There is an error in Step 1. The solution incorrectly multiplies 48 by 2 instead of dividing it by 2 to calculate the number of clips Natalia sold in May. End of answer.  
New Solution:  
Step 1, Natalia sold 48 / 2 = 24 clips in May. Step 2: Natalia sold 48 + 24 = 72 clips altogether in April and May. Step 3: so the final answer is: 72. End of answer.  

Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?  
Solution: Step 1, Natalia sold 48 + 2 = 50 clips in May. Step 2: Natalia sold 48 + 50 = 98 clips altogether in April and May. Step 3: so the final answer is: 98. End of answer.  
Feedback:  
There is an error in Step 1. The solution incorrectly adds 2 to 48 instead of dividing 48 by 2 to calculate the number of clips Natalia sold in May. End of answer.  
New Solution:  
Step 1, Natalia sold 48 / 2 = 24 clips in May. Step 2: Natalia sold 48 + 24 = 72 clips altogether in April and May. Step 3: so the final answer is: 72. End of answer.  

Question: {question}  
Solution: {solution}  
Feedback: {feedback}  
New Solution:  
'''