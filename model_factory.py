"""
Factory for Chat models

This module contains a factory function to create and return a ChatOCIGenAI model instance.
It is designed to be used in the context of an application that interacts with Oracle Cloud
Infrastructure (OCI) Generative AI services.

This version has been adapted to work with new models (xAI and OpenAI)
Author: L. Saetta
Date: 21/05/2025

"""

from langchain_community.chat_models import ChatOCIGenAI
from utils import get_console_logger
from config import MODEL_ID, SERVICE_ENDPOINT, AUTH_TYPE, DEBUG, MAX_TOKENS, TEMPERATURE
from config_private import COMPARTMENT_OCID

MODELS_WITHOUT_KWARGS = {
    "openai.gpt-4o-search-preview",
    "openai.gpt-4o-search-preview-2025-03-11",
}


def normalize_provider(model_id: str) -> str:
    """
    apply an hack to handle new models:
    use meta as provider for these new models
    """
    provider = model_id.split(".")[0]
    if provider in {"xai", "openai"}:
        # Known LangChain limitation workaround
        return "meta"
    return provider


def get_chat_model(
    model_id: str = MODEL_ID,
    service_endpoint: str = SERVICE_ENDPOINT,
    temperature: float = TEMPERATURE,
    max_tokens: int = MAX_TOKENS,
) -> ChatOCIGenAI:
    """
    Factory function to create and return a ChatOCIGenAI model instance.

    Args:
        model_id (str): The model ID.
        service_endpoint (str): The OCI service endpoint.
        temperature (float): The generation temperature.
        max_tokens (int): Maximum number of tokens.
        logger: Optional logger instance.

    Returns:
        ChatOCIGenAI: Configured chat model instance.
    """
    # Create and return the chat model
    logger = get_console_logger()

    if DEBUG:
        logger.info("Using model: %s", model_id)

    # try to identify the provider
    _provider = normalize_provider(model_id)

    if model_id not in MODELS_WITHOUT_KWARGS:
        _model_kwargs = {
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
    else:
        # for some models (OpenAI search) you cannot set those params
        _model_kwargs = None

    return ChatOCIGenAI(
        auth_type=AUTH_TYPE,
        model_id=model_id,
        service_endpoint=service_endpoint,
        model_kwargs=_model_kwargs,
        compartment_id=COMPARTMENT_OCID,
        provider=_provider,
    )
