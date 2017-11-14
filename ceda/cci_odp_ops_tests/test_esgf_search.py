#!/usr/bin/env python
"""Test CCI Open Data Portal CSW service
"""
from nagiosplugin import result
__author__ = "P J Kershaw"
__date__ = "07/11/17"
__copyright__ = "(C) 2017 Science and Technology Facilities Council"
__license__ = """BSD - See LICENSE file in top-level directory"""
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
import unittest

import requests

from pyesgf.search import SearchConnection, results


class EsgfSearchTestCase(unittest.TestCase):
    '''Unit test case for testing ESA CCI Open Data Portal ESGF Search
    Service'''

    ESGF_SEARCH_URI = 'http://esgf-index1.ceda.ac.uk/esg-search'
    ESGF_SEARCH_CCI_PROJ_NAME = 'esacci'
    MIN_EXPTD_DATASETS = 200
    MIN_EXPTD_SOILMOISTURE_DATASETS = 9
    MIN_EXPTD_OCEANCOLOUR_DATASETS = 100

    @classmethod
    def _search(cls, **search_kwargs):
        conn = SearchConnection(cls.ESGF_SEARCH_URI, distrib=False)
        ctx = conn.new_context(project=cls.ESGF_SEARCH_CCI_PROJ_NAME,
                               **search_kwargs)

        results = ctx.search()
        return results

    def test01_search_all(self):
        results = self.__class__._search()
        self.assertGreater(len(results), self.__class__.MIN_EXPTD_DATASETS-1,
                           msg='Expecting at least {:d} datasets returned from'
                               ' search'.format(
                               self.__class__.MIN_EXPTD_DATASETS))

        ds = results[0]

        self.assertTrue(ds, msg='Expecting non-null first dataset ID')

        f1 = ds.file_context().search()[0]
        self.assertTrue(f1, msg='Expecting non-null first download URL')

    def test02_search_soilmoisture(self):
        results = self.__class__._search(cci_project="SOILMOISTURE")
        self.assertGreater(len(results),
                           self.__class__.MIN_EXPTD_SOILMOISTURE_DATASETS-1,
                           msg='Expecting at least {:d} datasets returned from'
                               ' search'.format(
                               self.__class__.MIN_EXPTD_SOILMOISTURE_DATASETS))

        ds = results[0]

        self.assertTrue(ds, msg='Expecting non-null first dataset ID')

        f1 = ds.file_context().search()[0]
        self.assertTrue(f1, msg='Expecting non-null first download URL')

    def test03_search_oceancolour(self):
        results = self.__class__._search(cci_project="OC")
        self.assertGreater(len(results),
                           self.__class__.MIN_EXPTD_OCEANCOLOUR_DATASETS-1,
                           msg='Expecting at least {:d} datasets returned from'
                               ' search'.format(
                                self.__class__.MIN_EXPTD_OCEANCOLOUR_DATASETS))

        ds = results[0]

        self.assertTrue(ds, msg='Expecting non-null first dataset ID')

        f1 = ds.file_context().search()[0]
        self.assertTrue(f1, msg='Expecting non-null first download URL')
