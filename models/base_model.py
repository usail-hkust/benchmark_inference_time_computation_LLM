import os
import openai
import backoff
import time
import traceback
import re
from  models.reward_models.intern_prm import PRM


completion_tokens = 0
prompt_tokens = 0


# Try importing LlamaModel; if not available, set it to None
try:
    from models.open_models.inference_model import Model
except ImportError:
    Model = None  # LlamaModel is not available in this environment


open_model_instance = None
reward_model_instance = None

def initialize_model(model_name="llama-2-7b",gpu_memory_utilization =0.9):
    global open_model_instance, reward_model_instance
    if model_name.startswith("llama-") or model_name.startswith("Qwen2") or model_name.startswith("Mistral")   or model_name.startswith("QwQ"):
        
        if open_model_instance is None:
            open_model_instance = Model(model_name=model_name,gpu_memory_utilization= gpu_memory_utilization)
        model_instance = open_model_instance
    elif model_name.startswith("internlm"):
        if reward_model_instance is None:
            reward_model_instance = PRM(model_name=model_name)
        model_instance = reward_model_instance
    return model_instance




api_key = os.getenv("OPENAI_API_KEY", "")
if api_key:
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY is not set")

api_base = os.getenv("OPENAI_API_BASE", "")
if api_base:
    print(f"Warning: OPENAI_API_BASE is set to {api_base}")
    openai.api_base = api_base

def log_backoff(details):
    print(f"Error occurred: {details['exception']}. Retrying...")

@backoff.on_exception(
    backoff.expo, 
    openai.OpenAIError, 
    max_tries=200, 
    on_backoff=log_backoff  
)
def completions_with_backoff(**kwargs):
    response = openai.ChatCompletion.create(**kwargs)

    if response.get("finish_reason") == "content_filter":
        print("内容被过滤，正在重试...")
        raise openai.OpenAIError("Content filtered")  
    return response


def gpt(prompt, model="gpt-4o", temperature=0.7, max_tokens=2000, n=1, stop=None, top_p=0.9,gpu_memory_utilization=0.9):
    global completion_tokens, prompt_tokens
    messages = [{"role": "user", "content": prompt}]

    if model == "gpt-4o":
        return gpt4o_ask(messages, temperature, max_tokens, n, stop,top_p)
    elif model.startswith("llama-") or model.startswith("Qwen2") or model.startswith("Mistral")  or model.startswith("QwQ"):
     

        initialize_model(model_name=model, gpu_memory_utilization= gpu_memory_utilization)
        
        outputs = open_model_instance.predict(
            prompt = prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            n=n,
            stop_symbol=stop,
            top_p = top_p
        )
        responses = [output["content"] for output in outputs]
        completion_tokens_local = [output["completion_tokens"] for output in outputs]
        prompt_tokens_local = [output["prompt_tokens"] for output in outputs]
        
        completion_tokens += sum(completion_tokens_local)
        prompt_tokens += sum(prompt_tokens_local)

        return responses
    elif model.startswith("internlm"):
        
        initialize_model(model_name=model)
        if "reward" in model:
            values = reward_model_instance.get_reward_score(
                prompt = prompt
            )
        elif "critic" in model:
            values = reward_model_instance.get_critic_score(
                prompt = prompt
            )
        return values
    else:
        return chatgpt(messages, model, temperature, max_tokens, n, stop,top_p)

def chatgpt(messages, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None,top_p = 1.0):
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        res = completions_with_backoff(model=model, messages=messages, temperature=temperature,
                                       max_tokens=max_tokens, n=cnt, stop=stop, top_p = top_p)
        outputs.extend([choice["message"]["content"] for choice in res["choices"]])
        completion_tokens += res["usage"]["completion_tokens"]
        prompt_tokens += res["usage"]["prompt_tokens"]
    return outputs

def gpt4o_ask(messages, temperature=0.7, max_tokens=1000, n=1, stop=None,top_p = 1.0):
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        cnt = min(n, 20) 
        n -= cnt
        # Azure OpenAI API configuration
        openai.api_key = os.getenv("AZURE_API_KEY", "")  # Get API key from environment variable
        openai.api_base = os.getenv("AZURE_API_BASE", "")  # Get API base from environment variable
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15'  # Azure OpenAI API version

        res = completions_with_backoff(engine=os.getenv("AZURE_ENGINE", ""), messages=messages, 
                                     temperature=temperature, max_tokens=max_tokens, 
                                     n=cnt, stop=stop, top_p=top_p)

        for choice in res["choices"]:
            if "message" in choice and "content" in choice["message"]:
                response = choice["message"]["content"]

                pattern = re.compile(r'end\s+of\s+answer\.', re.IGNORECASE)
                match = pattern.search(response)

                if match:
                    end_pos = match.end()
                    response = response[:end_pos]
                
                if re.search(r"End of answer\.", response):
                    response = re.split(r"End of answer\.", response)[0]

                matches = list(re.finditer(r"Question:", response))
                if len(matches) >= 2:
                    second_question_pos = matches[1].start()
                    response = response[:second_question_pos]

                outputs.append(response)
            else:
                print(f"Unexpected response format: {choice}")

        completion_tokens += res['usage']['completion_tokens']
        prompt_tokens += res['usage']['prompt_tokens']

    return outputs

def gpt_usage(backend="gpt-4"):
    global completion_tokens, prompt_tokens
    cost = 0
    if backend == "gpt-4":
        cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
    elif backend == "gpt-4o":
        cost = completion_tokens / 1000 * 0.015 + prompt_tokens / 1000 * 0.005
    elif backend == "gpt-3.5-turbo":
        cost = completion_tokens / 1000 * 0.002 + prompt_tokens / 1000 * 0.0015
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}
