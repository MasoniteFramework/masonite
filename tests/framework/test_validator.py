from masonite.request import Request
from masonite.validator import Validator
from validator import Pattern, Required, validate, Length

wsgi_request = {
    'wsgi.version': (1, 0),
    'wsgi.multithread': False,
    'wsgi.multiprocess': True,
    'wsgi.run_once': False,
    'SERVER_SOFTWARE': 'gunicorn/19.7.1',
    'REQUEST_METHOD': 'GET',
    'QUERY_STRING': 'id=1',
    'RAW_URI': '/',
    'SERVER_PROTOCOL': 'HTTP/1.1',
    'HTTP_HOST': '127.0.0.1:8000',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'HTTP_UPGRADE_INSECURE_REQUESTS': '1',
    'HTTP_COOKIE': 'setcookie=value',
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
    'HTTP_ACCEPT_LANGUAGE': 'en-us',
    'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
    'HTTP_CONNECTION': 'keep-alive',
    'wsgi.url_scheme': 'http',
    'REMOTE_ADDR': '127.0.0.1',
    'REMOTE_PORT': '62241',
    'SERVER_NAME': '127.0.0.1',
    'SERVER_PORT': '8000',
    'PATH_INFO': '/',
    'SCRIPT_NAME': ''
}

REQUEST = Request(wsgi_request)

def test_validator():
    pass
    # validator = Validator()
    # assert validator.validate() == validator
def test_validator_sets_request():
    validator = Validator(REQUEST)

    assert validator.request is REQUEST

def test_email_validator_sets_dictionary():
    email_validator = Validator(REQUEST)
    email_validator.validate({'id': 1})
    assert email_validator.validation_dictionary == {'id': 1}

def test_validator_check_does_not_match():
    email_validator = Validator(REQUEST)
    email_validator.validate({'id': [Required, Pattern('[a-zA-Z]')]})
    assert email_validator.check() is False

def test_validator_check_matches():
    email_validator = Validator(REQUEST)
    email_validator.validate({'id': [Required, Pattern(r'\d+')]})
    assert email_validator.check() is True

def test_validator_error():
    email_validator = Validator(REQUEST)
    email_validator.validate({'username': [Required]})
    assert email_validator.check() is False
    assert email_validator.errors()['username'] == 'must be present'

def test_validator_error_without_request():
    email_validator = Validator()
    email_validator.validate({'username': [Required]})
    assert email_validator.check({'id': 5}) is False
    assert email_validator.errors()['username'] == 'must be present'

def test_validator_check_matches_without_request():
    email_validator = Validator()
    email_validator.validate({'id': [Required, Pattern(r'\d+')]})
    assert email_validator.check({'id': '4'}) is True

def test_validator_errors_returns_false():
    email_validator = Validator()
    email_validator.validate({'id': [Required, Pattern(r'\d+')]})
    assert email_validator.check({'id': '4'}) is True
    assert email_validator.errors() is None

def test_custom_error_message():
    email_validator = Validator()
    email_validator.validate({'id': [Required], 'username': [Required]})
    email_validator.messages({'id': 'change your id', 'username': 'dont forget your username'})

    assert email_validator.check({'tomato': 'true'}) is False
    assert email_validator.errors()['id'] == 'change your id'
    assert email_validator.errors()['username'] == 'dont forget your username'

def test_custom_error_messages_missing_one():
    email_validator = Validator()
    email_validator.validate({'id': [Required]})

    email_validator.messages(
        {'username': 'dont forget your username'})

    assert email_validator.check({'username': '5'}) is False
    assert email_validator.errors()['id'] == 'must be present'

def test_validator_length():
    email_validator = Validator()
    email_validator.validate({'id': [Length(0, maximum=2)]})
    assert email_validator.check({'id': [1,2,3,4,5]}) is False
