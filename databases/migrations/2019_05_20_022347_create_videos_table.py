from orator.migrations import Migration


class CreateVideosTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('videos') as table:
            table.increments('id')
            table.string('name')
            table.string('duration')
            table.string('url')
            table.datetime('published_at')
            table.string('thumbnail').nullable()
            table.integer('premium')
            table.unsigned_integer('author_id').nullable()
            table.foreign('author_id').references('id').on('users').on_delete('CASCADE')
            table.text('description')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('videos')
