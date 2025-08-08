import requests
import random
import string
import re

def getUserInfo():
    """
    Prompts the user to configure API endpoints and keys.
    Returns:
        tuple: (conwayAPI, gptURLAPI, gptKEY, contentType)
    """
    print("Configure your Conway API URL and GPT access:")
    conwayAPI = input("Enter Conway API URL (default http://127.0.0.1:8000/cgol): ").strip() or "http://127.0.0.1:8000/cgol"
    gptURLAPI = input("Enter API URL (e.g. https://api.yourprovider.com/v1/chat/completions): ").strip()
    gptKEY = input("Enter GPT API key: ").strip()
    contentType = input("Enter Content-Type (default application/json): ").strip() or "application/json"
    return conwayAPI, gptURLAPI, gptKEY, contentType

def callCGOL(apiURL: str, word: str):
    """
    Calls Conway API with a given word.
    Args:
        apiURL (str): Conway API URL.
        word (str): The input word to analyze.
    Returns:
        tuple: (generations, score) returned by Conway API.
    """
    resp = requests.post(apiURL, json={"word": word})
    resp.raise_for_status()
    data = resp.json()
    return data["generations"], data["score"]

def randomWordGenerate(length=6):
    """
    Generates a random lowercase alphabetic word.
    Args:
        length (int): Length of the word (default 6).
    Returns:
        str: Randomly generated word.
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def conwayTool(conwayAPIURL: str, prompt: str) -> str:
    """
    Processes supported prompts and queries Conway API accordingly.
    Args:
        conwayAPIURL (str): Conway API URL.
        prompt (str): User prompt string.
    Returns:
        str: Response based on Conway API results or error message.
    """
    lowerPromt = prompt.lower()

    if "how many generations will the word" in lowerPromt:
        match = re.search(r"word [‘'\"“](\w+)[’'\"”]", prompt, re.IGNORECASE)
        if not match:
            return "Sorry, I couldn't find the word in your prompt."
        word = match.group(1)
        try:
            generations, score = callCGOL(conwayAPIURL, word)
            return f"The word '{word}' results in {generations} generations and a score of {score}."
        except Exception as e:
            return f"Error calling Conway API: {e}"

    elif "generate 3 random words" in lowerPromt:
        results = []
        try:
            for _ in range(3):
                w = randomWordGenerate()
                gens, score = callCGOL(conwayAPIURL, w)
                results.append((w, gens, score))
            highest = max(results, key=lambda x: x[2])
            wordScores = ", ".join([f"'{w}' (gens: {g}, score: {s})" for w, g, s in results])
            return (
                f"Generated 3 random words and their results: {wordScores}. "
                f"The highest Conway score is for '{highest[0]}' with a score of {highest[2]}."
            )
        except Exception as e:
            return f"Error calling Conway API: {e}"
    else:
        return "Prompt not recognized. Please use one of the supported queries."

def callGPT4o(apiURL: str, apiKEY: str, contentTYPE: str, prompt: str) -> str:
    """
    Calls GPT-4o-mini API with the user prompt.
    Args:
        apiURL (str): GPT API URL.
        apiKEY (str): GPT API key.
        contentTYPE (str): Content-Type header.
        prompt (str): User prompt string.
    Returns:
        str: GPT model's response text.
    """
    headers = {
        "Authorization": f"Bearer {apiKEY}",
        "Content-Type": contentTYPE,
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    response = requests.post(apiURL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

def handleLLM(conway_api_url: str, gpt_api_url: str, gpt_api_key: str, content_type: str, prompt: str) -> str:
    try:
        gpt_response = callGPT4o(gpt_api_url, gpt_api_key, content_type, prompt)
    except Exception as e:
        return f"Error calling GPT API: {e}"

    return conwayTool(conway_api_url, prompt)

def runCLI():
    conway_api_url, gpt_api_url, gpt_api_key, content_type = getUserInfo()
    print("\nWelcome to the Conway CLI! Type 'exit' to quit.")

    while True:
        user_prompt = input("Enter prompt for Conway: ").strip()
        if user_prompt.lower() == "exit":
            print("Goodbye!")
            break

        response = handleLLM(conway_api_url, gpt_api_url, gpt_api_key, content_type, user_prompt)
        print(f"Response:\n{response}\n")

if __name__ == "__main__":
    runCLI()
