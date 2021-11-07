from masoniteorm.migrations import Migration


class CreateFailedJobsTable(Migration):
    def up(self):
        """Run the migrations."""
        with self.schema.create("failed_jobs") as table:
            table.increments("id")
            table.string("queue").nullable()
            table.string("connection").nullable()
            table.string("name").nullable()
            table.string("driver").nullable()
            table.binary("payload")
            table.text("exception").nullable()
            table.timestamp("failed_at").nullable()
            table.timestamp("created_at").nullable()

    def down(self):
        """Revert the migrations."""
        self.schema.drop("failed_jobs")
