from orator.migrations import Migration


class CreateVideosPlaylistsFk(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('videos') as table:
            table.unsigned_integer('playlist_id').nullable()
            table.foreign('playlist_id').references('id').on('playlists')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('videos') as table:
            pass
