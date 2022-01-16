from tests import TestCase
from src.masonite.facades import Hash


class TestHashers(TestCase):
    def test_should_hash_and_check_using_hasher(self):

        for driver in Hash.drivers.keys():
            hashed = Hash.make("masonite", driver=driver)
            assert hashed != "masonite"
            assert Hash.check("masonite", hashed, driver=driver)

    def test_bcrypt_needs_rehash(self):
        hashed = Hash.make("masonite", options={"rounds": 5})
        # here no options is given so default rounds will be used (10 in tests config)
        assert Hash.needs_rehash(hashed)

    def test_argon2_needs_rehash(self):
        hashed = Hash.make(
            "masonite",
            driver="argon2",
            options={
                "memory": 512,
                "threads": 8,
                "time": 2,
            },
        )
        # Here argon2 method is invoked without custom options and will
        # use default argon2 configuration, so rehash will be needed
        assert Hash.needs_rehash(hashed, driver="argon2")

    def test_should_return_hash_content_as_string(self):

        for driver in Hash.drivers.keys():
            hashed = Hash.make("masonite", driver=driver)
            assert type(hashed) == str

    def test_should_return_hash_content_as_bytes(self):

        for driver in Hash.drivers.keys():
            hashed = Hash.make_bytes("masonite", driver=driver)
            assert type(hashed) == bytes
