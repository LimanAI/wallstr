import itertools
import math
from collections.abc import Sequence
from typing import Literal

import structlog
import tiktoken
from langchain_community.llms.replicate import Replicate
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from PIL.Image import Image
from pydantic import SecretStr

from wallstr.conf import settings
from wallstr.conf.llm_models import SUPPORTED_LLM_MODELS_TYPES

logger = structlog.get_logger()

SUPPORTED_LLM_MODELS_WITH_VISION = ["gpt-4o-mini"]
SUPPORTED_LLM_MODELS_WITH_VISION_TYPES = Literal["gpt-4o-mini"]

LLMModel = (
    ChatOllama | ChatGoogleGenerativeAI | ChatOpenAI | AzureChatOpenAI | Replicate
)


def get_llm(
    model: SUPPORTED_LLM_MODELS_TYPES,
) -> LLMModel:
    if model is not None:
        match model:
            case "claude-3.5-sonnet":
                if settings.MODELS.CLAUDE_35_SONNET is None:
                    raise Exception(
                        "Model claude-3.5-sonnet is not supported in settings"
                    )
                if settings.MODELS.CLAUDE_35_SONNET.PROVIDER == "REPLICATE":
                    replicate_api_key = (
                        settings.MODELS.CLAUDE_35_SONNET.REPLICATE_API_KEY
                        or settings.REPLICATE_API_KEY
                    )
                    if replicate_api_key is None:
                        raise Exception(
                            "Replicate API key is not set for claude-3.5-sonnet model"
                        )
                    _set_replicate_key(replicate_api_key)
                    return Replicate(
                        model="anthropic/claude-3.5-sonnet",
                        replicate_api_token=replicate_api_key.get_secret_value(),
                    )

                raise Exception(
                    f"Not supported provider {settings.MODELS.CLAUDE_35_SONNET.PROVIDER} for claude-3.5-sonnet"
                )
            case "gpt-4o-mini":
                if settings.MODELS.GPT_4O_MINI is None:
                    raise Exception("Model gpt-4o-mini is not supported in settings")
                if settings.MODELS.GPT_4O_MINI.PROVIDER == "OPENAI":
                    return ChatOpenAI(
                        api_key=settings.MODELS.GPT_4O_MINI.OPENAI_API_KEY
                        or settings.OPENAI_API_KEY,
                        model=settings.MODELS.GPT_4O_MINI.NAME,
                    )
                elif settings.MODELS.GPT_4O_MINI.PROVIDER == "AZURE":
                    return AzureChatOpenAI(
                        api_key=settings.MODELS.GPT_4O_MINI.AZURE_API_KEY,
                        api_version=settings.MODELS.GPT_4O_MINI.AZURE_API_VERSION,
                        azure_endpoint=settings.MODELS.GPT_4O_MINI.AZURE_API_URL,
                        model=settings.MODELS.GPT_4O_MINI.NAME,
                    )
                raise Exception(
                    f"Not supported provider {settings.MODELS.GPT_4O_MINI.PROVIDER} for gpt-4o-mini"
                )
            case "gpt-4o":
                if settings.MODELS.GPT_4O is None:
                    raise Exception("Model gpt-4o is not supported in settings")
                if settings.MODELS.GPT_4O.PROVIDER == "OPENAI":
                    return ChatOpenAI(
                        api_key=settings.MODELS.GPT_4O.OPENAI_API_KEY
                        or settings.OPENAI_API_KEY,
                        model=settings.MODELS.GPT_4O.NAME,
                    )
                elif settings.MODELS.GPT_4O.PROVIDER == "AZURE":
                    return AzureChatOpenAI(
                        api_key=settings.MODELS.GPT_4O.AZURE_API_KEY,
                        api_version=settings.MODELS.GPT_4O.AZURE_API_VERSION,
                        azure_endpoint=settings.MODELS.GPT_4O.AZURE_API_URL,
                        model=settings.MODELS.GPT_4O.NAME,
                    )
                raise Exception(
                    f"Not supported provider {settings.MODELS.GPT_4O.PROVIDER} for GPT-4o-mini"
                )
            case "llama3-70b":
                if settings.MODELS.LLAMA3_70B is None:
                    raise Exception("Model llama3-70b is not supported in settings")
                if settings.MODELS.LLAMA3_70B.PROVIDER == "REPLICATE":
                    replicate_api_key = (
                        settings.MODELS.LLAMA3_70B.REPLICATE_API_KEY
                        or settings.REPLICATE_API_KEY
                    )
                    if replicate_api_key is None:
                        raise Exception(
                            "Replicate API key is not set for llama3-70b model"
                        )
                    _set_replicate_key(replicate_api_key)
                    return Replicate(
                        model="meta/meta-llama-3-70b",
                        replicate_api_token=replicate_api_key.get_secret_value(),
                    )

                raise Exception(
                    f"Not supported provider {settings.MODELS.LLAMA3_70B.PROVIDER} for llama3-70b"
                )
            case "gemini-2.0-flash":
                if settings.MODELS.GEMINI_2 is None:
                    raise Exception(
                        "Model gemini-2.0-flash is not supported in settings"
                    )

                if settings.MODELS.GEMINI_2.PROVIDER == "GOOGLE":
                    google_api_key = (
                        settings.MODELS.GEMINI_2.GOOGLE_API_KEY
                        or settings.GOOGLE_API_KEY
                    )
                    if google_api_key is None:
                        raise Exception(
                            "Google API key is not set for gemini-2.0-flash model"
                        )
                    return ChatGoogleGenerativeAI(
                        model=settings.MODELS.GEMINI_2.NAME,
                        google_api_key=google_api_key,
                    )  # type: ignore

                raise Exception(
                    f"Not supported provider {settings.MODELS.GEMINI_2.PROVIDER} for gemini-2.0-flash"
                )
            case "gemma-3-27b":
                if settings.MODELS.GEMMA_3_27B is None:
                    raise Exception("Model gemma-3-27b is not supported in settings")

                if settings.MODELS.GEMMA_3_27B.PROVIDER == "REPLICATE":
                    replicate_api_key = (
                        settings.MODELS.GEMMA_3_27B.REPLICATE_API_KEY
                        or settings.REPLICATE_API_KEY
                    )
                    if replicate_api_key is None:
                        raise Exception(
                            "Replicate API key is not set for gemma-3-27b model"
                        )
                    _set_replicate_key(replicate_api_key)
                    return Replicate(
                        model="google-deepmind/gemma-3-27b-it:c0f0aebe8e578c15a7531e08a62cf01206f5870e9d0a67804b8152822db58c54",
                        replicate_api_token=replicate_api_key.get_secret_value(),
                    )

                raise Exception(
                    f"Not supported provider {settings.MODELS.GEMMA_3_27B.PROVIDER} for gemma-3-27b"
                )
            case _:
                raise ValueError(f"Unsupported model: {model}")


def get_llm_with_vision(
    model: SUPPORTED_LLM_MODELS_WITH_VISION_TYPES = "gpt-4o-mini",
) -> ChatOpenAI | AzureChatOpenAI:
    llm = get_llm(model)
    if not isinstance(llm, ChatOpenAI) and not isinstance(llm, AzureChatOpenAI):
        raise ValueError(f"Only ChatOpenAI model supports vision, got {llm}")
    return llm


def estimate_input_tokens(
    llm: LLMModel,
    input_: str | Sequence[BaseMessage],
    *,
    image: Image | None = None,
    image_mode: Literal["low", "high", "auto"] = "auto",
) -> int:
    enc = None
    if isinstance(llm, (ChatOpenAI, AzureChatOpenAI)):
        if llm.model_name is None:
            logger.warning(
                f"Model name is not set for {llm}, cannot estimate input tokens"
            )
            return 0

        enc = tiktoken.encoding_for_model(llm.model_name)

    if enc is None:
        logger.warning(f"Cannot get tokens encoding for {llm}")
        return 0

    input_enc = []
    if isinstance(input_, str):
        input_enc = enc.encode(input_)
    if isinstance(input_, list):
        content = _merge_langchain_messages(input_)
        input_enc = list(
            itertools.chain(*[enc.encode(raw_message) for raw_message in content])
        )
    input_tokens = len(input_enc)

    if image is not None:
        input_tokens += estimate_input_tokens_for_image(llm, image, image_mode)
    return input_tokens


def estimate_input_tokens_for_image(
    llm: LLMModel, image: Image, image_mode: Literal["low", "high", "auto"] = "auto"
) -> int:
    """
    Getting tokens for models with vision
    Only OpenAI models supported:
    https://platform.openai.com/docs/guides/vision#low-or-high-fidelity-image-understanding
    """
    logger.trace(
        f"Calculate input tokens for {image.size[0]}x{image.size[1]} image, mode: {image_mode}"
    )
    if not isinstance(llm, (ChatOpenAI, AzureChatOpenAI)):
        logger.warning(f"Token estimation for image is not implemented for {llm}")
        return 0

    if llm.model_name not in SUPPORTED_LLM_MODELS_WITH_VISION:
        logger.warning("Model does not support vision")
        return 0
    if image_mode == "low":
        return 85

    if image_mode == "auto" and max(image.size) <= 512:
        return 85

    MAX_SIZE = 2048
    MIN_SIZE = 768

    max_side: float = min(MAX_SIZE, max(image.size))
    scale = max_side / max(image.size)
    min_side = min(image.size) * scale

    scale = MIN_SIZE / min_side
    min_side = MIN_SIZE
    max_side = scale * max_side

    square = max_side * min_side
    tiles = math.ceil(square / 512**2)
    return 170 * tiles + 85


def _merge_langchain_messages(
    input_: Sequence[BaseMessage],
) -> list[str]:
    """
    Returns list with raw text from LangChain messages
    """
    output = []
    for message in input_:
        content = message.content
        if isinstance(content, str):
            output.append(content)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, str):
                    output.append(item)
                elif isinstance(item, dict) and item["type"] == "text":
                    output.append(item["text"])
        else:
            logger.warning(f"Unsupported message type {message}")
    return output


def _set_replicate_key(replicate_api_key: SecretStr) -> None:
    """
    LangChain bug: https://github.com/langchain-ai/langchain/pull/27859
    setting replicate_api_token doesn't work for replicate client
    """
    import os

    os.environ["REPLICATE_API_TOKEN"] = replicate_api_key.get_secret_value()
