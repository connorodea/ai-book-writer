"""Configuration for the book generation system - Updated for AutoGen v2"""
import os
from typing import Dict, List, Optional
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily

def get_config(api_key: Optional[str] = None, base_url: str = "http://localhost:1234/v1", model_name: str = "llama-3.1-8b-instruct") -> Dict:
    """Get the configuration for the agents - Updated for AutoGen v2"""
    
    # Use environment variable if no API key provided
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY", "not-needed")
    
    # Create model info for non-OpenAI models
    if "gpt" not in model_name.lower() and "claude" not in model_name.lower():
        # For local/custom models
        model_info = ModelInfo(
            model_name=model_name,
            family=ModelFamily.LLAMA_3_3_8B if "llama" in model_name.lower() else ModelFamily.UNKNOWN,
            context_length=8192,
            max_tokens=4096,
            vision=False,  # Most local models don't support vision
            function_calling=True,  # Assume function calling support
            json_output=True  # Assume JSON output support
        )
    else:
        model_info = None  # OpenAI models are auto-detected
    
    # Create model client for the new API
    model_client = OpenAIChatCompletionClient(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        model_info=model_info
    )
    
    return {
        "model_client": model_client,
        "temperature": 0.7,
        "max_tokens": 2000,
        "timeout": 600
    }

def get_local_config(port: int = 1234, model_name: str = "llama-3.1-8b-instruct") -> Dict:
    """Get configuration for local LLM server"""
    return get_config(
        api_key="not-needed",
        base_url=f"http://localhost:{port}/v1",
        model_name=model_name
    )

def get_openai_config(api_key: str, model_name: str = "gpt-4") -> Dict:
    """Get configuration for OpenAI API"""
    return get_config(
        api_key=api_key,
        base_url="https://api.openai.com/v1",
        model_name=model_name
    )