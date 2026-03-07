from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gitlab_webhook_secret: str
    gitlab_token: str
    gitlab_base_url: str = "https://gitlab.com"
    risk_scout_comment_marker: str = "<!-- MR_RISK_SCOUT -->"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()