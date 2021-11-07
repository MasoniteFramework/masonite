class DatabaseTransactions:
    def startTestRun(self):
        self.application.make("resolver").begin_transaction(self.connection)
        return self

    def stopTestRun(self):
        self.application.make("resolver").rollback(self.connection)
        return self
