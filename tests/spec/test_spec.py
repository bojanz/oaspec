#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Platform.sh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest
from jsonschema.exceptions import ValidationError
from pathlib import Path
from oaspec.spec import OASpecParser
from oaspec.schema import OASpecParserError
from oaspec.utils import yaml

import json
from oaspec.utils import yaml

def get_test_data(file_path):
    return Path.cwd() / "tests/data" / file_path

def load_yaml(file_path):
    with Path(file_path).open('r', encoding='utf-8') as f:
        return yaml.load(f)

def load_json(file_path):
    with Path(file_path).open('r', encoding='utf-8') as f:
        return json.load(f)

class TestCreateOASpec(object):

    def test_create_object_with_yaml_file(self):

        spec_path_string = str(get_test_data("petstore-3.0.1.yaml"))
        oas = OASpecParser(spec=spec_path_string)

        assert str(oas._spec_file) == spec_path_string
        assert oas._raw_spec.keys() == load_yaml(spec_path_string).keys()
        assert oas._raw_spec == load_yaml(spec_path_string)

    def test_create_object_with_json_file(self):

        spec_path_string = str(get_test_data("petstore-3.0.1.json"))
        oas = OASpecParser(spec=spec_path_string)

        assert str(oas._spec_file) == spec_path_string
        assert oas._raw_spec.keys() == load_json(spec_path_string).keys()
        assert oas._raw_spec == load_json(spec_path_string)

    def test_create_object_with_yaml_raw(self):

        spec_path = get_test_data("petstore-3.0.1.yaml")
        with spec_path.open('r', encoding='utf-8') as f:
            raw_spec = f.read()

        oas = OASpecParser(spec=raw_spec)

        assert oas._spec_file == None
        assert oas._raw_spec.keys() == load_yaml(str(spec_path)).keys()
        assert oas._raw_spec == load_yaml(str(spec_path))

    def test_create_object_with_json_raw(self):

        spec_path = get_test_data("petstore-3.0.1.json")
        with spec_path.open('r', encoding='utf-8') as f:
            raw_spec = f.read()

        oas = OASpecParser(spec=raw_spec)

        assert oas._spec_file == None
        assert oas._raw_spec.keys() == load_json(str(spec_path)).keys()
        assert oas._raw_spec == load_json(str(spec_path))

    def test_create_object_with_json_dict(self):

        spec_path = get_test_data("petstore-3.0.1.json")
        with spec_path.open('r', encoding='utf-8') as f:
            dict_spec = json.load(f)

        oas = OASpecParser(spec=dict_spec)

        assert oas._spec_file == None
        assert oas._raw_spec.keys() == load_json(str(spec_path)).keys()
        assert oas._raw_spec == load_json(str(spec_path))

    def test_create_object_with_yaml_dict(self):

        spec_path = get_test_data("petstore-3.0.1.yaml")
        with spec_path.open('r', encoding='utf-8') as f:
            dict_spec = yaml.load(f)

        oas = OASpecParser(spec=dict_spec)

        assert oas._spec_file == None
        assert oas._raw_spec.keys() == load_yaml(str(spec_path)).keys()
        assert oas._raw_spec == load_yaml(str(spec_path))

    def test_create_object_with_other_raw_spec(self):

        spec_path_string = str(get_test_data("petstore-3.0.1.yaml"))
        oas = OASpecParser(spec=spec_path_string)

        second_oas = OASpecParser(spec=oas._raw_spec)

        assert second_oas._spec_file == None
        assert second_oas._raw_spec.keys() == oas._raw_spec.keys()
        assert second_oas._raw_spec == oas._raw_spec

        assert second_oas._raw_spec.keys() == load_yaml(spec_path_string).keys()
        assert second_oas._raw_spec == load_yaml(spec_path_string)

    def test_create_object_with_loaded_yaml(self):

        spec_path_string = str(get_test_data("petstore-3.0.1.yaml"))
        oas = OASpecParser()

        oas.load_file(spec_path_string)

        assert str(oas._spec_file) == spec_path_string
        assert oas._raw_spec.keys() == load_yaml(spec_path_string).keys()
        assert oas._raw_spec == load_yaml(spec_path_string)

    def test_create_object_with_loaded_json(self):

        spec_path_string = str(get_test_data("petstore-3.0.1.json"))
        oas = OASpecParser()

        oas.load_file(spec_path_string)

        assert str(oas._spec_file) == spec_path_string
        assert oas._raw_spec.keys() == load_json(spec_path_string).keys()
        assert oas._raw_spec == load_json(spec_path_string)

    def test_create_object_with_parsed_yaml(self):

        spec_path = get_test_data("petstore-3.0.1.yaml")
        spec_path_string = str(spec_path)
        with spec_path.open('r', encoding='utf-8') as f:
            raw_spec = f.read()

        oas = OASpecParser()
        oas.load_raw(raw_spec)

        assert oas._spec_file == None
        assert oas._raw_spec.keys() == load_yaml(spec_path_string).keys()
        assert oas._raw_spec == load_yaml(spec_path_string)

    def test_create_object_with_invalid_type(self):

        with pytest.raises(TypeError):
            oas = OASpecParser(spec=list())

class TestOASpecParser(object):

    def test_version_parser(self):
        spec_path_string = str(get_test_data("petstore-3.0.1.yaml"))
        oas = OASpecParser(spec=spec_path_string)
        spec = oas.parse_spec()

        assert spec.openapi == "3.0.1"

    def test_invalid_version_variations(self):
        variations = [
            "1.0.0",
            "2.0.0",
            "3.0",
            "3",
            "3.100.0",
            "3.0.100"
        ]

        for ver in variations:
            raw_spec = f"""
                openapi: "{ver}"
                info:
                version: 1.0.0
                title: Swagger Petstore
                license:
                    name: MIT
            """
            
            with pytest.raises(OASpecParserError) as excinfo:
                oas = OASpecParser(spec=raw_spec)
                oas.parse_spec()

                assert "Invalid version number" in str(excinfo.value)

    def test_version_missing(self):
        spec_path_string = str(get_test_data("petstore-3.0.1.yaml"))
        oas = OASpecParser(spec=spec_path_string)

        del oas._raw_spec["openapi"]
        with pytest.raises(ValidationError) as excinfo:
            oas.parse_spec()

        assert "'openapi' is a required property" in str(excinfo.value)
