class Argon2Hasher:
    def __init__(self, options={}):
        self.options = options

    def set_options(self, options):
        self.options = options
        return self

    def _get_password_hasher(self):
        try:
            import argon2
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'argon2' library. Run 'pip install argon2-cffi' to fix this."
            )

        memory = self.options.get("memory", argon2.DEFAULT_MEMORY_COST)
        threads = self.options.get("threads", argon2.DEFAULT_PARALLELISM)
        time = self.options.get("time", argon2.DEFAULT_TIME_COST)
        return argon2.PasswordHasher(
            memory_cost=memory, parallelism=threads, time_cost=time
        )

    def make(self, string):
        ph = self._get_password_hasher()
        return str(ph.hash(bytes(string, "utf-8")))

    def check(self, plain_string, hashed_string):
        ph = self._get_password_hasher()
        return ph.verify(hashed_string, bytes(plain_string, "utf-8"))

    def needs_rehash(self, hashed_string):
        ph = self._get_password_hasher()
        return ph.check_needs_rehash(hashed_string)
