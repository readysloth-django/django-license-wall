from uuid import UUID
from random import Random
from datetime import datetime

# License key format (uuid)
# seed: 32 bit
# position: 32 bit
# key: 64 bit

SEED_LEN_BIT = 32
POSITION_LEN_BIT = 8
KEY_LEN_BIT = 88

assert (SEED_LEN_BIT + POSITION_LEN_BIT + KEY_LEN_BIT) == 128

SEED_LEN_BYTES = SEED_LEN_BIT // 8
POSITION_LEN_BYTES = POSITION_LEN_BIT // 8
KEY_LEN_BYTES = KEY_LEN_BIT // 8


class LicenseKey:
    def __init__(self,
                 seed: int,
                 position: int,
                 key: int):
        self.seed = seed
        self.position = position
        self.key = key

        self.__seed_bytes = self.seed.to_bytes(SEED_LEN_BYTES)
        self.__position_bytes = self.position.to_bytes(POSITION_LEN_BYTES)
        self.__key_bytes = self.key.to_bytes(KEY_LEN_BYTES)
        self.__license_bytes = self.__seed_bytes + self.__position_bytes + self.__key_bytes

    @staticmethod
    def from_str(license_key: str):
        license_bytes = UUID(license_key).bytes
        seed_bytes = license_bytes[:SEED_LEN_BYTES]
        position_bytes = license_bytes[SEED_LEN_BYTES:SEED_LEN_BYTES + POSITION_LEN_BYTES]
        key_bytes = license_bytes[SEED_LEN_BYTES + POSITION_LEN_BYTES:]
        return LicenseKey(int.from_bytes(seed_bytes),
                          int.from_bytes(position_bytes),
                          int.from_bytes(key_bytes))

    @staticmethod
    def generate(initial_seed: int,
                 use_initial: bool = False,
                 random_class: Random = Random):
        seed = initial_seed
        if not use_initial:
            seed = random_class(initial_seed).getrandbits(SEED_LEN_BIT)
        rng = random_class(seed)
        position = rng.getrandbits(POSITION_LEN_BIT)

        key = rng.getrandbits(KEY_LEN_BIT)
        for i in range(position):
            key = rng.getrandbits(KEY_LEN_BIT)
        return LicenseKey(seed, position, key)

    @staticmethod
    def verify(license: str):
        try:
            incoming_license = LicenseKey.from_str(license)
            generated_license = LicenseKey.generate(incoming_license.seed,
                                                    use_initial=True)
            return incoming_license == generated_license
        except Exception:
            return False

    def __str__(self):
        return str(UUID(bytes=self.__license_bytes))

    def __eq__(self, value: 'LicenseKey'):
        return (self.seed == value.seed and
                self.position == value.position and
                self.key == value.key)


class LicenseGenerator:
    def __init__(self,
                 init_seed: int = 0,
                 random_class: Random = Random):
        self.init_seed = init_seed
        self.random_class = random_class
        self.seed_rng = random_class(init_seed)

    def __iter__(self):
        return self

    def __next__(self):
        seed = self.seed_rng.getrandbits(SEED_LEN_BIT)
        return LicenseKey.generate(seed, random_class=self.random_class)


class YearLicenseGenerator(LicenseGenerator):
    def __init__(self, *args, **kwargs):
        seed = datetime.now().year
        super().__init__(seed, *args, **kwargs)


class MonthLicenseGenerator(LicenseGenerator):
    def __init__(self, *args, **kwargs):
        seed = datetime.now().year << 8 | datetime.now().month
        super().__init__(seed, *args, **kwargs)


class DayLicenseGenerator(LicenseGenerator):
    def __init__(self, *args, **kwargs):
        seed = datetime.now().year << 8 | datetime.now().month << 4 | datetime.now().day
        super().__init__(seed, *args, **kwargs)


class WeekLicenseGenerator(LicenseGenerator):
    def __init__(self, *args, **kwargs):
        seed = datetime.now().year << 8 | datetime.now().isocalendar()[1]
        super().__init__(seed, *args, **kwargs)
