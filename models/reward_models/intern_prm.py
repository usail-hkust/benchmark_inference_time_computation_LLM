import torch
from transformers import AutoModel, AutoTokenizer

class PRM:
    def __init__(self, model_name: str, device_map: str = "cuda:0", torch_dtype: torch.dtype = torch.float16, trust_remote_code: bool = True):
        """
        Initialize the PRM class to handle model loading and scoring.

        Args:
            model_name (str): The name of the model (e.g., "internlm2_5-step-prover-critic").
            device_map (str, optional): The device map, e.g., "auto" or "cuda". Defaults to "auto".
            torch_dtype (torch.dtype, optional): The data type for model parameters, e.g., torch.float16. Defaults to torch.float16.
            trust_remote_code (bool, optional): Whether to trust remote code for loading the model and tokenizer. Defaults to True.
        """
        
        # Define model paths for different model names
        self.model_paths = {
            "internlm2_5-step-prover-critic": "/nfs/ofs-llm-ssd/models/prm/internlm2_5-step-prover-critic",
            "internlm2-1_8b-reward": "/nfs/ofs-llm-ssd/models/prm/internlm2-1_8b-reward",
        }

        # Check if the model name exists in the model paths dictionary
        if model_name not in self.model_paths:
            raise ValueError(f"Model name '{model_name}' not found in available models.")
        
        # Get the model path for the specified model name
        self.model_path = self.model_paths[model_name]

        # Load the model and tokenizer
        self.model = AutoModel.from_pretrained(
            self.model_path,
            device_map=device_map,
            torch_dtype=torch_dtype,
            trust_remote_code=trust_remote_code
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=trust_remote_code)

    def get_critic_score(self, prompt) -> list:
        """
        Given a batch of chat responses, compute the critic score for each response in the batch.
        
        Args:
            prompt (list): List of chat responses to evaluate.
            
        Returns:
            list: A list of computed scores for each response in the batch.
        """

        # Initialize the result list to collect scores
        format_scores = []

        # Determine the batch size
        batch_size = len(prompt)

        # If the batch size exceeds a certain threshold, split the batch into smaller chunks
        batch_threshold = 1
        if batch_size >= batch_threshold:
            # Split the batch into chunks
            for i in range(0, batch_size, batch_threshold):
                batch_chunk = prompt[i:i + batch_threshold]
                # Get scores for the current chunk
                scores = self.model.get_scores(self.tokenizer, batch_chunk)
        
                # Extract only the first score (assuming scores is a list of tuples/lists)
                format_scores.extend([score[0] for score in scores])
        else:
            # Process the whole batch if it is below the threshold
            scores = self.model.get_scores(self.tokenizer, prompt)
            format_scores = [score[0] for score in scores]

        return format_scores


    def get_reward_score(self, prompt) -> list:
        """
        Given a user input and a list of assistant responses, computes the reward scores for the batch.

        Args:
            prompt (list): List of tuples (user_input, assistant_response).

        Returns:
            list: A list of computed reward scores for each (user_input, assistant_response) pair.
        """

        # Initialize the result list to collect scores
        reward_scores = []

        # Determine the batch size
        batch_size = len(prompt)

        # If the batch size exceeds a certain threshold, split the batch into smaller chunks
        batch_threshold = 1
        if batch_size >= batch_threshold:
            # Split the batch into chunks
            for i in range(0, batch_size, batch_threshold):
                batch_chunk = prompt[i:i + batch_threshold]
                # Get scores for the current chunk
                scores = self.model.get_scores(self.tokenizer, batch_chunk)
             
                reward_scores.append(scores)
        else:
            # Process the whole batch if it is below the threshold
            scores = self.model.get_scores(self.tokenizer, prompt)
            # If the batch has only one item, ensure scores is wrapped in a list
            if  len(prompt) == 1:
                # If scores is a tuple or list with a single element, wrap it in a list
                scores = [scores]
            reward_scores = scores

        return reward_scores



def test_prm_model():
    """
    Function to test the PRM model with user input (x) and a list of assistant responses (ys).
    """

    # Example chat data for x (user input) and ys (a list of assistant responses)
    x = "Every day, Wendi feeds each of her chickens three cups of mixed chicken feed, containing seeds, mealworms and vegetables to help keep them healthy. She gives the chickens their feed in three separate meals. In the morning, she gives her flock of chickens 15 cups of feed. In the afternoon, she gives her chickens another 25 cups of feed. How many cups of feed does she need to give her chickens in the final meal of the day if the size of Wendi's flock is 20 chickens?"
    
    ys = [
        "Answer: Step 1: Wendi has 20 chickens and she gives them 3 cups of feed each. This means she gives her chickens 20 * 3 = 60 cups of feed in a day. Step 2: Wendi already gave her chickens 15 + 25 = 40 cups of feed. Step 3: This means, she needs to give her chickens 60 - 40 = 20 cups of feed in the final meal of the day. Step 4: so the final answer is: 20.",
        "Answer: Wendi will need to give 20 chickens a total of 60 cups of feed, and since 40 cups have already been given, she needs to provide 20 cups in the final meal.",
        "Wendi needs to give the chickens 20 cups of feed in the last meal to make sure each chicken gets three cups in total."
    ]

    # Specify the model to use
    model_name = "internlm2-1_8b-reward"  # You can change this to any of the available models from model_paths
    model_name = "internlm2_5-step-prover-critic"  # You can change this to any of the available models from model_paths
    # Create the PRM instance
    prm_model = PRM(model_name=model_name)
    
    # Construct the chat batch based on the user input and assistant responses
    chat_batch = [
        [{"role": "user", "content": x}, {"role": "assistant", "content": y}]
        for y in ys
    ]
    
        # Get critic scores for the responses
    critic_scores = prm_model.get_critic_score(chat_batch)
    print("Critic Scores:", critic_scores)

    # # Get reward scores for the responses paired with the user input
    # reward_scores = prm_model.get_reward_score(chat_batch)
    # print("Reward Scores:", reward_scores)

if __name__ == "__main__":
    # Run the test
    test_prm_model()

