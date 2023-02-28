import app
import config
import pytest
import os


def test_retrieve_google_place():
    output_list = app.retrieve_google_place(api_key=config.API_KEY, coordinate=config.LOCATION, radius=5000)

    assert isinstance(output_list, list)
    assert config.API_KEY == 'abc'