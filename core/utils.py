import random
import time
from functools import wraps

from loguru import logger
from starknet_py.contract import Contract
from starknet_py.hash.address import compute_address
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.gateway_client import GatewayClient
from tqdm import tqdm
from web3 import Web3

from config import (
    BRAAVOS_PROXY_CLASS_HASH,
    ARGENTX_PROXY_CLASS_HASH,
    BRAAVOS_IMPLEMENTATION_CLASS_HASH,
    ARGENTX_IMPLEMENTATION_CLASS_HASH,
    WALLET_APPLICATION,
    STARKNET_RPC_PROVIDER
)
from core.chain import eth


def get_proxy_class_hash() -> str:
    if WALLET_APPLICATION == "argentx":
        return ARGENTX_PROXY_CLASS_HASH
    elif WALLET_APPLICATION == "braavos":
        return BRAAVOS_PROXY_CLASS_HASH
    else:
        raise Exception(f"No proxy class hash with name for {WALLET_APPLICATION}")


def get_implementation_class_hash() -> str:
    if WALLET_APPLICATION == "braavos":
        return BRAAVOS_IMPLEMENTATION_CLASS_HASH
    elif WALLET_APPLICATION == "argentx":
        return ARGENTX_IMPLEMENTATION_CLASS_HASH
    else:
        raise Exception(f"No implementation class hash with name for {WALLET_APPLICATION}")


def get_address(key_pair) -> int:
    if WALLET_APPLICATION == "braavos":
        return get_braavos_address(key_pair=key_pair)
    elif WALLET_APPLICATION == "argentx":
        return get_argentx_address(key_pair=key_pair)
    else:
        raise Exception("Get address error")


def get_client():
    if STARKNET_RPC_PROVIDER is None:
        return GatewayClient(net="mainnet")
    else:
        return FullNodeClient(node_url=STARKNET_RPC_PROVIDER)


async def get_proxy_contract(self, contract_address):
    return await Contract.from_address(address=contract_address, provider=self, proxy_config=True)


def get_braavos_address(key_pair) -> int:
    proxy_class_hash = BRAAVOS_PROXY_CLASS_HASH
    implementation_class_hash = BRAAVOS_IMPLEMENTATION_CLASS_HASH

    selector = get_selector_from_name("initializer")
    call_data = [key_pair.public_key]

    return compute_address(
        class_hash=proxy_class_hash,
        constructor_calldata=[implementation_class_hash, selector, len(call_data), *call_data],
        salt=key_pair.public_key,
    )


def get_argentx_address(key_pair) -> int:
    proxy_class_hash = ARGENTX_PROXY_CLASS_HASH
    implementation_class_hash = ARGENTX_IMPLEMENTATION_CLASS_HASH

    selector = get_selector_from_name("initialize")
    call_data = [key_pair.public_key, 0]

    return compute_address(
        class_hash=proxy_class_hash,
        constructor_calldata=[implementation_class_hash, selector, len(call_data), *call_data],
        salt=key_pair.public_key,
    )


def get_eth_gas_fee():
    w3 = Web3(Web3.HTTPProvider(eth.rpc))
    return w3.eth.gas_price


def check_balance_starknet(min_balance):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            balance = await self.get_balance()
            if balance < Web3.to_wei(min_balance, "ether"):
                logger.error(f"Balance is below minimum at {hex(self.address)}.")
                return False
            return await func(self, *args, **kwargs)

        return wrapper

    return decorator


def gas_delay(gas_threshold: int, delay_range: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                current_eth_gas_price = get_eth_gas_fee()
                threshold = Web3.to_wei(gas_threshold, "gwei")
                if current_eth_gas_price > threshold:
                    random_delay = random.randint(delay_range[0], delay_range[1])

                    logger.warning(
                        f"Current gas fee '{current_eth_gas_price}' wei > Gas threshold '{threshold}' wei. Waiting for {random_delay} seconds..."
                    )

                    with tqdm(total=random_delay, desc="Waiting", unit="s", dynamic_ncols=True, colour="blue") as pbar:
                        for _ in range(random_delay):
                            time.sleep(1)
                            pbar.update(1)
                else:
                    break

            return func(*args, **kwargs)

        return wrapper

    return decorator


def wait_async(delay_range: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            random_delay = random.randint(*delay_range)
            logger.info(f"Sleeping for {random_delay} seconds...")
            with tqdm(total=random_delay, desc="Waiting", unit="s", dynamic_ncols=True, colour="blue") as pbar:
                for _ in range(random_delay):
                    time.sleep(1)
                    pbar.update(1)
            return result

        return wrapper

    return decorator
