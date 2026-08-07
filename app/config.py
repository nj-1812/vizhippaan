from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    APP_NAME: str = "VIZHIPPAAN API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    ENVIRONMENT: str = "development"

    FRONTEND_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    MODEL_PATH: str = str(BASE_DIR / "models" / "vizhippaan_catboost_model.cbm")
    METADATA_PATH: str = str(BASE_DIR / "models" / "model_metadata.json")
    DATA_PATH: str = str(BASE_DIR / "data" / "vizhippaan_feature_engineered.csv")

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    @property
    def origins(self) -> list[str]:
        return [x.strip() for x in self.FRONTEND_ORIGINS.split(",") if x.strip()]

settings = Settings()
