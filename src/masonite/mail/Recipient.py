class Recipient:
    """Message recipient class allowing to build a list a recipients from a string.
    Example: 'Joe <joe@example.com>, Sam <sam@example.com>'.
    """

    def __init__(self, recipient: "list|tuple|str"):
        if isinstance(recipient, (list, tuple)):
            recipient = ",".join(recipient)
        self.recipient = recipient

    def header(self) -> str:
        headers = []
        for address in self.recipient.split(","):

            if "<" in address:
                headers.append(address)
                continue

            if address.strip():
                headers.append(f"<{address.strip()}>")

        return ", ".join(headers)
