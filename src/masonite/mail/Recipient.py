class Recipient:
    def __init__(self, recipient):
        if isinstance(recipient, (list, tuple)):
            recipient = ",".join(recipient)
        self.recipient = recipient

    def header(self):
        headers = []
        for address in self.recipient.split(","):

            if "<" in address:
                headers.append(address)
                continue

            if address.strip():
                headers.append(f"<{address.strip()}>")

        return ", ".join(headers)
