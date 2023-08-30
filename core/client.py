from loguru import logger
from starknet_py.net.account.account import Account
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

from config import TX_DELAY_RANGE, GAS_THRESHOLD, MIN_BALANCE, GAS_DELAY_RANGE, MINT_CONTRACT_ADDRESS
from core.utils import check_balance_starknet, wait_async, gas_delay
from core.utils import (
    get_proxy_class_hash,
    get_implementation_class_hash,
    get_address,
    get_client,
    get_proxy_contract
)


class StarknetClient(Account):
    def __init__(self, private_key: str):
        self.private_key = int(private_key, 0)
        self.key_pair = KeyPair.from_private_key(self.private_key)
        self.proxy_class_hash = get_proxy_class_hash()
        self.implementation_class_hash = get_implementation_class_hash()
        self.ESTIMATED_FEE_MULTIPLIER = 1.2

        super().__init__(
            address=get_address(self.key_pair),
            client=get_client(),
            signer=None,
            key_pair=self.key_pair,
            chain=StarknetChainId.MAINNET
        )

    @check_balance_starknet(min_balance=MIN_BALANCE)
    @wait_async(delay_range=TX_DELAY_RANGE)
    @gas_delay(gas_threshold=GAS_THRESHOLD, delay_range=GAS_DELAY_RANGE)
    async def mint(self) -> bool:
        try:
            logger.info(f"Try to execute starknet avnu_swap function")

            contract_address = int(MINT_CONTRACT_ADDRESS, 16)
            contract = await get_proxy_contract(self, contract_address)
            call = contract.functions["mintPublic"].prepare(
                to=self.address
            )

            try:
                tx = await self.execute(calls=call, auto_estimate=True)

                if await self.client.wait_for_tx(tx.transaction_hash):
                    logger.success(f"Transaction was successful")
                    logger.success(f"https://starkscan.co/tx//{(hex(tx.transaction_hash))}")
                    return True

            except Exception as e:
                logger.error(f"Send tx error: {str(e)}")
                return False

        except Exception as e:
            logger.exception(f"Exception occurred in Starknet avnu_swap function: {e}")
            return False
