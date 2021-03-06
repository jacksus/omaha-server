# coding: utf8

"""
This software is licensed under the Apache 2 license, quoted below.

Copyright 2014 Crystalnix Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""

import os

from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase

from crash.serializers import SymbolsSerializer
from crash.models import Symbols
from crash.factories import SymbolsFactory

from omaha.tests.utils import temporary_media_root
from omaha.tests.test_api import BaseTest


BASE_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(BASE_DIR, 'testdata')
SYM_FILE = os.path.join(TEST_DATA_DIR, 'BreakpadTestApp.sym')


class VersionTest(BaseTest, APITestCase):
    url = reverse('symbols-list')
    url_detail = 'symbols-detail'
    factory = SymbolsFactory
    serializer = SymbolsSerializer

    @temporary_media_root(MEDIA_URL='http://cache.pack.google.com/edgedl/chrome/install/782.112/')
    def test_detail(self):
        super(VersionTest, self).test_detail()

    @temporary_media_root(MEDIA_URL='http://cache.pack.google.com/edgedl/chrome/install/782.112/')
    def test_list(self):
        super(VersionTest, self).test_list()

    @temporary_media_root(MEDIA_URL='http://cache.pack.google.com/edgedl/chrome/install/782.112/')
    def test_create(self):
        with open(SYM_FILE, 'rb') as f:
            data = dict(file=SimpleUploadedFile('./BreakpadTestApp.sym', f.read()))
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        symbols = Symbols.objects.get(id=response.data['id'])
        self.assertEqual(response.data, self.serializer(symbols).data)
        self.assertEqual(symbols.debug_id, 'C1C0FA629EAA4B4D9DD2ADE270A231CC1')
        self.assertEqual(symbols.debug_file, 'BreakpadTestApp.pdb')
