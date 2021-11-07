from masoniteorm.migrations import Migration


class CreateQueueJobsTable(Migration):
    def up(self):
        """Run the migrations."""
        with self.schema.create("jobs") as table:
            table.increments("id")
            table.string("name")
            table.string("queue")
            table.binary("payload")
            table.integer("attempts")
            table.timestamp("ran_at").nullable()
            table.timestamp("available_at", now=True).nullable()
            table.timestamp("reserved_at").nullable()
            table.timestamp("created_at", now=True).nullable()

    def down(self):
        """Revert the migrations."""
        self.schema.drop("jobs")
