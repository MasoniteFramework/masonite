from masonite.helpers import clean_request_input

class TestCleanRequestInput:

    def test_can_clean_string(self):
        assert clean_request_input('<img """><script>alert(\'hey\')</script>">') == '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;'

    def test_can_clean_list(self):
        assert clean_request_input(
            ['<img """><script>alert(\'hey\')</script>">', '<img """><script>alert(\'hey\')</script>">']
        ) == [
            '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;',
            '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;'
        ]

    def test_can_clean_dictionary(self):
        assert clean_request_input(
            {'key': '<img """><script>alert(\'hey\')</script>">'}
        ) == {'key': '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;'}
