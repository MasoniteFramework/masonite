import shutil

from masonite.helpers.filesystem import make_directory


def test_make_directory():
    dir_path = 'storage/uploads/test-dir'
    file_path = 'storage/uploads/test-dir/test.py'
    assert make_directory(dir_path)
    assert make_directory(file_path)
    with open(file_path, "w+"):
        pass
    assert not make_directory(file_path)
    shutil.rmtree(dir_path)
