from tests import TestCase
from src.masonite.pipeline import Pipeline
from src.masonite.request import Request
import os


class PipeTestOne:
    def handle(self, request, response):
        request.one = 1

        return request


class PipeTestTwo:
    def handle(self, request, response):
        request.two = 2

        return request


class PipeTestBreak:
    def handle(self, request, response):

        return response


class PipeTestThree:
    def handle(self, request, response):
        request.three = 3

        return request


class TestPipeline(TestCase):
    def test_pipeline_sets_attributes(self):
        request = Request({})
        request2 = Request({})
        pipeline = Pipeline(request, request2).through([PipeTestOne, PipeTestTwo])
        self.assertTrue(request.one == 1)
        self.assertTrue(request.two == 2)

    def test_pipeline_exits(self):
        request = Request({})
        request2 = Request({})
        pipeline = Pipeline(request, request2).through([PipeTestOne, PipeTestBreak])
        self.assertTrue(request.one == 1)
        with self.assertRaises(AttributeError):
            self.assertTrue(request.two == 2)
