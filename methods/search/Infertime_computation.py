import numpy as np
from functools import partial
from models.base_model import gpt
import concurrent.futures
from collections import Counter
from methods.method_utils.str_utils import extract_last_question, extract_last_answer
from prompts.self_refine import *
from prompts.binary_evaluate import *
import random
import torch.nn as nn
import torch
class InferTimeComputation:
    def __init__(self, task, args):
        self.task = task
        self.args = args
        if self.args.baseline == 'naive':
            self.args.n_generate_sample = 1


        self.value_cache = {}
        self.memory = []
        self.args.score_criterion = 'min'  # or 'min' or 'max'
        self.args.max_node_depth = 8 
        self.max_memory_size = args.max_memory_size if hasattr(args, 'max_memory_size') else 100
        self.stop = "Step"
        #self.stop = "."
        # load inference model

        #print("vllm only use {gpu_memory_utilization}% GPU memory repctively for inference model".format(gpu_memory_utilization = args.inference_gpu_memory_utilization * 100)) 
        self.gpt = partial(gpt, model=args.backend, temperature=args.temperature, top_p=args.top_p, max_tokens=args.max_tokens, gpu_memory_utilization = args.inference_gpu_memory_utilization)

        # load reward model
        if args.method_evaluate not in ['value', 'vote',"random","self_process_value", "self_result_value"]:
            from models.reward_models.request_gpt import request_gpt
            if args.backend_prm.startswith("Xinternlm"):
                self.prm = partial(gpt, model=args.backend_prm)
            elif args.backend_prm == "gpt-4o" or args.backend_prm.startswith("llama") or args.backend_prm.startswith("Qwen2") or args.backend_prm.startswith("Mistral") or args.backend_prm.startswith("internlm") or args.backend_prm.startswith("QwQ"):
                self.prm = partial(request_gpt, model=args.backend_prm, temperature=args.temperature, max_tokens=args.max_tokens, port = args.port,gpu_memory_utilization = args.reward_gpu_memory_utilization)
        
    def generate_sentences(self, prompt, n_samples, stop=None):

        generated = self.gpt(prompt, n=n_samples, stop=stop)
        return [g.strip() for g in generated]
    
    def get_values(self, x, ys):
        # Extract the last question, avoiding the few-shot examples
        x = extract_last_question(x)

        # self evaluation
        if self.args.method_evaluate == "value":
            values = []
            for y in ys:
                value_prompt = self.task.value_prompt_wrap(x, y)
                if value_prompt in self.value_cache:
                    value = self.value_cache[value_prompt]
                else:
                    value_outputs = self.gpt(value_prompt, n=self.args.n_evaluate_sample, stop= "End of answer.")
                    value = self.task.value_outputs_unwrap(x, y, value_outputs)
                    self.value_cache[value_prompt] = value
                values.append(value)

        elif self.args.method_evaluate == "self_process_value":
            values = []
            for y in ys:
                value_prompt = self.task.self_process_value_prompt_wrap(x, y)
                if value_prompt in self.value_cache:
                    value = self.value_cache[value_prompt]
                else:
                    value_outputs = self.gpt(value_prompt, n=self.args.n_evaluate_sample, stop= "End of answer.")
                    value = self.task.value_outputs_unwrap(x, y, value_outputs)
                    self.value_cache[value_prompt] = value
                values.append(value)
        elif self.args.method_evaluate == "self_result_value":
            values = []
            for y in ys:
                y = self.task.extract_answer(y).replace(': ', '').strip()
                value_prompt = self.task.self_result_value_prompt_wrap(x, y)
                if value_prompt in self.value_cache:
                    value = self.value_cache[value_prompt]
                else:
                    value_outputs = self.gpt(value_prompt, n=self.args.n_evaluate_sample, stop= "End of answer.")
                    value = self.task.value_outputs_unwrap(x, y, value_outputs)
                    self.value_cache[value_prompt] = value
                values.append(value)
        elif self.args.method_evaluate == "random":
            values = [random.uniform(0, 1) for _ in ys]

        #backen_model:  llm_as_binary, llm_as_critical， llm_as_process_reward, llm_as_reuslt_reward
        elif self.args.method_evaluate == "llm_as_binary":
            values = []
            for y in ys:
                value_prompt = binary_evaluate + x + '\nThought Process: ' + y + '\nEvaluation Process:\n'
                if value_prompt in self.value_cache:
                    value = self.value_cache[value_prompt]
                else:
                    value_outputs = self.prm(value_prompt, n=self.args.n_evaluate_sample, stop= "End of answer.")
                    value = binary_evaluate_unwrap(value_outputs=value_outputs)
                    self.value_cache[value_prompt] = value
                values.append(value)
        elif self.args.method_evaluate == "llm_as_process_reward":
            values = []
            for y in ys:
                value_prompt = self.task.self_process_value_prompt_wrap(x, y)
                if value_prompt in self.value_cache:
                    value = self.value_cache[value_prompt]
                else:
                    value_outputs = self.gpt(value_prompt, n=self.args.n_evaluate_sample, stop= "End of answer.")
                    value = self.task.value_outputs_unwrap(x, y, value_outputs)
                    self.value_cache[value_prompt] = value
                values.append(value)
        elif self.args.method_evaluate == "qwq_as_process_reward":
            values = []
            for y in ys:
                value_prompt = self.task.self_process_value_prompt_wrap(x, y)
                if value_prompt in self.value_cache:
                    value = self.value_cache[value_prompt]
                else:
                    value_outputs = self.prm(value_prompt, n=self.args.n_evaluate_sample, stop= "End of answer.")
                    value = self.task.value_outputs_unwrap(x, y, value_outputs)
                    self.value_cache[value_prompt] = value
                values.append(value)
        elif self.args.method_evaluate == "llm_as_reuslt_reward":
            values = []
            for y in ys:
                y = self.task.extract_answer(y).replace(': ', '').strip()
                value_prompt = self.task.self_result_value_prompt_wrap(x, y)
                if value_prompt in self.value_cache:
                    value = self.value_cache[value_prompt]
                else:
                    value_outputs = self.gpt(value_prompt, n=self.args.n_evaluate_sample, stop= "End of answer.")
                    value = self.task.value_outputs_unwrap(x, y, value_outputs)
                    self.value_cache[value_prompt] = value
                values.append(value)
        elif self.args.method_evaluate == "llm_as_reward_value" or "llm_as_critic_value":
            if self.args.backend_prm.startswith("internlm"):
                chat_batch = [[{"role": "user", "content": x}, {"role": "assistant", "content": y}]
                    for y in ys]
                values = self.prm(prompt=chat_batch)
                #print("values:", values)
            else:
                raise NameError(f"Unknown backend model: {self.args.backend_prm}")

        else:
            raise NameError(f"Unknown evaluation method: {self.args.method_evaluate}")

        return values

    def solve(self, x, idx, to_print=True):
        if self.args.baseline == 'naive':
            return self.solve_naive(x, idx, to_print)
        elif self.args.baseline == 'greedy':
            return self.solve_greedy(x, idx, to_print)
        elif self.args.baseline == 'majority':
            return self.solve_majority(x, idx, to_print)
        elif self.args.baseline == 'weighted_majority':
            return self.solve_best_of_n_with_weighted_voting(x, idx, to_print)
        elif self.args.baseline == 'best_of_n':
            return self.solve_best_of_n(x, idx, to_print)
        elif self.args.baseline == 'mcts':
            return self.solve_mcts(x, idx, to_print)
        elif self.args.baseline == 'beam_search':
            return self.solve_beam_search(x, idx, to_print)
        elif self.args.baseline == 'ToT_dfs':
            return self.solve_dfs(x, idx, to_print)
        elif self.args.baseline == 'self_refine':
            return self.solve_self_refine(x, idx, to_print)
        else:
            raise ValueError(f"Unknown method: {self.args.method}")
            
    def solve_naive(self, x, idx, to_print=True):
        if self.args.prompt_sample == 'standard':
            current_prompt = self.task.standard_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'cot':
            current_prompt = self.task.cot_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'reflect_cot':
            current_prompt = self.task.reflect_cot_prompt_wrap(x, "")
        else:
            raise NameError
        
        step_data = []
        total_token_count = 0
        step_index = 1
        candidates = self.generate_sentences(current_prompt, self.args.n_generate_sample, stop= "End of answer.")
        final_answer = candidates[0].strip()
        if to_print:
            print(final_answer)
        return [final_answer], {'steps': step_data}
    
    def solve_majority(self, x, idx, to_print=True, max_retry=5):
        retry_count = 0

        while retry_count < max_retry:
            # Generate the prompt based on the selected mode
            if self.args.prompt_sample == 'standard':
                current_prompt = self.task.standard_prompt_wrap(x, "")
            elif self.args.prompt_sample == 'cot':
                current_prompt = self.task.cot_prompt_wrap(x, "")
            elif self.args.prompt_sample == 'reflect_cot':
                current_prompt = self.task.reflect_cot_prompt_wrap(x, "")
            else:
                raise ValueError("Invalid prompt_sample mode.")

            # Generate candidate answers
            candidates = self.generate_sentences(
                current_prompt, 
                self.args.n_generate_sample, 
                stop="End of answer."
            )

            # Prepare the info dictionary to store each candidate and its value
            info = []
            for candidate in candidates:
                info.append({"prompt": x, "candidate": candidate})

            # Extract and clean answers from the candidates
            extracted_answers = [
                self.task.extract_answer(candidate).replace(': ', '').strip()
                for candidate in candidates
            ]

            # Count occurrences of each extracted answer
            answer_counts = Counter(extracted_answers)

            # Ensure no empty answers ("") are selected as the final answer
            sorted_answers = answer_counts.most_common()
            most_common_answer = None

            for answer, _ in sorted_answers:
                if answer != "":  # Skip empty answers
                    most_common_answer = answer
                    break

            if most_common_answer:
                # Find the first candidate corresponding to the most common extracted answer
                matching_candidate = next(
                    candidate for candidate, extracted_answer in zip(candidates, extracted_answers)
                    if extracted_answer == most_common_answer
                )

                # Optional: Print the matching candidate
                if to_print:
                    print(matching_candidate)

                return [matching_candidate], {'info': info}

            # If no valid answer is found, increment retry count and try again
            retry_count += 1
            print(f"Retrying... ({retry_count}/{max_retry})")

        # If retries are exhausted, return the final answer string
        print("Maximum retries reached. Returning final answer.")
        return ["the final answer is "], {'info': info}
    import numpy as np

    def solve_best_of_n_with_weighted_voting(self, x, idx, to_print=True):
        # Generate the prompt based on the selected mode
        if self.args.prompt_sample == 'standard':
            current_prompt = self.task.standard_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'cot':
            current_prompt = self.task.cot_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'reflect_cot':
            current_prompt = self.task.reflect_cot_prompt_wrap(x, "")
        else:
            raise ValueError("Invalid prompt_sample mode. Must be 'standard' or 'cot'.")

        # Generate N candidate solutions
        N = self.args.n_generate_sample  # Number of candidates
        candidates = self.generate_sentences(current_prompt, N, stop="End of answer.")

        # Extract answers from candidates
        extracted_answers = [
            self.task.extract_answer(candidate).replace(': ', '').strip()
            for candidate in candidates
        ]

        # Evaluate candidates
        values = self.get_values(x, candidates)

        # If all values are the same, avoid division by zero and handle it
        min_value = np.min(values)
        max_value = np.max(values)

        if max_value == min_value:
            # All values are the same, so we assign equal weight to all candidates
            normalized_values = [1.0 for _ in values]
        else:
            # Normalize the values between 0 and 1
            normalized_values = [(v - min_value) / (max_value - min_value) for v in values]

        # Aggregate votes with normalized weights
        weighted_votes = {}
        for idx, answer in enumerate(extracted_answers):
            weight = normalized_values[idx]  # Get the normalized weight of the candidate
            if answer in weighted_votes:
                weighted_votes[answer] += weight  # Add weight to the total for this answer
            else:
                weighted_votes[answer] = weight  # Initialize weight for this answer

        # Select the answer with the highest total weighted vote
        most_voted_answer = max(weighted_votes, key=weighted_votes.get)

        # Filter candidates that match the most voted answer
        matching_candidates = [
            candidates[i] for i, ans in enumerate(extracted_answers) if ans == most_voted_answer
        ]
        
        # Evaluate these matching candidates and select the one with the best value
        matching_values = [values[i] for i, ans in enumerate(extracted_answers) if ans == most_voted_answer]
        best_idx = np.argmax(np.array(matching_values))

        best_candidate = matching_candidates[best_idx]
        best_value = matching_values[best_idx]

        # Prepare the info dictionary to store each candidate, its value, and extracted answer
        info = []
        for candidate, value, extracted_answer in zip(candidates, values, extracted_answers):
            info.append({"x": x, "candidate": candidate, "value": value, "extracted_answer": extracted_answer})

        if to_print:
            print(f"Best candidate with value {best_value} and extracted answer '{most_voted_answer}':\n{best_candidate}")
            # Print all candidates and their corresponding values
            print("\nAll candidates and their values:")
            for candidate_value in info:
                value = candidate_value.get("value")
                candidate = candidate_value.get("candidate")
                extracted_answer = candidate_value.get("extracted_answer")
                print(f"Value: {value} -> Candidate: {candidate} (Extracted answer: {extracted_answer})")

        # Return the best candidate and the info dictionary
        return [best_candidate], {'info': info}

    def solve_greedy(self, x, idx, to_print=True):
        if self.args.prompt_sample == 'standard':
            current_prompt = self.task.standard_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'cot':
            current_prompt = self.task.cot_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'reflect_cot':
            current_prompt = self.task.reflect_cot_prompt_wrap(x, "")
        else:
            raise NameError
        step_data = []
        step_index = 0
        current_solution = ""
        while True:
            # Generate N candidate sentences in batch
            N = self.args.n_generate_sample
            retry_count = 0
            max_retry = 2
            while retry_count <= max_retry:
                candidates = self.generate_sentences(current_prompt, self.args.n_generate_sample, stop='Step')
                valid_candidates = []
                for candidate in candidates:
                    if "Question" in candidate or candidate.count("Answer:") > 2:
                        continue
                    valid_candidates.append(candidate)
                if valid_candidates:
                    candidates = valid_candidates
                    break
                retry_count += 1
            if retry_count > max_retry:
                candidates = [candidate.split("Question")[0] for candidate in candidates]


            values = self.get_values(x, [current_solution + " " + candidate for candidate in candidates])
            best_idx = np.argmax(np.array(values))
            best_candidate = candidates[best_idx]
            best_score = values[best_idx]

            # Append to current prompt
            current_prompt += " " + best_candidate
            current_solution += " " + best_candidate
            # Record step information
            step_info = {
                "step": step_index,
                "candidates": [{"candidate": c, "score": v} for c, v in zip(candidates, values)],
                "best_candidate": best_candidate,
                "best_solution": current_solution,
                "best_score": best_score
            }
            step_data.append(step_info)

            # Update memory with assessments
            # self.update_memory([assessments[best_idx]])

            if to_print:
                print(f"\n--- Step {step_index} ---")
                print("Best Candidate:")
                print(best_candidate)
                print("\nCurrent Solution:")
                print(current_solution)
                print("-" * 40)
         
            # Check for stopping condition
            if "answer is" in best_candidate or "final answer is" in best_candidate or "End of answer." in best_candidate or step_index >= 20:
                break

            step_index += 1

        # Process the final answer
        
        final_answer = current_solution.strip()
        return [final_answer], {'steps': step_data}



    def solve_best_of_n(self, x, idx, to_print=True):
        # Generate the prompt based on the selected mode
        if self.args.prompt_sample == 'standard':
            current_prompt = self.task.standard_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'cot':
            current_prompt = self.task.cot_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'reflect_cot':
            current_prompt = self.task.reflect_cot_prompt_wrap(x, "")
        else:
            raise ValueError("Invalid prompt_sample mode. Must be 'standard' or 'cot'.")

        # Generate N candidate solutions
        N = self.args.n_generate_sample  # Number of candidates
        candidates = self.generate_sentences(current_prompt, N, stop= "End of answer.")

        # Evaluate candidates
        values = self.get_values(x, candidates)

        # Select the best candidate
        best_idx = np.argmax(np.array(values))

        best_candidate = candidates[best_idx]
        best_value = values[best_idx]

        # Prepare the info dictionary to store each candidate and its value
        info = []
        for candidate, value in zip(candidates, values):
            info.append({"x":x,"candidate": candidate, "value": value})

        if to_print:
            print(f"Best candidate with value {best_value}:\n{best_candidate}")
            # Print all candidates and their corresponding values
            print("\nAll candidates and their values:")
            for candidate_value in info:
                value = candidate_value.get("value")
                candidate = candidate_value.get("candidate")
                print(f"Value: {value} -> Candidate: {candidate}")

        # Return the best candidate and the info dictionary
        return [best_candidate], {'info': info}
    


    def solve_self_refine(self, x, idx, to_print=True):
        if self.args.prompt_sample == 'standard':
            initial_prompt = self.task.standard_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'cot':
            initial_prompt = self.task.cot_prompt_wrap(x, "")
        else:
            raise ValueError("Invalid prompt_sample mode. Must be 'standard' or 'cot'.")
        initial_prompt += "Answer: Step"
        num_iteration = getattr(self.args, 'num_iteration', 3)
        current_ans = self.generate_sentences(initial_prompt, 1)[0].strip()
        step = [{"iteration": 0, "answer": current_ans, "feedback": None}]
        info = []
        info.append(step[0])
        for i in range(num_iteration):
            feedback_ans = self.generate_sentences(feedback_prompt.format(question=x, solution=current_ans), 1)[0].strip()
            if 'No error' in feedback_ans:
                break
            current_ans = self.generate_sentences(refine_prompt.format(question=x, solution=current_ans, feedback=feedback_ans), 1)[0].strip()
    
            info.append({"iteration": i + 1,"answer": current_ans, "feedback": feedback_ans, "revised_answer": current_ans})
            if to_print:
                print(f"--- Iteration {i + 1} ---")
                print(f"Feedback: {feedback_ans}")
                print(f"Revised version: {current_ans}")
                print("-------------------------")

        return [current_ans], {'info': info}

        
    def solve_beam_search(self, x, idx, to_print=True):
        # Generate the initial prompt
        if self.args.prompt_sample == 'standard':
            initial_prompt = self.task.standard_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'cot':
            initial_prompt = self.task.cot_prompt_wrap(x, "")
        else:
            raise ValueError("Invalid prompt_sample mode. Must be 'standard' or 'cot'.")
        initial_prompt+= "Answer: Step"
        temp_dict = {}
        beam_width = self.args.n_select_sample  # Beam width
        max_depth = getattr(self.args, 'max_node_depth', 20)  # Max steps
        n_generate_sample = getattr(self.args, 'n_generate_sample', 5)  # Candidates per beam

        beams = [ (initial_prompt , "", [0]) ]  # Each beam is (prompt, , cumulative_score)
        completed_beams = []
        step_data = []

        for depth in range(max_depth):
            if len(beams) < 1:
                break
            all_candidates = []
            for prompt, cand, score in beams:
                # Generate possible continuations
                new_prompt = prompt + " " + cand
                candidates = self.generate_sentences(new_prompt, n_generate_sample, stop=self.stop)
                current_solutions = [extract_last_answer(new_prompt + " " + candidate) for candidate in candidates]

                values = self.get_values(x, current_solutions)
                # Combine current score with candidate values
                for candidate, value in zip(candidates, values):
                    if candidate in temp_dict:
                        continue  # Skip if this candidate has already been generated
                    temp_dict[new_prompt + " " + candidate] = True  # Mark candidate as generated
                    new_score = score + [value]
                    all_candidates.append( (new_prompt, candidate, new_score) )
            # Keep the top beam_width beams
            if self.args.score_criterion == 'max':
                all_candidates.sort(key=lambda x: -x[2][-1])
            else:
                all_candidates.sort(key=lambda x: -max(x[2]))
            beams = all_candidates[:beam_width]
            # Record step information
            step_info = {
                "step": depth,
                "beams": [
                    {"prompt": beam[0], "cand": beam[1], "score": beam[2]} for beam in beams
                ]
            }
            step_data.append(step_info)
            # Check for completion
            remaining_beams = []
            for prompt, cand, score in beams:
                if "\boxed{" in cand or "\\boxed{" in cand or "answer is" in cand or "final answer is" in cand or "End of answer." in cand:
                    completed_beams.append((prompt, cand, score))
                else:
                    remaining_beams.append((prompt, cand, score))
            
            beams = remaining_beams  # Only keep unfinished beams

            if to_print:
                print(f"\n--- Step {depth} ---")
                for beam in beams:
                    print(f"PROMPT: {beam[0]}\nCANDIDATE: {beam[1]}\nSCORE: {beam[2]}")
                    print("=" * 40)
                print("-" * 40)

        # Select the best completed beam
        if completed_beams:
            if self.args.score_criterion == 'max':
                best_prompt, candid, best_score = max(completed_beams, key=lambda x: x[2][-1])
            else:
                best_prompt, candid, best_score = max(completed_beams, key=lambda x: max(x[2]))
        else:
            beams = step_info['beams']
            # No completed beam, take the best current beam
            if self.args.score_criterion == 'max':
                ans = max(beams, key=lambda x: max(x["score"]))
                best_prompt, candid, best_score = ans['prompt'], ans['cand'], ans['score']
            else:
                ans = max(beams, key=lambda x: max(x["score"]))
                best_prompt, candid, best_score = ans['prompt'], ans['cand'], ans['score']
        if to_print:
            print(f"Best beam with score {best_score}:\n{best_prompt} {candid}")
        ys = extract_last_answer(best_prompt + " " + candid)
        return [ys], {'steps': step_data}

    def solve_mcts(self, x, idx, to_print=True):
        '''
        Follow the paper: AlphaZero-Like Tree-Search can Guide Large Language Model Decoding and Training
        
        Only mcts_alpha is usable
        '''
        if self.args.prompt_sample == 'standard':
            initial_prompt = self.task.standard_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'cot':
            initial_prompt = self.task.cot_prompt_wrap(x, "")
        else:
            raise ValueError("Invalid prompt_sample mode. Must be 'standard' or 'cot'.")
        initial_prompt+= "Answer: Step"
        # Set the root node with initial state and depth
        root = MCTSNode(state=initial_prompt, depth=0)
        num_simulation = getattr(self.args, 'num_simulation', 5)
        max_depth = getattr(self.args, 'max_depth', 8)
        sample_action = getattr(self.args, 'sample_action', False)
        c_base = getattr(self.args, 'c_base', 19652)
        c_init = getattr(self.args, 'c_puct', 1.25)
        n_generate_sample = getattr(self.args, 'n_generate_sample', 5)

        # Perform MCTS search
        solution_node = self.mcts_alpha_search(
            root, 
            n_generate_sample, 
            num_simulation, 
            c_base, 
            c_init, 
            max_depth, 
            sample_action, 
            to_print
        )

        # Build solution from final node upward
        solution = solution_node.state
        steps = []
        info = []
        node = solution_node

        # Collect path and node info
        while node:
            child_info = []
            for child in node.children:
                q_value = child.total_value / (child.visits + 1e-6)
                child_info.append({
                    'child_action': child.action,
                    'child_state': child.state,
                    'value': child.total_value,
                    'visits': child.visits,
                    'q_value': q_value
                })
            info.insert(0, {
                'depth': node.depth,
                'action': node.action,
                'state': node.state,
                'value': node.total_value,
                'visits': node.visits,
                'children': child_info
            })
            steps.insert(0, node.action)
            node = node.parent

        if to_print:
            for i, layer in enumerate(info[::-1]):
                print("---------- DEPTH:", layer['depth'], "----------")
                print("ACTION:", layer['action'])
                print("STATE:", layer['state'])
                print("CHILDREN:")
                for c in layer['children']:
                    print("   ACTION:", c['child_action'])
                    print("   STATE:", c['child_state'])
                print("----------------------------------------")
        ys = extract_last_answer(solution)
        if to_print:
            print(f"FINAL SOLUTION:\n{ys}")

        return [ys], {'steps': steps, 'info': info}
    
    def mcts_alpha_search(self, root, n_generate_sample, num_simulation, c_base, c_init, max_depth, sample_action, to_print):
        """
        Perform MCTS-Alpha search.
        """
        
        def action(node):
            temperature = 1.0
            action_visits = []
            for action in node.children:
                action_visits.append((action, action.visits))
            actions, visits = zip(*action_visits)
            action_probs = nn.functional.softmax(1.0/ temperature* np.log(torch.as_tensor(visits, dtype=torch.float32) + 1e-10), dim=0,).numpy()
            if sample_action:
                action = np.random.choice(actions, p=action_probs)
                # self.reset_prior(root)
            else:
                action = actions[np.argmax(action_probs)]
            return action
        current_node = root
        if not root.is_fully_expanded():
            self.expand(current_node, n_generate_sample)
        
        while not current_node.is_terminal():
            # Simulate Phase
            for n in range(num_simulation):
                node = current_node
                while node.is_fully_expanded() and not node.is_terminal():
                    if node.depth >= max_depth:
                        if to_print:
                            print(f"Reached maximum depth of {max_depth}. Stopping expansion at this node.")
                        break
                    node = self.select_best_child(node, c_base, c_init)
                # Expansion Phase
                    if not node.is_terminal() and node.depth <= max_depth:
                        new_node = self.expand(node, n_generate_sample)
                        # Backpropagation Phase
                        self.backpropagate(new_node, new_node.MC_estimate)
            try:
                current_node = action(current_node)
                print("Do Action: ", current_node.action)
            except:
                print("Fail Action, The final current_node is: ", current_node.action)
                break
        return current_node # Choose the best child without exploration



    
    
    def solve_dfs(self, x, idx, to_print=True):
        """
        Perform Depth-First Search (DFS) to explore possible solutions.

        Args:
            root (MCTSNode): The root node to start DFS from.
            max_depth (int): The maximum depth to search.
            to_print (bool): Whether to print intermediate results.

        Returns:
            str: The best solution found during the DFS.
        """
        if self.args.prompt_sample == 'standard':
            initial_prompt = self.task.standard_prompt_wrap(x, "")
        elif self.args.prompt_sample == 'cot':
            initial_prompt = self.task.cot_prompt_wrap(x, "")
        else:
            raise ValueError("Invalid prompt_sample mode. Must be 'standard' or 'cot'.")

        max_depth = getattr(self.args, 'max_depth', 8)
        value_thresh = getattr(self.args, 'value_thresh', 0.3)
        prune_ratio = getattr(self.args, 'prune_ratio', 0.4)
        num_paths = getattr(self.args, 'num_paths', 3)
        root = MCTSNode(state=initial_prompt, depth=0)

        stack = [(root, 0)]
        best_solution = None
        best_score = -float('inf') if self.args.score_criterion == 'max' else float('inf')
        path = []
        info = []

        if to_print:
            print("---------- Starting DFS ----------")
            print(f"Initial Prompt:\n{initial_prompt}\n-----------------------------------")

        while stack:
            current_node, depth = stack.pop()
            
            if to_print:
                print(f"VISITING DEPTH {depth}:")
                print(f"CURRENT NODE STATE:\n{current_node.state}")
                print("-----------------------------------")

            # Check terminal or depth
            if current_node.is_terminal():
                path.append(current_node)
                if current_node.MC_estimate is not None:
                    if self.args.score_criterion == 'max':
                        if current_node.MC_estimate > best_score:
                            best_score = current_node.MC_estimate
                            best_solution = current_node
                    else:  # 'min'
                        if current_node.MC_estimate < best_score:
                            best_score = current_node.MC_estimate
                            best_solution = current_node
                continue
            if depth >= max_depth:
                continue
            if len(path) >= num_paths:
                continue

            # Expand current node
            if not current_node.is_fully_expanded():
                self.expand(current_node, self.args.n_generate_sample)

            children = current_node.children
            # Sort children for better paths first
            children.sort(key=lambda c: -c.MC_estimate)

            if to_print and children:
                print("CHILDREN (SORTED BY MC_ESTIMATE):")
                for child in children:
                    print(f"CHILD ACTION: {child.action} | ESTIMATE: {child.MC_estimate}")
                print("-----------------------------------")

            # Prune and push to stack
            keep_count = int((1 - prune_ratio) * len(children))
            for i, child in enumerate(children):
                if i > keep_count:
                    break
                if child.MC_estimate < value_thresh and len(path) != 0:
                    continue
                stack.append((child, depth + 1))

            # Record info for each depth
            info.append({
                'depth': depth,
                'state': current_node.state,
                'children': [{'action': child.action, 'estimate': child.MC_estimate} for child in children]
            })

        # Aggregate Path
        best_path = None
        best_solution_str = ''
        best_value_hist = [-float('inf')]

        for solution in path:
            steps = []
            value_hist = []
            node = solution
            while node:
                steps.insert(0, node.action)
                value_hist.insert(0, node.MC_estimate)
                node = node.parent

            if sum(best_value_hist)/len(best_value_hist) < sum(value_hist)/len(value_hist):
                best_path = steps
                best_solution_str = solution.state
                best_value_hist = value_hist

        ys = extract_last_answer(best_solution_str)

        if to_print:
            print(f"---------- DFS COMPLETE ----------")
            print(f"BEST SOLUTION FOUND WITH AVERAGE SCORE {sum(best_value_hist)/len(best_value_hist):.3f}:")
            print("SOLUTION PATH:")
            for step in best_path:
                print(f"{step}")
            print("-----------------------------------")

        return [ys], {'info': info, 'best_path': best_path}

    def select_best_child(self, node, c_base=19652, c_init=1.25):
        """
        Select the best child using refined PUCT formula.
        The cpuct is dynamically adjusted based on the number of total visits.
        """
        best_value = -float('inf')
        best_child = None

        for child in node.children:
            q_value = child.total_value / (child.visits + 1e-6)  # Mean value of the child
            u_value = ((c_init + np.log((node.visits + c_base + 1) / c_base)) 
                       * np.sqrt(node.visits) / (1 + child.visits))
            puct_value = q_value + u_value

            if puct_value > best_value:
                best_value = puct_value
                best_child = child

        return best_child

    def expand(self, node, n_generate_sample):
        """
        Expand the given node by sampling its children based on a temperature-scaled 
        probability distribution proportional to the value function.

        Args:
            node (MCTSNode): The current node to expand.
            n_generate_sample (int): Number of actions to generate.

        Returns:
            MCTSNode: The selected child node based on the sampling probability.
        """

        print("\n===== Starting Expand =====")
        print(f"Expanding node at depth {node.depth}")
        print(f"Generating up to {n_generate_sample} candidate actions")

        # Generate children if none exist
        if len(node.children) == 0:
            actions = self.generate_sentences(node.state, n_generate_sample, stop=self.stop)
            hist_actions = {}
            # Initialize child nodes and collect their values
            for action in actions:
                if hist_actions.get(action):
                    hist_actions[action] += 1
                    continue
                else:
                    hist_actions[action] = 1

                next_state = node.state + " " + action
                child_node = MCTSNode(state=next_state, parent=node, action=action, depth=node.depth + 1)

                print("\n===== Next State =====")
                print(next_state)
                print("======================")

                x = extract_last_question(next_state)
                ys = extract_last_answer(x)
                if "Answer" in x:
                    x = x.split("Answer")[0]

                print("\n===== Extracted X =====")
                print(x)
                print("======================")

                print("\n===== Extracted YS =====")
                print(ys)
                print("======================")
               
                mc_estimate = self.get_values(x,  [ys])[0]

                print("\n===== Value Outputs =====")
                print("MC Estimate:", mc_estimate)
                print("=========================")

                child_node.MC_estimate = mc_estimate
                child_node.rollout_length = node.rollout_length + 1

                # Store child node and its value
                node.expand(action, child_node)

        return random.choice(node.children)

    def simulate(self, state, current_depth, max_depth):
        current_state = state
        depth = current_depth
        total_reward = 0.0
        step_rewards = []
        action = ""

        while "\\boxed{" not in action or "answer is" not in action or "final answer is" not in action or "End of answer." not in action or depth < max_depth:
            # Generate possible actions
            action = self.generate_sentences(current_state, 1)
            # print("Action:", action)
            action = action[0]
            if not action:
                break  # No further actions possible

            
            
            x = extract_last_question(current_state + " " + action)
            ys = extract_last_answer(x)
            if "Answer" in x:
                x = x.split("Answer")[0]
            # Evaluate the current state using the reward model
            reward = self.get_values(x,  [ys])
            current_state += " " + action

            if len(reward)!=0:
                total_reward += reward[0]
            step_rewards.append(reward)
            depth += 1

        return total_reward, step_rewards, current_state

    def backpropagate(self, node, value):
        while node is not None:
            node.visits += 1
            # Update Q(s, a) incrementally
            node.total_value += value
            node.value = node.total_value / node.visits
            node = node.parent

    def sample_action_based_on_visits(self, node):

        probabilities = [child.visits / node.visits for child in node.children]
        return random.choices(node.children, probabilities)[0]


# Update the MCTSNode class to include depth
class MCTSNode:
    def __init__(self, state, parent=None, action="", depth=0):
        self.state = state  # The current solution (partial or complete)
        self.parent = parent
        self.action = action  # The action that led to this state (the last sentence added)
        self.children = []
        self.visits = 0
        self.mean_value = 0.0  # Cumulative value from simulations (Q-value)
        self.total_value = 0.0
        self.untried_actions = None  # Actions (sentences) that can be tried from this state
        self.depth = depth  # Depth of the node in the tree
        self.MC_estimate = 0.0  # Monte Carlo estimation of correctness (for Omega MCTS)
        self.rollout_length = 0  # Length of the rollout from this node

    def is_fully_expanded(self):
        return len(self.children)>0  # No more actions to try

    def is_terminal(self):
        return "\\boxed{" in self.action or "answer is" in self.action or "final answer is" in self.action or "End of answer." in self.action

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.total_value / child.visits) + c_param * np.sqrt((2 * np.log(self.visits) / child.visits))
            if child.visits > 0 else 0
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def expand(self, action, child_node):
        self.children.append(child_node)