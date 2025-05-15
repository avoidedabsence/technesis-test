from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv
from loguru import logger

@dataclass
class _Config:
    BOT_TOKEN: str
    DB_URL: str
    DB_SYNC_URL: str
    
    CONCURRENT_REQUESTS: int
    
    def _init() -> _Config | None:
        load_dotenv()
        
        token = getenv('BOT_TOKEN', None)
        db_path = getenv('DB_PATH', None)
        concur_reqs = getenv('CONCURRENT_REQUESTS', None)
        
        if any(var is None for var in (token, db_path, concur_reqs)):
            logger.critical("dotenv file is not fully completed, check BOT_TOKEN and DB_PATH variables")
            return None

        concur_reqs = int(concur_reqs)
        db_url = "sqlite+aiosqlite:///" + db_path
        db_sync_url = db_url.replace("+aiosqlite", "")
        
        return _Config(
            BOT_TOKEN=token,
            DB_SYNC_URL=db_sync_url,
            DB_URL=db_url,
            CONCURRENT_REQUESTS=concur_reqs
        )
        
Config = _Config.init()