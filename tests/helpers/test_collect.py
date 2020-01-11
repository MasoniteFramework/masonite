from src.masonite.helpers import collect


class TestCollect:

    def test_collect_helper(self):
        assert collect([1, 2]).first() == 1
