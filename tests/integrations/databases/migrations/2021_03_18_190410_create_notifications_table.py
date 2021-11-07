from masoniteorm.migrations import Migration


class CreateNotificationsTable(Migration):
    def up(self):
        """Run the migrations."""
        with self.schema.create("notifications") as table:
            table.big_increments("id").primary()
            table.string("type")
            table.text("data")
            table.morphs("notifiable")
            table.datetime("read_at").nullable()
            table.timestamps()

    def down(self):
        """Revert the migrations."""
        self.schema.drop("notifications")
