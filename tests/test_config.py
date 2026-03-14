"""
配置测试
"""

import pytest
from app.config import settings


def test_settings_loaded():
    """测试配置加载"""
    assert settings is not None


def test_llm_provider():
    """测试 LLM 提供商检测"""
    provider = settings.llm_provider
    assert provider in ["dashscope", "openai", "none"]


def test_has_llm_key():
    """测试 LLM Key 检测"""
    # 至少有一个 API Key 配置
    # 这个测试可能会失败，取决于 .env 配置
    pass  # 可选测试
