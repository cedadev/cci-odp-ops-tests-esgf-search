#!/usr/bin/env python
"""Test CCI Open Data Portal CSW service
"""
__author__ = "P J Kershaw"
__date__ = "07/11/17"
__copyright__ = "(C) 2017 Science and Technology Facilities Council"
__license__ = """BSD - See LICENSE file in top-level directory"""
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
import unittest

import requests

from pyesgf.search import SearchConnection


class EsgfSearchTestCase(unittest.TestCase):
    '''Unit test case for testing ESA CCI Open Data Portal ESGF Search
    Service'''

    ESGF_SEARCH_URI = 'http://esgf-index1.ceda.ac.uk/esg-search'
    ESGF_SEARCH_CCI_PROJ_NAME = 'esacci'
    MIN_EXPTD_DATASETS = 200

    def test01_search(self):
        conn = SearchConnection(self.__class__.ESGF_SEARCH_URI, distrib=False)
        ctx = conn.new_context(project=self.__class__.ESGF_SEARCH_CCI_PROJ_NAME)

        try:
            results = ctx.search()
        except requests.exceptions.ConnectionError as exc:
            self.fail('Connection error: {}'.format(exc))

        self.assertGreater(len(results), self.__class__.MIN_EXPTD_DATASETS,
                           msg='Expecting at least 200 datasets returned from'
                               ' search')
        print("Found: {:d} datasets".format(len(results)))

        ds = results[0]

        self.assertTrue(ds, msg='Expecting non-null first dataset ID')
        print("First dataset ID: {}".format(ds.dataset_id))

        f1 = ds.file_context().search()[0]
        self.assertTrue(f1, msg='Expecting non-null first download URL')
        print("First file in that dataset: {}".format(f1.download_url))

