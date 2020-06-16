# -*- coding: utf-8 -*-
# ------------------------------
# PSE Tape Structure
# ------------------------------
# Total size: 19456 octets
#
# Old format                       New format (due to SPZ broken)
#   Header size: 16 octets           Header size: 16 octets
#   Frame size:  72 octets x 270     Frame size:  36 octets x 540
#
# -----------------------------    -----------------------------
# |    header (16 octets)     |    |    header (16 octets)     |
# |---------------------------|    |---------------------------|
# |    frame1 (72 octets)     |    |    frame1 (36 octets)     |
# |                           |    |---------------------------|
# |                           |    |    frame2 (36 octets)     |
# |---------------------------|    |---------------------------|
# |    frame2 (72 octets)     |    |    frame3 (36 octets)     |
# |                           |    |---------------------------|
# |                           |    |    frame4 (36 octets)     |
# |---------------------------|    |---------------------------|
# |    ...                    |    |    ...                    |
# |---------------------------|    |---------------------------|
# |    frame270 (72 octets)   |    |    frame539 (36 octets)   |
# |                           |    |---------------------------|
# |                           |    |    frame540 (36 octets)   |
# |---------------------------|    |---------------------------|
# |    header (16 octets)     |    |    header (16 octets)     |
# |---------------------------|    |---------------------------|
# |    frame1 (72 octets)     |    |    frame1 (36 octets)     |
# |                           |    |---------------------------|
# |                           |    |    frame2 (36 octets)     |
# |---------------------------|    |---------------------------|
# |    ...                    |    |    ...                    |
# |---------------------------|    |---------------------------|
#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA


SIZE_PSE_RECORD = 19456
SIZE_RECORD_HEADER = 16
SIZE_DATA_PART_OLD = 72
SIZE_DATA_PART_NEW = 36
NUMBER_OF_FRAMES_OLD = 270
NUMBER_OF_FRAMES_NEW = 540
