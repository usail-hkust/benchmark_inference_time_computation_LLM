import logging
import argparse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from functools import partial
import torch.multiprocessing as mp  
import os  
import torch  
from models.base_model import initialize_model, open_model_instance, reward_model_instance 
from typing import Any, Optional


os.environ["OMP_NUM_THREADS"] = "1"  
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"  

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Run FastAPI service with configurable model and port.")
    parser.add_argument('--model', type=str, default="Qwen2.5-7B", help="Model name to be used (default: 'Qwen2.5-7B')")
    parser.add_argument('--port', type=int, default=8000, help="Port to run the FastAPI service on (default: 8000)")
    parser.add_argument('--gpu_memory_utilization', type=float, default=0.9, help="GPU memory utilization percentage (default: 0.45)")
    return parser.parse_args()


args = parse_args()


if __name__ == '__main__':
    torch.cuda.init()
    mp.set_start_method("spawn", force=True)


app = FastAPI()
model_instance = None

class ModelRequest(BaseModel):
    prompt: Any  
    model: str  # No default value, so the model can be changed via parameters
    temperature: float = 0.7
    max_tokens: int = 1000
    n: int = 1
    stop: Optional[str] = None
    top_p: float = 1.0
    gpu_memory_utilization: float = 0.45

# FastAPI startup event to load the model
@app.on_event("startup")
def startup_event():
    try:
        logger.info(f"Starting to load model: {args.model}, GPU memory utilization: {args.gpu_memory_utilization * 100}%")
        
        global model_instance
        model_instance = initialize_model(model_name=args.model, gpu_memory_utilization=args.gpu_memory_utilization)
       
    except Exception as e:
        logger.error(f"Model loading failed: {e}")
        raise e  # Let the application fail to start to avoid handling requests when the model is not loaded

# Model request handler function
def handle_model_request(prompt: Any, model: str, temperature: float, max_tokens: int, n: int, stop: Optional[str], top_p: float, gpu_memory_utilization: float = 0.45):
    # Choose which instance to use based on the model type
    messages = [{"role": "user", "content": prompt}]
  
    if model == "gpt-4o":
        return model_instance(messages, temperature, max_tokens, n, stop, top_p)
    elif model.startswith("llama-") or model.startswith("Qwen2") or model.startswith("Mistral") or model.startswith("QwQ"):

        outputs = model_instance.predict(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            n=n,
            stop_symbol=stop,
            top_p=top_p
        )
        responses = [output["content"] for output in outputs]

        return responses
    elif model.startswith("internlm"):

        if "reward" in model:
            values = model_instance.get_reward_score(
                prompt=prompt
            )
        elif "critic" in model:
            values = model_instance.get_critic_score(
                prompt=prompt
            )
        return values


@app.post("/generate/")
async def generate_response(request: ModelRequest):
    """
    Receive request, call the corresponding model for inference, and return the result
    """
    try:
        logger.info(f"Received model request: {request.model}, prompt: {request.prompt}")

        # Check if the requested model matches the loaded model
        if request.model != args.model:
            raise HTTPException(status_code=400, detail=f"Requested model {request.model} is not loaded.")

        # Call model inference
        response = handle_model_request(
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            n=request.n,
            stop=request.stop,
            top_p=request.top_p,
            gpu_memory_utilization=request.gpu_memory_utilization
        )
        
        logger.info(f"Model generated response: {response}")
        return {"response": response}
    
    except HTTPException as he:
        raise he  # Directly raise HTTP exception
    except Exception as e:
        logger.error(f"Error occurred during model inference: {e}")
        raise HTTPException(status_code=500, detail=f"Error occurred during model inference: {e}")

if __name__ == "__main__":
    logger.info(f"Starting FastAPI service, model: {args.model}, port: {args.port}")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=args.port)
