#!/usr/bin/env python3
# -*- coding=utf-8 -*- 

import pyvo

import sys
import warnings

from astropy.table import Table



if not sys.warnoptions:
    warnings.simplefilter("ignore")

QUERY="""
SELECT
   TOP 50
   *
   FROM ivoa.obscore AS db
   JOIN TAP_UPLOAD.lt AS mine
   ON 1=CONTAINS (POINT('ICRS', db.s_ra, db.s_dec),
                 CIRCLE('ICRS', mine.RA, mine.Decl, mine.Beta))
   AND db.dataproduct_type='image'
"""

# Try with the table of neutrinos from example2 
try:
  lt = Table.read('../example2/neutrinos.vot', format='votable')

# Or get the fallback file
except: 
  lt = Table.read('fallback.vot', format='votable')

# Make Service Object
service = pyvo.dal.TAPService ("http://dc.zah.uni-heidelberg.de/tap")

# Run Search on obscore table on the GAVO dc
result = service.run_async(query=QUERY, uploads={"lt":lt})

# Send resulting table to Topcat via SAMP
result.broadcast_samp("topcat")
