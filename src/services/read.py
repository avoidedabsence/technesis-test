from loguru import logger
import pandas as pd

from database.models import Item
from utils.exceptions import CustomException


def read_file(user_id: int, file_path: str) -> dict:
    df = validate_file(user_id, file_path)
    
    return df.to_dict('index')
    
    
def validate_file(user_id: int, file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(
            file_path
        )
    except Exception as e:
        logger.error('failed to read {}:{} from cache, exc: {}', user_id, file_path, e)
        raise CustomException(f'Ошибка при прочтении файла из кэша \({e}\)') 
    
    headers = list(df)
    
    if headers != ['title', 'url', 'xpath']:
        logger.error('invalid headers {} for file:{}', headers, file_path)
        raise CustomException(f'Ошибка в полях таблицы \({headers} \!\= {['title', 'url', 'xpath']}\)') 
    
    return df

    