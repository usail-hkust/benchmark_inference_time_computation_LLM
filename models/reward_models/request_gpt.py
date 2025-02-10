import requests
import argparse

def request_gpt(prompt, model="Qwen2.5-7B", temperature=0.7, max_tokens=3000, n=1, stop=None, top_p=1.0, port=8001,gpu_memory_utilization=0.9):
    """
    Send request to FastAPI service and get response from GPT model
    :param prompt: Input prompt text for the model
    :param model: Name of the model to use
    :param temperature: Temperature parameter affecting randomness of generated text
    :param max_tokens: Maximum number of tokens to return
    :param n: Number of completions to generate
    :param stop: Stop sequence for text generation
    :param top_p: Nucleus sampling probability
    :param port: Port number for FastAPI service, default is 8001
    """
    # Build HTTP address
    http_address = f"http://127.0.0.1:{port}/generate/"
    
    # If stop is None, pass empty string
    if model == "gpt-4o":
        if stop is None:
            stop = ""
    else:
        if stop is None:
            #stop = ""
            stop = "End of answer."
    
    # Request data
    data = {
        "prompt": prompt,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "n": n,
        "stop": stop,  # stop will be empty string instead of None
        "top_p": top_p,
        "gpu_memory_utilization": gpu_memory_utilization
    }

    try:
        print(f"Sending request to {http_address} with data: {data}")
        response = requests.post(http_address, json=data)
        
        # # Print status code and response body for debugging
        # print(f"Response Status Code: {response.status_code}")
        # print(f"Response Body: {response.text}")
        
        # Check if response is successful
        response.raise_for_status()  # Will raise an exception if response has error
        
        # Return text from response
        return response.json().get("response", "No response in the body.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error making HTTP request: {e}")
        return None

# Parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send request to FastAPI service.")
    parser.add_argument("prompt", type=str, help="The prompt to send to the GPT model")
    parser.add_argument("--port", type=int, default=8001, help="Port for the FastAPI service (default is 8001)")

    args = parser.parse_args()

    # Call request_gpt function with parsed arguments
    response = request_gpt(args.prompt, port=args.port)
    
    if response:
        print("Generated text:", response)
    else:
        print("Failed to get response.")
