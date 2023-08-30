ARGENTX_PROXY_CLASS_HASH = 0x025EC026985A3BF9D0CC1FE17326B245DFDC3FF89B8FDE106542A3EA56C5A918
ARGENTX_IMPLEMENTATION_CLASS_HASH = 0x33434AD846CDD5F23EB73FF09FE6FDDD568284A0FB7D1BE20EE482F044DABE2

BRAAVOS_PROXY_CLASS_HASH = 0x03131FA018D520A037686CE3EFDDEAB8F28895662F019CA3CA18A626650F7D1E
BRAAVOS_IMPLEMENTATION_CLASS_HASH = 0x5AA23D5BB71DDAA783DA7EA79D405315BAFA7CF0387A74F4593578C3E9E6570

MINT_CONTRACT_ADDRESS = "0x00b719f69b00a008a797dc48585449730aa1c09901fdbac1bc94b3bdc287cf76"

# если вы используете приватные RPC, то нужно сменить None на "https://ваш-rpc-endpoint"
STARKNET_RPC_PROVIDER = None

# максимальная плата за газ в сети ERC-20 при которой транзакции будут отправляться, значение в GWEI
GAS_THRESHOLD = 20

# диапазон для времени задержки между проверками текущей платы за газ в секундах
GAS_DELAY_RANGE = [60, 60]

# путь к файлу, содержащий приватные ключи Starknet кошельков
PRIVATE_KEYS_PATH = "data/private_keys.txt"

# путь к файлу, содержащему приватные ключи Starknet кошельков, где была ошибка минта
ERROR_PRIVATE_KEYS_PATH = "data/errors_private_keys.txt"

# диапазон для времени задержки между отправкой каждой транзакции в секундах
TX_DELAY_RANGE = [10, 30]

# минимальный баланс в ETH, если баланс ниже минимально, аккаунт пропускается
MIN_BALANCE = 0.0001

# приложение, с помощью которого вы генерировали кошельки starknet: "argentx" либо "braavos"
WALLET_APPLICATION = "argentx"
