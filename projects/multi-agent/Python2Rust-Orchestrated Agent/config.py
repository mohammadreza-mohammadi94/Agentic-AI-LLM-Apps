# Define models and their respective platforms

MODEL_CONFIG = {
    "groq": {
        "client": "GroqClient",
        "models": {
            "llama-3.3-70b-versatile": {"max_tokens": 8192, "temperature": 0.6, "top_p": 0.9},
            "openai/gpt-oss-120b": {"max_tokens": 8192, "temperature": 0.6, "top_p": 0.9}
        }
    },
    "cerebras": {
        "client": "CerebrasClient",
        "models": {
            "qwen-3-coder-480b": {"max_tokens": 40000, "temperature": 0.5, "top_p": 0.8},
            "llama-4-maverick-17b-128e-instruct": {"max_tokens": 32768, "temperature": 0.6, "top_p": 0.9}
        }
    }
}

# The most powerful model is designated as the "Judge" for the review task.
JUDGE_PLATFORM = "cerebras"
JUDGE_MODEL_NAME = "qwen-3-coder-480b"