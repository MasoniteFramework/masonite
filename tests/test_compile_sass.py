import os
from masonite.storage import Storage


class TestCompileSass:

    def test_compiles_sass(self):
        Storage().compile_sass()

        assert os.path.exists(os.path.join(os.getcwd(), 'storage/compiled/style.css'))
