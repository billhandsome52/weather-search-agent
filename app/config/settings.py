from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    
    # LLM API
    dashscope_api_key: str = ""
    openai_api_key: str = ""
    
    # Search API
    brave_api_key: str = ""
    
    # Configuration
    default_llm_model: str = "qwen-plus"
    verbose: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    @property
    def has_llm_key(self) -> bool:
        return bool(self.dashscope_api_key or self.openai_api_key)
    
    @property
    def has_search_key(self) -> bool:
        return bool(self.brave_api_key)
    
    @property
    def llm_provider(self) -> str:
        if self.dashscope_api_key:
            return "dashscope"
        elif self.openai_api_key:
            return "openai"
        return "none"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
