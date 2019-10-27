from orator.migrations import Migration


class CreateQueueJobsTable(Migration):

    def up(self):
        """Run the migrations."""
        with self.schema.create('queue_jobs') as table:
            table.increments('id')
            table.string('name')
            table.binary('serialized')
            table.integer('attempts')
            table.integer('failed').nullable()
            table.timestamp('ran_at').nullable()
            table.timestamp('created_at').nullable()
            table.timestamp('wait_until').nullable()

    def down(self):
        """Revert the migrations."""
        self.schema.drop('queue_jobs')
