# Inference-Time Computation Strategies for LLM Reasoning

## 0. Overview

With the advancement of large language models (LLMs), solving complex reasoning tasks has gained increasing attention. Inference-time computation methods (e.g., Best-of-N, beam search) are particularly valuable as they enhance reasoning performance without modifying model parameters or requiring additional training. However, these techniques come with implementation challenges, and most existing methods remain at the proof-of-concept stage with limited practical adoption due to computational complexity and varying effectiveness across different tasks.

In this project, we investigate and benchmark diverse inference-time computation strategies across reasoning tasks of varying complexity. Since most current methods rely on a proposer-verifier pipeline that first generates candidate solutions and then selects the best one based on reward signals, our research focuses on optimizing both candidate solution generation (e.g., instructing prompts, hyperparameters such as temperature and top-p) and reward mechanisms (e.g., self-evaluation, reward types). Through extensive experiments (more than 20,000 A100-80G GPU hours with over 1,000 experiments) across a variety of models (e.g., Llama, Qwen, and Mistral families), our ablation studies reveal that previously overlooked strategies can significantly enhance performance. Furthermore, we establish a standardized benchmark for inference-time computation by systematically evaluating six representative methods across eight reasoning tasks.

## 1. Quick Start

### 1.1 Installation

```bash
# Clone the repository
git clone https://github.com/usail-hkust/benchmark_inference_time_computation_LLM

# Change directory to the cloned repository
cd benchmark_inference_time_computation_LLM

# Create a new conda environment with Python 3.12
conda create -n llm_reasoning python=3.12

# Activate the conda environment
conda activate llm_reasoning

# Install the required dependencies
pip install -r requirements.txt
```

### 1.2 Running the Experiment

#### 1.2.1 Preparation

- Ensure you have the necessary dependencies installed.
- Set up the required models before running experiments.

#### 1.2.1.1 Inference Model Pre-Preparation

Before running the experiments, ensure that the required models are properly set up. The following model paths need to be defined in `models/inference_model.py`:

```python
model_paths = {
    "llama-3.1-8b": "Meta-Llama-3.1-8B-Instruct",
    "llama-3.1-70b": "Meta-Llama-3.1-70B-Instruct",
    "Qwen2.5-7B": "Qwen2.5-7B-Instruct",
    "Qwen2.5-72B": "Qwen2.5-72B-Instruct",
    "Mistral-7B-Instruct-v0.3": "Mistral-7B-Instruct-v0.3",
    "QwQ-32B-Preview": "QwQ-32B-Preview",
    }
```

Ensure these paths are correctly configured to load the respective models before running any experiments.

#### 1.2.1.2 Reward Model Preparation

In addition to setting up inference models, ensure that the reward models are correctly defined in *`models/reward_models/intern_prm.py`*:

```python
self.model_paths = {
    "internlm2_5-step-prover-critic": "prm/internlm2_5-step-prover-critic",
    "internlm2-1_8b-reward": "internlm2-1_8b-reward",
}
```

These paths should be correctly set to ensure proper initialization of the reward models before running inference-time computations.



#### 1.2.2 Run the main experiment

Before executing the main inference-time computation strategies, ensure proper configuration of key parameters. This includes defining the backend model, task type, generation method, evaluation approach, and reward model. The reward model plays a crucial role in assessing the quality of generated responses and guiding the inference-time computation.

The process consists of two major steps:

1. **Launching the Reward Model Service:** This initializes the reward model and ensures it is ready for evaluation. It is executed as a FastAPI service running on a specified port.
2. **Performing Inference-Time Computation:** After the reward model is active, the inference-time computation process begins, utilizing various methods such as prompt sampling, reward-based evaluation, and optimized hyperparameters.

Below, we provide specific command-line examples to illustrate these steps in practice. The following parameters are used in the experiment:

#### Model and Task Settings

- `--backend`: Specifies the language model used for inference. Supported models include:
  - `gpt-4`, `gpt-3.5-turbo`, `gpt-4o`

  - `llama-3.1-405b`, `llama-3.1-70b`, `llama-3.1-8b`

  - `Qwen2.5-7B`, `Qwen2.5-72B`, `Mistral-7B-Instruct-v0.3`

  - `QwQ-32B-Preview`
- `--task`: Specifies the reasoning task to execute. Options include:
  - `bamboogle`, `strategyqa`, `hotpotqa`, `gsm8k`, `gsm_hard`, `MATH500`, `fever`, `prontoqa`, `humaneval`
- `--task_start_index` and `--task_end_index`: Define the range of data samples to process.

#### Prompt and Sampling Methods

- `--prompt_sample`: Determines the prompt type for inference. Options include:
  - `cot` (Chain-of-Thought)
  - `standard`
  - `reflect_cot`
- `--n_generate_sample`: Number of candidate solutions generated per query.
- `--n_evaluate_sample`: Number of solutions evaluated per query.

#### Evaluation and Reward Models

- `--method_evaluate`: The evaluation method applied, such as:
  - `qwq_as_process_reward`
  - `llm_as_reward_value`
  - `llm_as_critic_value`
- `--backend_prm`: Specifies the backend model used for reward evaluation. Examples include:
  - `QwQ-32B-Preview`, `internlm2-1_8b-reward`
- `--port`: Defines the port number where the reward model service runs.

#### Inference-Time Computation Methods

- `--baseline`: The inference-time computation technique applied. Options include:
  - `best_of_n`, `greedy`, `mcts`, `beam_search`, `ToT_dfs`, `naive`, `weighted_majority`

These parameters define how inference-time computation strategies interact with reward models to enhance LLM reasoning capabilities.



These parameters define how inference-time computation strategies interact with reward models to enhance LLM reasoning capabilities.

```bash
# Get the current timestamp
current_time=$(date +"%Y%m%d_%H%M%S")

log_file="serve_logs/run_serve1_reward_type_bamboogle_$current_time.log"

# Start the FastAPI service (run_serve.py) on port 8001
echo "Starting FastAPI service (run_serve.py)... port 8001"
sudo env CUDA_VISIBLE_DEVICES=0,1,2,3 python -m serves.run_serve --model QwQ-32B-Preview --port 8001 > "$log_file" 2>&1 &

# Wait for FastAPI service to start
echo "Waiting for FastAPI service to start..."
sleep 500  # Ensuring sufficient time for service startup

# Run the inference-time computation experiments
sudo env CUDA_VISIBLE_DEVICES=4,5,6,7 python -u run.py \
                                    --backend llama-3.1-8b \
                                    --task bamboogle \
                                    --task_start_index 0 \
                                    --task_end_index 126 \
                                    --prompt_sample cot \
                                    --method_evaluate qwq_as_process_reward \
                                    --backend_prm QwQ-32B-Preview \
                                    --port 8001 \
                                    --n_generate_sample 32 \
                                    --baseline best_of_n \
                                    ${@}

sudo env CUDA_VISIBLE_DEVICES=2,3,4,5 python -u run.py \
                                    --backend llama-3.1-8b \
                                    --task bamboogle \
                                    --task_start_index 0 \
                                    --task_end_index 126 \
                                    --prompt_sample cot \
                                    --method_evaluate llm_as_reward_value \
                                    --backend_prm internlm2-1_8b-reward \
                                    --port 8001 \
                                    --n_generate_sample 32 \
                                    --n_evaluate_sample 3 \
                                    --baseline best_of_n \
                                    ${@}

sudo env CUDA_VISIBLE_DEVICES=2,3,4,5 python -u run.py \
                                    --backend llama-3.1-8b \
                                    --task bamboogle \
                                    --task_start_index 0 \
                                    --task_end_index 126 \
                                    --prompt_sample cot \
                                    --method_evaluate llm_as_critic_value \
                                    --port 8002 \
                                    --n_generate_sample 32 \
                                    --n_evaluate_sample 3 \
                                    --baseline best_of_n \
                                    --trick_type reward_type \
                                    --backend_prm internlm2_5-step-prover-critic \
                                    ${@}
```

## 2. Benchmarking and Results

Our benchmarking evaluates inference-time computation across:

- **Six inference-time computation methods**
- **Eight reasoning tasks**
- **Multiple LLM architectures** (Llama, Qwen, Mistral, etc.)

Key findings include:

- **Instruction prompts significantly influence LLM reasoning**
- **Self-evaluation often struggles to assess solution quality**
- **Reward models can introduce performance inflation**
- **Hyperparameters like temperature and top-p affect performance by up to 5%**

## 3. Available Tasks

Our research focuses on the following reasoning tasks:

- **Arithmetic Reasoning:** Evaluating models on GSM8K and GSM-Hard datasets to test their arithmetic calculation skills.
- **Complex Mathematical Reasoning:** Using the MATH dataset to assess proficiency in solving advanced mathematical problems.
- **Logical Reasoning:** Measuring logical deduction and inference abilities with the ProntoQA dataset.
- **Code Generation:** Testing code generation skills on the HumanEval dataset.
- **Question Answering:** Evaluating performance in answering diverse questions using the Bamboogle dataset.
- **Fact Verification:** Assessing factual verification using the FEVER dataset.
- **Common Sense Reasoning:** Testing understanding of common sense knowledge and reasoning with the HotpotQA dataset.

To run a specific Trick:


**Example: Running the Temperature Trick (0.6 - 1.0)**

```bash
sudo python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample cot \
    --n_generate_sample 32 \
    --baseline majority \
    --trick_type temperature \
    --temperature 0.6 \
    ${@}
```

To modify the temperature, adjust the `--temperature` flag within the range 0.6 - 1.0.


**Example: Running the Top-P Trick (0.6 - 1.0)**

```bash
python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample cot \
    --n_generate_sample 32 \
    --baseline majority \
    --trick_type topp \
    --top_p 0.6 \
    ${@}
```

To modify the top-p value, adjust the `--top_p` flag within the range 0.6 - 1.0.



#### Example: Running the Self-Evaluation Trick

```bash
sudo python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample cot \
    --method_generate sample \
    --method_evaluate random \
    --n_generate_sample 32 \
    --n_evaluate_sample 3 \
    --baseline best_of_n \
    --trick_type self_evaluation \
    ${@}
```

```bash
sudo python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample cot \
    --method_generate sample \
    --method_evaluate self_process_value \
    --n_generate_sample 32 \
    --n_evaluate_sample 3 \
    --baseline best_of_n \
    --trick_type self_evaluation \
    ${@}
```

```bash
sudo python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample cot \
    --method_generate sample \
    --method_evaluate self_result_value \
    --n_generate_sample 32 \
    --n_evaluate_sample 3 \
    --baseline best_of_n \
    --trick_type self_evaluation \
    ${@}
```

This trick evaluates the model’s responses using self-assessment techniques such as `random`, `self_process_value`, and `self_result_value`.

#

#### Example: Running the Prompt Type Trick

```bash
sudo python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample standard \
    --method_select greedy \
    --n_generate_sample 32 \
    --baseline majority \
    --trick_type prompt \
    ${@}
```

```bash
sudo python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample cot \
    --n_generate_sample 32 \
    --baseline majority \
    --trick_type prompt \
    ${@}
```

```bash
sudo python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample reflect_cot \
    --n_generate_sample 32 \
    --baseline majority \
    --trick_type prompt \
    ${@}
```

This trick evaluates the effect of different prompt types such as `standard`, `cot`, and `reflect_cot` on model performance.


#

#### Example: Running the Reward Type Trick

```bash
# Get the current timestamp
current_time=$(date +"%Y%m%d_%H%M%S")

log_file="serve_logs/run_serve1_reward_type_bamboogle_$current_time.log"

# Start the FastAPI service (run_serve.py) on port 8001
echo "Starting FastAPI service (run_serve.py)... port 8001"
sudo env CUDA_VISIBLE_DEVICES=0,1,2,3 python  -m serves.run_serve --model QwQ-32B-Preview  --port 8001 > "$log_file" 2>&1 &

# Wait for FastAPI service to start
echo "Waiting for FastAPI service to start..."
sleep 500


echo "Starting FastAPI service (run_serve.py)... port 8002"
sudo env CUDA_VISIBLE_DEVICES=0 python  -m serves.run_serve  --model internlm2-1_8b-reward  --port 8001 > "$log_file" 2>&1 &


echo "Waiting for FastAPI service to start..."
sleep 10  


echo "Starting FastAPI service (run_serve.py)...port 8003"
sudo env CUDA_VISIBLE_DEVICES=1 python  -m serves.run_serve  --model internlm2_5-step-prover-critic --port 8002 > "$log_file" 2>&1 &


echo "Waiting for FastAPI service to start..."
sleep 10  




sudo env CUDA_VISIBLE_DEVICES=4,5,6,7 python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample cot \
    --method_generate sample \
    --method_evaluate qwq_as_process_reward \
    --backend_prm QwQ-32B-Preview \
    --port 8001 \
    --n_generate_sample 32 \
    --n_evaluate_sample 3 \
    --baseline best_of_n \
    --trick_type reward_type \
    ${@}
```

```bash
sudo env CUDA_VISIBLE_DEVICES=2,3,4,5 python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample cot \
    --method_generate sample \
    --method_evaluate llm_as_reward_value \
    --backend_prm internlm2-1_8b-reward \
    --port 8002 \
    --n_generate_sample 32 \
    --n_evaluate_sample 3 \
    --baseline best_of_n \
    --trick_type reward_type \
    ${@}
```

```bash
sudo env CUDA_VISIBLE_DEVICES=2,3,4,5 python -u run.py \
    --backend llama-3.1-8b \
    --task bamboogle \
    --task_start_index 0 \
    --task_end_index 126 \
    --prompt_sample cot \
    --method_generate sample \
    --method_evaluate llm_as_critic_value \
    --port 8003 \
    --n_generate_sample 32 \
    --n_evaluate_sample 3 \
    --baseline best_of_n \
    --trick_type reward_type \
    --backend_prm internlm2_5-step-prover-critic \
    ${@}
```

*This trick evaluates the effect of different reward model types on model performance, including `qwq_as_process_reward`, `llm_as_reward_value`, and `llm_as_critic_value`




## 4. Acknowledgements

We would like to express our gratitude to the [Princeton NLP Tree of Thought LLM project](https://github.com/princeton-nlp/tree-of-thought-llm) for their invaluable contributions.



## 5. Citation

If you find our work useful, please cite:

```bibtex
@misc{liu2025bagtricksinferencetimecomputation,
    title={Bag of Tricks for Inference-time Computation of LLM Reasoning}, 
    author={Fan Liu and Wenshuo Chao and Naiqiang Tan and Hao Liu},
    year={2025},
    eprint={2502.07191},
    archivePrefix={arXiv},
    primaryClass={cs.AI},
    url={https://arxiv.org/abs/2502.07191}, 
}
```