import json
import unittest
import pytest
import platform
import pendulum
from uuid import uuid1, uuid3, uuid4, uuid5

# from masonite.drivers import SessionCookieDriver
from tests import TestCase

from src.masonite.validation import RuleEnclosure
from src.masonite.validation.providers import ValidationProvider
from src.masonite.validation import (
    ValidationFactory,
    Validator,
    accepted,
    active_domain,
    after_today,
    before_today,
    confirmed,
    contains,
    date,
    different,
    distinct,
    does_not,
    email,
    equals,
    exists,
    file,
    greater_than,
    image,
    in_range,
    ip,
    is_future,
    is_list,
    is_in,
    is_past,
    isnt,
    postal_code,
    strong,
    regex,
    uuid,
    video,
)
from src.masonite.validation.Validator import json as vjson
from src.masonite.validation.Validator import (
    length,
    less_than,
    matches,
    none,
    numeric,
    one_of,
    phone,
    required,
    required_if,
    required_with,
    string,
    timezone,
    truthy,
    when,
)


class TestValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_required(self):
        validate = Validator().validate({"test": 1}, required(["user", "email"]))

        self.assertEqual(validate.get("user"), ["The user field is required."])
        self.assertEqual(validate.get("email"), ["The email field is required."])

        validate = Validator().validate({"test": 1}, required(["test"]))

        self.assertEqual(len(validate), 0)

    def test_required_with_non_truthy_values(self):
        for falsy_value in [[], {}, "", False, 0]:
            validate = Validator().validate({"user": falsy_value}, required(["user"]))
            self.assertEqual(validate.get("user"), ["The user field is required."])

    def test_can_validate_null_values(self):
        validate = Validator().validate({"test": None}, length(["test"], min=2, max=5))

        self.assertEqual(len(validate), 0)

    def test_extendable(self):
        v = Validator()
        v.extend("numeric", numeric)

        validate = v.validate({"test": 1}, v.numeric(["test"]))

        self.assertEqual(len(validate), 0)

    def test_email(self):
        validate = Validator().validate({"email": "user@example.com"}, email(["email"]))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"email": "user"}, email(["email"]))

        self.assertEqual(
            validate.all(), {"email": ["The email must be a valid email address."]}
        )

    def test_email_with_one_letter_username(self):
        validate = Validator().validate({"email": "u@example.com"}, email(["email"]))
        self.assertEqual(len(validate), 0)

    def test_matches(self):
        validate = Validator().validate(
            {
                "password": "secret",
                "confirm": "secret",
            },
            matches("password", "confirm"),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "password": "secret",
                "confirm": "no-secret",
            },
            matches("password", "confirm"),
        )

        self.assertEqual(
            validate.all(), {"password": ["The password must match confirm."]}
        )

    def test_active_domain(self):
        validate = Validator().validate(
            {
                "domain1": "google.com",
                "domain2": "http://google.com",
                "domain3": "https://www.google.com",
                "email": "admin@gmail.com",
            },
            active_domain(["domain1", "domain2", "domain3", "email"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "domain1": "domain",
            },
            active_domain(["domain1"]),
        )

        self.assertEqual(
            validate.all(), {"domain1": ["The domain1 must be an active domain name."]}
        )

    def test_phone(self):
        validate = Validator().validate(
            {"phone": "876-182-1921"}, phone("phone", pattern="123-456-7890")
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"phone": "(876)182-1921"}, phone("phone", pattern="123-456-7890")
        )

        self.assertEqual(
            validate.all(), {"phone": ["The phone must be in the format XXX-XXX-XXXX."]}
        )

    def test_accepted(self):
        validate = Validator().validate({"terms": "on"}, accepted(["terms"]))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"terms": "test"}, accepted(["terms"]))

        self.assertEqual(validate.all(), {"terms": ["The terms must be accepted."]})

    def test_ip(self):
        validate = Validator().validate({"ip": "192.168.1.1"}, ip(["ip"]))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"ip": "test"}, ip(["ip"]))

        self.assertEqual(
            validate.all(), {"ip": ["The ip must be a valid ipv4 address."]}
        )

    def test_timezone(self):
        validate = Validator().validate(
            {"timezone": "America/New_York"}, timezone(["timezone"])
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"timezone": "test"}, timezone(["timezone"]))

        self.assertEqual(
            validate.all(), {"timezone": ["The timezone must be a valid timezone."]}
        )

    def test_exists(self):
        validate = Validator().validate(
            {
                "terms": "on",
                "user": "here",
            },
            exists(["user"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"terms": "test"}, exists(["user"]))

        self.assertEqual(validate.all(), {"user": ["The user must exist."]})

    def test_date(self):
        validate = Validator().validate(
            {
                "date": "1975-05-21T22:00:00",
            },
            date(["date"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "date": "woop",
            },
            date(["date"]),
        )

        self.assertEqual(validate.all(), {"date": ["The date must be a valid date."]})

    def test_before_today(self):
        validate = Validator().validate(
            {
                "date": "1975-05-21T22:00:00",
            },
            before_today(["date"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "date": pendulum.now().subtract(days=2).to_datetime_string(),
            },
            before_today(["date"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "date": "2030-05-21T22:00:00",
            },
            before_today(["date"]),
        )

        self.assertEqual(
            validate.all(), {"date": ["The date must be a date before today."]}
        )

    def test_after_today(self):
        validate = Validator().validate(
            {
                "date": "2030-05-21T22:00:00",
            },
            after_today(["date"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "date": pendulum.tomorrow().to_datetime_string(),
            },
            after_today(["date"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "date": "1975-05-21T22:00:00",
            },
            after_today(["date"]),
        )

        self.assertEqual(
            validate.all(), {"date": ["The date must be a date after today."]}
        )

    def test_is_past(self):
        validate = Validator().validate(
            {
                "date": "1950-05-21T22:00:00",
            },
            is_past(["date"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "date": pendulum.yesterday().to_datetime_string(),
            },
            is_past(["date"], tz="America/New_York"),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "date": pendulum.tomorrow().to_datetime_string(),
            },
            is_past("date", tz="America/New_York"),
        )

        self.assertEqual(
            validate.all(), {"date": ["The date must be a time in the past."]}
        )

    def test_is_future(self):
        validate = Validator().validate(
            {
                "date": "2030-05-21T22:00:00",
            },
            is_future(["date"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "date": pendulum.tomorrow().to_datetime_string(),
            },
            is_future(["date"], tz="America/New_York"),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "date": pendulum.yesterday().to_datetime_string(),
            },
            is_future(["date"]),
        )

        self.assertEqual(
            validate.all(), {"date": ["The date must be a time in the past."]}
        )

    def test_exception(self):
        with self.assertRaises(AttributeError) as e:
            validate = Validator().validate(
                {
                    "terms": "on",
                },
                required(["user"], raises={"user": AttributeError}),
            )

        try:
            validate = Validator().validate(
                {
                    "terms": "on",
                },
                required(["user"], raises={"user": AttributeError}),
            )
        except AttributeError as e:
            self.assertEqual(str(e), "The user field is required.")

        try:
            validate = Validator().validate(
                {
                    "terms": "on",
                },
                required(["user"], raises=True),
            )
        except ValueError as e:
            self.assertEqual(str(e), "The user field is required.")

    def test_conditional(self):
        validate = Validator().validate(
            {"terms": "on"}, when(accepted(["terms"])).then(required(["user"]))
        )

        self.assertEqual(validate.all(), {"user": ["The user field is required."]})

        validate = Validator().validate({"terms": "test"}, accepted(["terms"]))

        self.assertEqual(validate.all(), {"terms": ["The terms must be accepted."]})

    def test_error_message_required(self):
        validate = Validator().validate(
            {"test": 1},
            required(
                ["user", "email"], messages={"user": "there must be a user value"}
            ),
        )

        self.assertEqual(validate.get("user"), ["there must be a user value"])
        self.assertEqual(validate.get("email"), ["The email field is required."])

        validate = Validator().validate(
            {"test": 1},
            required(
                ["user", "email"], messages={"email": "there must be an email value"}
            ),
        )

        self.assertEqual(validate.get("user"), ["The user field is required."])
        self.assertEqual(validate.get("email"), ["there must be an email value"])

    def test_numeric(self):
        validate = Validator().validate({"test": 1}, numeric(["test"]))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"test": "hey"}, numeric(["test"]))

        self.assertEqual(validate.all(), {"test": ["The test must be a numeric."]})

    def test_several_tests(self):
        validate = Validator().validate(
            {"test": "hey"}, required(["notin"]), numeric(["notin"])
        )

        self.assertEqual(
            validate.all(),
            {"notin": ["The notin field is required.", "The notin must be a numeric."]},
        )

    def test_json(self):
        validate = Validator().validate({"json": "hey"}, vjson(["json"]))

        self.assertEqual(validate.all(), {"json": ["The json must be a valid JSON."]})

        validate = Validator().validate(
            {"json": json.dumps({"test": "key"})}, vjson(["json"])
        )

        self.assertEqual(len(validate), 0)

    def test_length(self):
        validate = Validator().validate(
            {"json": "hey"}, length(["json"], min=1, max=10)
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"json": "hey"}, length(["json"], "1..10"))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"json": "this is a really long string"}, length(["json"], min=1, max=10)
        )

        self.assertEqual(
            validate.all(), {"json": ["The json length must be between 1 and 10."]}
        )

        # test when only min given
        validate = Validator().validate({"json": "hoh"}, length(["json"], min=6))

        self.assertEqual(
            validate.all(), {"json": ["The json must be at least 6 characters."]}
        )

        # passing test when only min given
        validate = Validator().validate(
            {"json": "string which is long enough"}, length(["json"], min=6)
        )
        self.assertEqual(len(validate), 0)

        # test when only max given
        validate = Validator().validate(
            {"json": "this is a string too long"}, length(["json"], max=10)
        )

        self.assertEqual(
            validate.all(), {"json": ["The json length must be between 0 and 10."]}
        )

        # test that empty strings validates maximum length
        validate = Validator().validate({"json": ""}, length(["json"], max=10))
        self.assertEqual(len(validate), 0)

    def test_string(self):
        validate = Validator().validate({"text": "hey"}, string(["text"]))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"text": ["string1", "string2"]}, string(["text"])
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"text": 1}, string(["text"]))

        self.assertEqual(validate.all(), {"text": ["The text must be a string."]})

    def test_none(self):
        validate = Validator().validate({"text": None}, none(["text"]))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"text": 1}, none(["text"]))

        self.assertEqual(validate.all(), {"text": ["The text must be None."]})

    def test_equals(self):
        validate = Validator().validate({"text": "test1"}, equals(["text"], "test1"))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"text": "test2"}, equals(["text"], "test1"))

        self.assertEqual(validate.all(), {"text": ["The text must be equal to test1."]})

    def test_truthy(self):
        validate = Validator().validate({"text": "value"}, truthy(["text"]))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"text": 1}, truthy(["text"]))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"text": False}, truthy(["text"]))

        self.assertEqual(validate.all(), {"text": ["The text must be a truthy value."]})

    def test_in_range(self):
        validate = Validator().validate(
            {"text": 52}, in_range(["text"], min=25, max=72)
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"text": "1"}, in_range(["text"], min=1, max=10)
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"text": 1}, in_range(["text"], min=1, max=10))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"text": "hello"}, in_range(["text"], min=1, max=10)
        )

        self.assertEqual(validate.get("text"), ["The text must be between 1 and 10."])

        validate = Validator().validate(
            {"text": "1.5"}, in_range(["text"], min=1.5, max=5.5)
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"text": 101}, in_range(["text"], min=25, max=72)
        )

        self.assertEqual(
            validate.all(), {"text": ["The text must be between 25 and 72."]}
        )

    def test_greater_than(self):
        validate = Validator().validate({"text": 52}, greater_than(["text"], 25))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"text": 101}, greater_than(["text"], 150))

        self.assertEqual(
            validate.all(), {"text": ["The text must be greater than 150."]}
        )

    def test_less_than(self):
        validate = Validator().validate({"text": 10}, less_than(["text"], 25))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"text": 101}, less_than(["text"], 75))

        self.assertEqual(validate.all(), {"text": ["The text must be less than 75."]})

    def test_isnt(self):
        validate = Validator().validate(
            {"test": 50}, isnt(in_range(["test"], min=10, max=20))
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"test": 15}, isnt(in_range(["test"], min=10, max=20))
        )

        self.assertEqual(
            validate.all(), {"test": ["The test must not be between 10 and 20."]}
        )

    def test_isnt_equals(self):
        validate = Validator().validate(
            {"test": "test"},
            isnt(equals(["test"], "test"), length(["test"], min=10, max=20)),
        )

        self.assertEqual(
            validate.all(), {"test": ["The test must not be equal to test."]}
        )

    def test_contains(self):
        validate = Validator().validate(
            {"test": "this is a sentence"}, contains(["test"], "this")
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"test": "this is a not sentence"}, contains(["test"], "test")
        )

        self.assertEqual(validate.all(), {"test": ["The test must contain test."]})

    def test_is_in(self):
        validate = Validator().validate({"test": 1}, is_in(["test"], [1, 2, 3]))

        self.assertEqual(len(validate), 0)

        validate = Validator().validate({"test": 1}, is_in(["test"], [4, 2, 3]))

        self.assertEqual(
            validate.all(), {"test": ["The test must contain an element in [4, 2, 3]."]}
        )

    def test_when(self):
        validate = Validator().validate(
            {"email": "user@example.com", "phone": "123-456-7890"},
            when(isnt(required("email"))).then(required("phone")),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"email": "user@example.com"}, when(exists("email")).then(required("phone"))
        )

        self.assertEqual(validate.get("phone"), ["The phone field is required."])

        validate = Validator().validate(
            {"user": "user"}, when(exists("email")).then(required("phone"))
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "email": "user@example.com",
            },
            when(does_not(exists("email"))).then(required("phone")),
        )

        self.assertEqual(len(validate), 0)

    def test_does_not(self):
        validate = Validator().validate(
            {"phone": "123-456-7890"}, does_not(exists("email")).then(required("phone"))
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"email": "user@example.com", "phone": "123-456-7890"},
            does_not(exists("email")).then(required("phone")),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"user": "Joe"}, does_not(exists("email")).then(required("phone"))
        )

        self.assertEqual(validate.get("phone"), ["The phone field is required."])

    def test_one_of(self):
        validate = Validator().validate(
            {"email": "user@example.com", "phone": "123-456-7890"},
            one_of(["email", "phone"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"accepted": "on", "user": "Joe"}, one_of(["email", "phone"])
        )

        self.assertEqual(validate.get("email"), ["The email or phone is required."])
        self.assertEqual(validate.get("phone"), ["The email or phone is required."])

        validate = Validator().validate(
            {"accepted": "on", "user": "Joe"}, one_of(["email", "phone", "password"])
        )

        self.assertEqual(
            validate.get("email"), ["The email, phone, password is required."]
        )

        validate = Validator().validate(
            {"accepted": "on", "user": "Joe"},
            one_of(["email", "phone", "password", "user"]),
        )

        self.assertEqual(len(validate), 0)

    def test_regex(self):
        validate = Validator().validate(
            {
                "username": "masonite_user_1",
            },
            regex(["username"], "^[a-z0-9_-]{3,16}$"),
        )
        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"username": "Masonite User 2"}, regex(["username"], "^[a-z0-9_-]{3,16}$")
        )
        self.assertEqual(
            validate.get("username"),
            ["The username does not match pattern ^[a-z0-9_-]{3,16}$ ."],
        )

    def test_list_validation(self):
        validate = Validator().validate(
            {"name": "Joe", "discounts_ref": [1, 2, 3]},
            required(["name", "discounts_ref"]),
            numeric(["discounts_ref.*"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"name": "Joe", "discounts_ref": [1, 2, 3]},
            required(["name", "discounts_ref"]),
            length(["discounts_ref.*"], min=1, max=2),
        )

        self.assertEqual(len(validate), 0)

    def test_list_validation(self):
        validate = Validator().validate(
            {"name": "Joe", "discounts_ref": [1, 2, 3]},
            is_list(["discounts_ref.*"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"name": "Joe", "discounts_ref": {1: 2}},
            is_list(["discounts_ref.*"]),
        )

        self.assertEqual(len(validate), 1)

    def test_postal_code(self):
        validate = Validator().validate(
            {
                "postal_code": "not a post code",
            },
            postal_code(["postal_code"], "FR"),
        )
        self.assertEqual(
            validate.get("postal_code"),
            ["The postal_code is not a valid FR postal code. Valid example is 33380."],
        )

        validate = Validator().validate(
            {
                "postal_code": "44000",
            },
            postal_code(["postal_code"], "FR"),
        )
        self.assertEqual(len(validate), 0)

    def test_multiple_countries_for_postal_code(self):
        valid_postal_codes = ["EC1Y 8SY", "44000", "87832"]  # gb, fr, us
        for code in valid_postal_codes:
            validate = Validator().validate(
                {
                    "postal_code": code,
                },
                postal_code(["postal_code"], "FR,GB,US"),
            )
            self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "postal_code": "4430",
            },
            postal_code(["postal_code"], "FR,GB,US"),
        )
        self.assertEqual(
            validate.get("postal_code"),
            [
                "The postal_code is not a valid FR,GB,US postal code. Valid examples are 33380,EC1Y 8SY,95014."
            ],
        )

    def test_not_implemented_country_postal_code(self):
        try:
            validate = Validator().validate(
                {
                    "postal_code": "90988",
                },
                postal_code(["postal_code"], "XX"),
            )
        except NotImplementedError as e:
            self.assertEqual(
                str(e),
                "Unsupported country code XX. Check that it is a ISO 3166-1 country code or open a PR to require support of this country code.",
            )

    def test_file_validation(self):
        validate = Validator().validate(
            {
                "document": "a string",
            },
            file(["document"]),
        )

        self.assertEqual(
            validate.get("document"), ["The document is not a valid file."]
        )
        import os

        test_file = os.path.abspath(__file__)
        validate = Validator().validate({"document": test_file}, file(["document"]))
        self.assertEqual(len(validate), 0)

    def test_file_size_validation(self):
        import os

        # check that max size is 100 bytes
        test_file = os.path.abspath(__file__)
        validate = Validator().validate(
            {"document": test_file}, file(["document"], size=100)
        )
        self.assertEqual(
            validate.get("document"), ["The document file size exceeds 100 bytes."]
        )

        validate = Validator().validate(
            {"document": test_file}, file(["document"], size="2MB")
        )
        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"document": test_file}, file(["document"], size="4K")
        )
        self.assertEqual(
            validate.get("document"), ["The document file size exceeds 4 KB."]
        )

    def test_file_mime_types_validation(self):
        import os

        test_file = os.path.abspath(__file__)
        validate = Validator().validate(
            {"document": test_file},
            file(
                ["document"],
                mimes=[
                    "jpg",
                    "png",
                ],
            ),
        )
        self.assertEqual(
            validate.get("document"),
            ["The document mime type is not valid. Allowed formats are jpg,png."],
        )

        validate = Validator().validate(
            {"document": test_file},
            file(
                ["document"],
                mimes=[
                    "py",
                ],
            ),
        )
        self.assertEqual(len(validate), 0)

    def test_multiple_file_validations(self):
        import os

        test_file = os.path.abspath(__file__)
        validate = Validator().validate(
            {"document": test_file},
            file(
                ["document"],
                size=100,
                mimes=[
                    "jpg",
                    "png",
                ],
            ),
        )
        self.assertEqual(
            validate.get("document"),
            [
                "The document file size exceeds 100 bytes.",
                "The document mime type is not valid. Allowed formats are jpg,png.",
            ],
        )

    def test_image_validation(self):
        validate = Validator().validate(
            {
                "avatar": "a string",
            },
            image(["avatar"]),
        )

        self.assertEqual(validate.get("avatar"), ["The avatar is not a valid file."])

        import mimetypes

        image_extensions = [
            ext for ext, mt in mimetypes.types_map.items() if mt.startswith("image")
        ]

        import os

        test_file = os.path.abspath(__file__)  # python file
        validate = Validator().validate(
            {
                "avatar": test_file,
            },
            image(["avatar"]),
        )
        self.assertEqual(
            validate.get("avatar"),
            [
                "The avatar file is not a valid image. Allowed formats are {}.".format(
                    ",".join(image_extensions)
                )
            ],
        )

        import tempfile

        with tempfile.NamedTemporaryFile(dir="/tmp", suffix=".png") as tmpfile:
            test_image = tmpfile.name
            validate = Validator().validate({"avatar": test_image}, image(["avatar"]))

        self.assertEqual(len(validate), 0)

    def test_image_size_validation(self):
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(dir="/tmp", suffix=".png") as tmpfile:
            test_image = tmpfile.name
            tmpfile.write(b"dummy content to get a size around 40 bytes")
            tmpfile.flush()
            validate = Validator().validate(
                {"avatar": test_image}, image(["avatar"], size="2MB")
            )
            self.assertEqual(len(validate), 0)

            validate = Validator().validate(
                {"avatar": test_image}, image(["avatar"], size="20b")
            )
            self.assertEqual(
                validate.get("avatar"), ["The avatar file size exceeds 20 bytes."]
            )

    def test_video_validation(self):
        validate = Validator().validate(
            {
                "document": "a string",
            },
            video(["document"]),
        )

        self.assertEqual(
            validate.get("document"), ["The document is not a valid file."]
        )

        import mimetypes

        video_extensions = [
            ext for ext, mt in mimetypes.types_map.items() if mt.startswith("video")
        ]

        import os

        test_file = os.path.abspath(__file__)  # python file
        validate = Validator().validate(
            {
                "document": test_file,
            },
            video(["document"]),
        )
        self.assertEqual(
            validate.get("document"),
            [
                "The document file is not a valid video. Allowed formats are {}.".format(
                    ",".join(video_extensions)
                )
            ],
        )

        import tempfile

        with tempfile.NamedTemporaryFile(dir="/tmp", suffix=".mp4") as tmpfile:
            test_video = tmpfile.name
            validate = Validator().validate(
                {"document": test_video}, video(["document"])
            )

        self.assertEqual(len(validate), 0)

    def test_different(self):
        validate = Validator().validate(
            {"field_1": "value_1", "field_2": "value_2"},
            different(["field_1"], "field_2"),
        )
        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"field_1": "value_1", "field_2": "value_1"},
            different(["field_1"], "field_2"),
        )
        self.assertEqual(
            validate.get("field_1"),
            ["The field_1 value must be different than field_2 value."],
        )

        validate = Validator().validate(
            {"field_1": None, "field_2": None}, different(["field_1"], "field_2")
        )
        self.assertEqual(
            validate.get("field_1"),
            ["The field_1 value must be different than field_2 value."],
        )

    def test_that_default_uuid_must_be_uuid4(self):
        from uuid import NAMESPACE_DNS

        u3 = uuid3(NAMESPACE_DNS, "domain.com")
        u5 = uuid5(NAMESPACE_DNS, "domain.com")
        for uuid_value in [uuid1(), u3, u5]:
            validate = Validator().validate(
                {
                    "document_id": uuid_value,
                },
                uuid(["document_id"]),
            )
            self.assertEqual(
                validate.get("document_id"),
                ["The document_id value must be a valid UUID 4."],
            )

        validate = Validator().validate(
            {
                "document_id": uuid4(),
            },
            uuid(["document_id"], 4),
        )
        self.assertEqual(len(validate), 0)

    def test_invalid_uuid_values(self):
        for uuid_value in [None, [], True, "", "uuid", {"uuid": "nope"}, 3, ()]:
            validate = Validator().validate(
                {
                    "document_id": uuid_value,
                },
                uuid(["document_id"]),
            )
            self.assertEqual(
                validate.get("document_id"),
                ["The document_id value must be a valid UUID 4."],
            )

    def test_uuid_rule_with_specified_versions(self):
        from uuid import NAMESPACE_DNS

        u3 = uuid3(NAMESPACE_DNS, "domain.com")
        u5 = uuid5(NAMESPACE_DNS, "domain.com")
        for version, uuid_value in [(1, uuid1()), (3, u3), (4, uuid4()), (5, u5)]:
            validate = Validator().validate(
                {
                    "document_id": uuid_value,
                },
                uuid(["document_id"], version),
            )
            self.assertEqual(len(validate), 0)

    def test_invalid_uuid_rule_with_specified_versions(self):
        for version in [1, 2, 3, 5]:
            validate = Validator().validate(
                {
                    "document_id": uuid4(),
                },
                uuid(["document_id"], version),
            )
            self.assertEqual(
                validate.get("document_id"),
                ["The document_id value must be a valid UUID {0}.".format(version)],
            )

    def test_uuid_version_can_be_str_or_int(self):
        uuid_value = uuid4()
        for version in [4, "4"]:
            validate = Validator().validate(
                {
                    "document_id": uuid_value,
                },
                uuid(["document_id"], version),
            )
            self.assertEqual(len(validate), 0)
        for version in [3, "3"]:
            validate = Validator().validate(
                {
                    "document_id": uuid_value,
                },
                uuid(["document_id"], version),
            )
            self.assertEqual(
                validate.get("document_id"),
                ["The document_id value must be a valid UUID 3."],
            )

    def test_required_if_rule_when_other_field_is_present(self):
        validate = Validator().validate(
            {"first_name": "Sam", "last_name": "Gamji"},
            required_if(["last_name"], "first_name", "Sam"),
        )
        self.assertEqual(len(validate), 0)
        validate = Validator().validate(
            {"first_name": "Sam", "last_name": ""},
            required_if(["last_name"], "first_name", "Sam"),
        )
        self.assertEqual(
            validate.get("last_name"),
            ["The last_name is required because first_name=Sam."],
        )
        validate = Validator().validate(
            {"first_name": "Sam", "last_name": ""},
            required_if(["last_name"], "first_name", "Joe"),
        )
        self.assertEqual(len(validate), 0)

    def test_required_if_rule_when_other_field_is_not_present(self):
        validate = Validator().validate(
            {
                "first_name": "Sam",
            },
            required_if(["last_name"], "first_name", "Sam"),
        )
        self.assertEqual(
            validate.get("last_name"),
            ["The last_name is required because first_name=Sam."],
        )
        validate = Validator().validate(
            {
                "first_name": "Sam",
            },
            required_if(["last_name"], "first_name", "Joe"),
        )
        self.assertEqual(len(validate), 0)

    def test_required_with_rule(self):
        validate = Validator().validate(
            {"first_name": "Sam", "last_name": "Gamji", "email": "samgamji@loftr.com"},
            required_with(["email"], ["first_name", "last_name" "nick_name"]),
        )
        self.assertEqual(len(validate), 0)
        validate = Validator().validate(
            {"first_name": "Sam", "email": "samgamji@loftr.com"},
            required_with(["email"], "first_name"),
        )
        self.assertEqual(len(validate), 0)
        validate = Validator().validate(
            {"first_name": "Sam", "email": ""}, required_with(["email"], "first_name")
        )
        self.assertEqual(
            validate.get("email"),
            ["The email is required because first_name is present."],
        )
        validate = Validator().validate(
            {"first_name": "Sam", "email": ""},
            required_with(["email"], "first_name,nick_name"),
        )
        self.assertEqual(
            validate.get("email"),
            ["The email is required because one in first_name,nick_name is present."],
        )

    def test_required_with_rule_with_comma_separated_fields(self):
        validate = Validator().validate(
            {"nick_name": "Sam", "email": "samgamji@loftr.com"},
            required_with(["email"], "first_name,last_name,nick_name"),
        )
        self.assertEqual(len(validate), 0)
        validate = Validator().validate(
            {
                "nick_name": "Sam",
            },
            required_with(["email"], "first_name,nick_name"),
        )
        self.assertEqual(
            validate.get("email"),
            ["The email is required because one in first_name,nick_name is present."],
        )

    def test_distinct(self):
        validate = Validator().validate(
            {
                "users": [
                    {
                        "first_name": "John",
                        "last_name": "Masonite",
                    },
                    {
                        "first_name": "Joe",
                        "last_name": "Masonite",
                    },
                ]
            },
            distinct(["users.*.last_name"]),
        )
        self.assertEqual(
            validate.get("users.*.last_name"),
            ["The users.*.last_name field has duplicate values."],
        )
        validate = Validator().validate(
            {
                "users": [
                    {
                        "id": 1,
                        "name": "John",
                    },
                    {
                        "id": 2,
                        "name": "Nick",
                    },
                ]
            },
            distinct(["users.*.id"]),
        )
        self.assertEqual(len(validate), 0)

    def test_distinct_with_simple_list(self):
        validate = Validator().validate(
            {"emails": ["john@masonite.com", "joe@masonite.com", "john@masonite.com"]},
            distinct(["emails"]),
        )
        self.assertEqual(
            validate.get("emails"), ["The emails field has duplicate values."]
        )


class TestDotNotationValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_dot_required(self):
        validate = Validator().validate(
            {"user": {"email": "user@example.com"}}, required(["user.id"])
        )

        self.assertEqual(
            validate.all(), {"user.id": ["The user.id field is required."]}
        )

        validate = Validator().validate({"user": {"id": 1}}, required(["user.id"]))

        self.assertEqual(len(validate), 0)

    def test_dot_numeric(self):
        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com"}}, numeric(["user.id"])
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com"}}, numeric(["user.email"])
        )

        self.assertEqual(
            validate.all(), {"user.email": ["The user.email must be a numeric."]}
        )

    def test_dot_several_tests(self):
        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com"}},
            required(["user.id", "user.email"]),
            numeric(["user.id"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com"}},
            required(["user.id", "user.email"]),
            numeric(["user.email"]),
        )

        self.assertEqual(
            validate.all(), {"user.email": ["The user.email must be a numeric."]}
        )

    def test_dot_json(self):
        validate = Validator().validate(
            {"user": {"id": "hey", "email": "user@example.com"}}, vjson(["user.id"])
        )

        self.assertEqual(
            validate.all(), {"user.id": ["The user.id must be a valid JSON."]}
        )

        validate = Validator().validate(
            {
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "payload": json.dumps({"test": "key"}),
                }
            },
            vjson(["user.payload"]),
        )

        self.assertEqual(len(validate), 0)

    def test_dot_length(self):
        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com"}},
            length(["user.id"], min=1, max=10),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "description": "this is a really long description",
                }
            },
            length(["user.id"], "1..10"),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "description": "this is a really long description",
                }
            },
            length(["user.description"], min=1, max=10),
        )

        self.assertEqual(
            validate.all(),
            {
                "user.description": [
                    "The user.description length must be between 1 and 10."
                ]
            },
        )

    def test_dot_in_range(self):
        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com", "age": 25}},
            in_range(["user.age"], min=25, max=72),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com", "age": 25}},
            in_range(["user.age"], min=27, max=72),
        )

        self.assertEqual(
            validate.all(), {"user.age": ["The user.age must be between 27 and 72."]}
        )

        validate = Validator().validate(
            {"data": {"value": "1.5"}},
            in_range(["data.value"], min=2, max=2.5),
        )

        self.assertEqual(
            validate.all(),
            {"data.value": ["The data.value must be between 2 and 2.5."]},
        )

    def test_dot_equals(self):
        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com", "age": 25}},
            equals(["user.age"], 25),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com", "age": 25}},
            equals(["user.age"], "test1"),
        )

        self.assertEqual(
            validate.all(), {"user.age": ["The user.age must be equal to test1."]}
        )

    def test_can_use_asterisk(self):
        validate = Validator().validate(
            {
                "user": {
                    "id": 1,
                    "addresses": [
                        {"id": 1, "street": "A Street"},
                        {"id": 2, "street": "B Street"},
                        {"id": 3, "street": "C Street"},
                    ],
                    "age": 25,
                }
            },
            required(["user.addresses.*.id"]),
            equals("user.addresses.*.id", [1, 2, 3]),
        )

        self.assertEqual(len(validate), 0, validate)

        validate = Validator().validate(
            {
                "user": {
                    "id": 1,
                    "addresses": [
                        {"id": 1, "street": "A Street"},
                        {"id": 2, "street": "B Street"},
                        {"id": 3, "street": "C Street"},
                    ],
                    "age": 25,
                }
            },
            required(["user.addresses.*.house"]),
        )

        self.assertEqual(
            validate.all(),
            {
                "user.addresses.*.house": [
                    "The user.addresses.*.house field is required."
                ]
            },
        )

        validate = Validator().validate(
            {"user": {"id": 1, "addresses": [], "age": 25}},
            required(["user.addresses.*.id"]),
        )

        self.assertEqual(
            validate.all(),
            {"user.addresses.*.id": ["The user.addresses.*.id field is required."]},
        )

    def test_dot_error_message_required(self):
        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com", "age": 25}},
            required(
                ["user.description"],
                messages={"user.description": "You are missing a description"},
            ),
        )

        self.assertEqual(
            validate.all(), {"user.description": ["You are missing a description"]}
        )

        validate = Validator().validate(
            {"user": {"id": 1, "email": "user@example.com"}},
            required(
                ["user.id", "user.email", "user.age"],
                messages={"user.age": "You are missing a user age"},
            ),
        )

        self.assertEqual(validate.all(), {"user.age": ["You are missing a user age"]})


class TestValidationFactory(unittest.TestCase):
    def test_can_register(self):
        factory = ValidationFactory()
        factory.register(required)
        self.assertEqual(factory.registry["required"], required)


class TestValidationProvider(TestCase):
    def setUp(self):
        super().setUp()
        self.provider = ValidationProvider(self.application)
        self.application.resolve(self.provider.boot)

    def test_loaded_validator_class(self):
        self.assertIsInstance(self.application.make(Validator), Validator)

    def test_loaded_registry(self):
        self.assertTrue(self.application.make(Validator).numeric)

    def test_request_validation(self):
        request = self.make_request(query_string="id=1&name=Joe")
        validate = self.application.make("validator")

        validated = request.validate(validate.required(["id", "name"]))

        self.assertEqual(len(validated), 0)

        validated = request.validate(validate.required(["user"]))

        self.assertEqual(validated.all(), {"user": ["The user field is required."]})

    # def test_request_validation_redirects_back_with_session(self):
    #     wsgi = generate_wsgi()
    #     self.application.bind("Application", self.application)
    #     self.application.bind("SessionCookieDriver", SessionCookieDriver)
    #     self.application.bind("Environ", wsgi)

    #     request = self.application.make("Request")
    #     request.load_environ(wsgi)

    #     request.request_variables = {"id": 1, "name": "Joe"}

    #     errors = request.validate(required("user"))

    #     request.session = SessionManager(self.app).driver("cookie")
    #     request.key("UKLAdrye6pZG4psVRPZytukJo2-A_Zxbo0VaqR5oig8=")
    #     self.assertEqual(
    #         request.redirect("/login").with_errors(errors).redirect_url, "/login"
    #     )
    #     self.assertEqual(
    #         request.redirect("/login").with_errors(errors).session.get("errors"),
    #         {"user": ["The user field is required."]},
    #     )

    def test_confirmed(self):
        validate = Validator().validate(
            {
                "password": "secret",
                "password_confirmation": "secret",
            },
            confirmed(["password"]),
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {
                "password": "secret",
            },
            confirmed(["password"]),
        )

        self.assertEqual(
            validate.all(), {"password": ["The password confirmation does not match."]}
        )

        validate = Validator().validate({}, confirmed(["password"]))

        self.assertEqual(
            validate.all(), {"password": ["The password confirmation does not match."]}
        )

        validate = Validator().validate(
            {
                "password": "secret",
                "password_confirmation": "foo",
            },
            confirmed(["password"]),
        )

        self.assertEqual(
            validate.all(), {"password": ["The password confirmation does not match."]}
        )

    def test_strong(self):
        validate = Validator().validate(
            {
                "password": "secret",
            },
            strong(["password"], uppercase=0, special=0, numbers=0),
        )

        self.assertEqual(
            validate.all(),
            {"password": ["The password field must be 8 characters in length"]},
        )

        validate = Validator().validate(
            {
                "password": "Secret",
            },
            strong(["password"], length=5, uppercase=2, special=0, numbers=0),
        )

        self.assertEqual(
            validate.all(),
            {"password": ["The password field must have 2 uppercase letters"]},
        )

        validate = Validator().validate(
            {
                "password": "secret!",
            },
            strong(["password"], length=5, uppercase=0, special=2, numbers=0),
        )

        self.assertEqual(
            validate.all(),
            {"password": ["The password field must have 2 special characters"]},
        )

        validate = Validator().validate(
            {
                "password": "secret!",
            },
            strong(["password"], length=5, uppercase=0, special=0, numbers=2),
        )

        self.assertEqual(
            validate.all(), {"password": ["The password field must have 2 numbers"]}
        )

        validate = Validator().validate(
            {
                "password": "secret!",
            },
            strong(["password"], length=8, uppercase=2, special=2, numbers=2),
        )

        password_validation = validate.get("password")
        self.assertIn("The password field must have 2 numbers", password_validation)
        self.assertIn(
            "The password field must be 8 characters in length", password_validation
        )

        self.assertIn(
            "The password field must have 2 uppercase letters", password_validation
        )

        self.assertIn(
            "The password field must have 2 special characters", password_validation
        )

        validate = Validator().validate(
            {
                "password": "secret!!",
            },
            strong(["password"], length=8, uppercase=0, special=2, numbers=0),
        )

        self.assertEqual(
            len(validate.all()),
            0,
        )

    def test_strong_breach(self):
        validate = Validator().validate(
            {
                "password": "secret",
            },
            strong(["password"], breach=True),
        )

        password_validation = validate.get("password")
        self.assertIn(
            "The password field has been breached in the past. Try another password",
            password_validation,
        )


class MockRuleEnclosure(RuleEnclosure):
    def rules(self):
        return [required(["username", "email"]), accepted("terms")]


class TestRuleEnclosure(unittest.TestCase):
    def test_enclosure_can_encapsulate_rules(self):
        validate = Validator().validate(
            {"username": "user123", "email": "user@example.com", "terms": "on"},
            MockRuleEnclosure,
        )

        self.assertEqual(len(validate), 0)

        validate = Validator().validate(
            {"email": "user@example.com", "terms": "on"}, MockRuleEnclosure
        )

        self.assertEqual(len(validate), 1)


class TestDictValidation(unittest.TestCase):
    def test_dictionary(self):
        validate = Validator().validate(
            {"test": 1, "terms": "on", "name": "Joe", "age": "25"},
            {
                "test": "required|truthy",
                "terms": "accepted",
                "name": "required|equals:Joe",
                "age": "required|greater_than:18",
            },
        )

        self.assertEqual(len(validate), 0)

    def test_required_with_string_validation(self):
        validate = Validator().validate(
            {"first_name": "Sam", "email": "samgamji@loftr.com"},
            {"email": "required_with:first_name,last_name"},
        )
        self.assertEqual(len(validate), 0)
        # with one argument
        validate = Validator().validate(
            {"email": ""}, {"email": "required_with:first_name"}
        )
        self.assertEqual(len(validate), 0)
        validate = Validator().validate(
            {"first_name": "Sam", "email": ""},
            {"email": "required_with:first_name,nick_name"},
        )
        self.assertIn(
            "The email is required because one in first_name,nick_name is present.",
            validate.get("email"),
        )
