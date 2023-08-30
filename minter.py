import random

from loguru import logger

from config import PRIVATE_KEYS_PATH, ERROR_PRIVATE_KEYS_PATH
from core.client import StarknetClient


def read_from_txt(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        logger.exception(f"File '{file_path}' not found.")
    except Exception as e:
        logger.exception(f"Encountered an error while reading a TXT file '{file_path}': {str(e)}.")


def write_to_txt(file_path, data):
    try:
        with open(file_path, 'w') as file:
            file.write(data)
    except FileNotFoundError:
        logger.exception(f"File '{file_path}' not found.")
    except Exception as e:
        logger.exception(f"Encountered an error while write data to TXT file '{file_path}': {str(e)}.")

async def run_minter() -> None:
    private_keys = read_from_txt(PRIVATE_KEYS_PATH)
    random.shuffle(private_keys)

    for private_key in private_keys:
        client = StarknetClient(private_key=private_key)
        result = await client.mint()

        if not result:
            errors = read_from_txt(ERROR_PRIVATE_KEYS_PATH)
            errors = errors + '\n' + private_key
            write_to_txt(ERROR_PRIVATE_KEYS_PATH, errors)

    logger.success("All accounts are finished.")
