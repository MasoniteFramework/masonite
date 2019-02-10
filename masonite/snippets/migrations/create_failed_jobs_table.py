from orator.migrations import Migration


class CreateFailedJobsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('failed_jobs') as table:
            table.increments('id')
            table.string('driver')
            table.string('channel')
            table.binary('payload')
            table.timestamp('failed_at')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('failed_jobs')
