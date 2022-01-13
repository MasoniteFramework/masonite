import bcrypt


class BcryptHasher:
    def __init__(self, options={}):
        self.options = options

    def set_options(self, options):
        self.options = options
        return self

    def make(self, string):
        return self.make_bytes(string).decode("utf-8")

    def make_bytes(self, string):
        rounds = self.options.get("rounds", 12)
        salt = bcrypt.gensalt(rounds=rounds)
        return bcrypt.hashpw(bytes(string, "utf-8"), salt)

    def check(self, plain_string, hashed_string):
        if not isinstance(hashed_string, bytes):
            hashed_string = bytes(hashed_string or "", "utf-8")
        return bcrypt.checkpw(bytes(plain_string, "utf-8"), hashed_string)

    def needs_rehash(self, hashed_string):
        # Bcrypt hashes have the format $2b${rounds}${salt}{checksum}. rounds is encoded as
        # 2 zero-padded decimal digits. The prefix (2b) is never modified in make() function so we
        # can assume that rounds value used when generating the hash is located at [4:6] indexes
        # of the hash.
        old_rounds_value = int(hashed_string[4:6])
        return old_rounds_value != self.options.get("rounds", 12)
