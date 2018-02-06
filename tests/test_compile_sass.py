from masonite.storage import Storage
import os

def test_compiles_sass():
    Storage().compile_sass()

    assert os.path.exists(os.path.join(os.getcwd(), 'storage/compiled/style.css'))
    os.remove(os.path.join(os.getcwd(), 'storage/compiled/style.css'))
