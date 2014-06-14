#!/usr/bin/env python
"""
Tests the cdl related functions of cdl_convert

REQUIREMENTS:

mock
"""

#==============================================================================
# IMPORTS
#==============================================================================

# Standard Imports
try:
    from unittest import mock
except ImportError:
    import mock
import os
import sys
import tempfile
import unittest
from xml.etree import ElementTree

# Grab our test's path and append the cdL_convert root directory

# There has to be a better method than:
# 1) Getting our current directory
# 2) Splitting into list
# 3) Splicing out the last 3 entries (filepath, test dir, tools dir)
# 4) Joining
# 5) Appending to our Python path.

sys.path.append('/'.join(os.path.realpath(__file__).split('/')[:-2]))

import cdl_convert.cdl_convert as cdl_convert

#==============================================================================
# GLOBALS
#==============================================================================

# parse_cdl ===================================================================

CDL_FULL = """<?xml version="1.0" encoding="UTF-8"?>
<ColorDecisionList xmlns="urn:ASC:CDL:v1.01">
    <Description>CDL description 1</Description>
    <InputDescription>CDL Input Desc Text</InputDescription>
    <Description>CDL description 2</Description>
    <ColorDecision>
        <Description>CD description 1</Description>
        <InputDescription>CD Input Desc Text</InputDescription>
        <Description>CD description 2</Description>
        <MediaRef ref="/best/path/ever.dpx"/>
        <Description>CD description 3</Description>
        <ColorCorrection id="014_xf_seqGrade_v01">
            <Description>CC description 1</Description>
            <InputDescription>Input Desc Text</InputDescription>
            <Description>CC description 2</Description>
            <SOPNode>
                <Description>Sop description 1</Description>
                <Description>Sop description 2</Description>
                <Slope>1.014 1.0104 0.62</Slope>
                <Offset>-0.00315 -0.00124 0.3103</Offset>
                <Power>1.0 0.9983 1.0</Power>
                <Description>Sop description 3</Description>
            </SOPNode>
            <Description>CC description 3</Description>
            <SATNode>
                <Description>Sat description 1</Description>
                <Saturation>1.09</Saturation>
                <Description>Sat description 2</Description>
            </SATNode>
            <Description>CC description 4</Description>
            <ViewingDescription>Viewing Desc Text</ViewingDescription>
            <Description>CC description 5</Description>
        </ColorCorrection>
        <ViewingDescription>CD WOOD VIEWER!? ////</ViewingDescription>
    </ColorDecision>
    <ColorDecision>
        <ColorCorrection id="f51.200">
            <SopNode>
                <Slope>0.2331 0.678669 1.0758</Slope>
                <Offset>0.031 0.128 -0.096</Offset>
                <Power>1.8 0.97 0.961</Power>
            </SopNode>
            <SatNode>
                <Saturation>1.01</Saturation>
            </SatNode>
        </ColorCorrection>
    </ColorDecision>
    <ColorDecision>
        <MediaRef ref="relative/path/13.jpg"/>
        <ColorCorrectionRef ref="f51.200"/>
    </ColorDecision>
    <ColorDecision>
        <ColorCorrection id="f55.100">
            <Description>Raised saturation a little!?! ag... \/Offset</Description>
            <Description>Raised saturation a little!?! ag... \/Offset</Description>
            <InputDescription>METAL VIEWER!!! \/\/</InputDescription>
            <ViewingDescription>WOOD VIEWER!? ////</ViewingDescription>
            <SopNode>
                <Description>Raised saturation a little!?! ag... \/Offset</Description>
                <Slope>137829.329 4327890.9833 3489031.003</Slope>
                <Offset>-3424.011 -342789423.013 -4238923.11</Offset>
                <Power>3271893.993 .0000998 0.0000000000000000113</Power>
            </SopNode>
            <SatNode>
                <Saturation>1798787.01</Saturation>
            </SatNode>
        </ColorCorrection>
    </ColorDecision>
    <ColorDecision>
        <ViewingDescription></ViewingDescription>
        <Description></Description>
        <Description>CD description 1</Description>
        <ColorCorrection id="f54.112">
            <ASC_SAT>
                <Saturation>1.01</Saturation>
            </ASC_SAT>
            <ASC_SOP>
                <Slope>0.2331 0.678669 1.0758</Slope>
                <Offset>0.031 0.128 -0.096</Offset>
                <Power>1.8 0.97 0.961</Power>
            </ASC_SOP>
        </ColorCorrection>
        <Description>CD description 2</Description>
        <InputDescription>CD Input Desc Text 2</InputDescription>
    </ColorDecision>
    <Description>CDL description 3</Description>
    <ViewingDescription>CDL Viewing Desc Text</ViewingDescription>
    <Description>CDL description 4</Description>
    <ColorDecision>
        <ViewingDescription></ViewingDescription>
        <ColorCorrection id="burp_100.x12">
            <ViewingDescription></ViewingDescription>
            <Description></Description>
            <SOPNode>
                <Description></Description>
                <Slope>1.014 1.0104 0.62</Slope>
                <Offset>-0.00315 -0.00124 0.3103</Offset>
                <Power>1.0 0.9983 1.0</Power>
            </SOPNode>
            <Description></Description>
            <InputDescription></InputDescription>
            <SatNode>
                <Saturation>1.09</Saturation>
                <Description></Description>
            </SatNode>
            <Description></Description>
        </ColorCorrection>
    </ColorDecision>
    <ColorDecision>
        <ViewingDescription>12345</ViewingDescription>
        <ColorCorrectionRef ref="f54.112"/>
    </ColorDecision>
    <Description>CDL description 5</Description>
</ColorDecisionList>
"""

CCC_ODD = """<?xml version="1.0" encoding="UTF-8"?>
<ColorCorrectionCollection>
    <Description></Description>
    <InputDescription></InputDescription>
    <Description>CCC description 1</Description>
    <Description></Description>
    <Description></Description>
    <Description></Description>
    <ColorCorrection id="014_xf_seqGrade_v01">
        <SOPNode>
            <Description>Sop description 1</Description>
            <Description>Sop description 2</Description>
            <Slope>1.014 1.0104 0.62</Slope>
            <Offset>-0.00315 -0.00124 0.3103</Offset>
            <Power>1.0 0.9983 1.0</Power>
            <Description>Sop description 3</Description>
        </SOPNode>
    </ColorCorrection>
    <ColorCorrection id="f51.200">
        <SopNode>
            <Slope>0.2331 0.678669 1.0758</Slope>
            <Offset>0.031 0.128 -0.096</Offset>
            <Power>1.8 0.97 0.961</Power>
        </SopNode>
    </ColorCorrection>
    <Description>Raised1 saturation a little!?! ag... \/Offset</Description>
    <Description>Raised2 saturation a little!?! ag... \/Offset</Description>
    <ColorCorrection id="f55.100">
        <SatNode>
            <Saturation>1798787.01</Saturation>
        </SatNode>
    </ColorCorrection>
    <ColorCorrection id="f54.112">
        <ASC_SAT>
            <Saturation>1.01</Saturation>
        </ASC_SAT>
    </ColorCorrection>
    <ViewingDescription></ViewingDescription>
    <ColorCorrection id="burp_200.x15">
        <SatNode>
            <Description>I am a lovely sat node</Description>
            <Saturation>1.01</Saturation>
        </SatNode>
    </ColorCorrection>
</ColorCorrectionCollection>
"""

# write_cdl ===================================================================

CDL_FULL_WRITE = """<?xml version="1.0" encoding="UTF-8"?>
<ColorDecisionList xmlns="urn:ASC:CDL:v1.01">
    <InputDescription>CDL Input Desc Text</InputDescription>
    <ViewingDescription>CDL Viewing Desc Text</ViewingDescription>
    <Description>CDL description 1</Description>
    <Description>CDL description 2</Description>
    <Description>CDL description 3</Description>
    <Description>CDL description 4</Description>
    <Description>CDL description 5</Description>
    <ColorDecision>
        <InputDescription>CD Input Desc Text</InputDescription>
        <ViewingDescription>CD WOOD VIEWER!? ////</ViewingDescription>
        <Description>CD description 1</Description>
        <Description>CD description 2</Description>
        <Description>CD description 3</Description>
        <MediaRef ref="/best/path/ever.dpx"/>
        <ColorCorrection id="014_xf_seqGrade_v01">
            <InputDescription>Input Desc Text</InputDescription>
            <ViewingDescription>Viewing Desc Text</ViewingDescription>
            <Description>CC description 1</Description>
            <Description>CC description 2</Description>
            <Description>CC description 3</Description>
            <Description>CC description 4</Description>
            <Description>CC description 5</Description>
            <SOPNode>
                <Description>Sop description 1</Description>
                <Description>Sop description 2</Description>
                <Description>Sop description 3</Description>
                <Slope>1.014 1.0104 0.62</Slope>
                <Offset>-0.00315 -0.00124 0.3103</Offset>
                <Power>1.0 0.9983 1.0</Power>
            </SOPNode>
            <SATNode>
                <Description>Sat description 1</Description>
                <Description>Sat description 2</Description>
                <Saturation>1.09</Saturation>
            </SATNode>
        </ColorCorrection>
    </ColorDecision>
    <ColorDecision>
        <ColorCorrection id="f51.200">
            <SOPNode>
                <Slope>0.2331 0.678669 1.0758</Slope>
                <Offset>0.031 0.128 -0.096</Offset>
                <Power>1.8 0.97 0.961</Power>
            </SOPNode>
            <SATNode>
                <Saturation>1.01</Saturation>
            </SATNode>
        </ColorCorrection>
    </ColorDecision>
    <ColorDecision>
        <MediaRef ref="relative/path/13.jpg"/>
        <ColorCorrectionRef ref="f51.200"/>
    </ColorDecision>
    <ColorDecision>
        <ColorCorrection id="f55.100">
            <InputDescription>METAL VIEWER!!! \/\/</InputDescription>
            <ViewingDescription>WOOD VIEWER!? ////</ViewingDescription>
            <Description>Raised saturation a little!?! ag... \/Offset</Description>
            <Description>Raised saturation a little!?! ag... \/Offset</Description>
            <SOPNode>
                <Description>Raised saturation a little!?! ag... \/Offset</Description>
                <Slope>137829.329 4327890.9833 3489031.003</Slope>
                <Offset>-3424.011 -342789423.013 -4238923.11</Offset>
                <Power>3271893.993 0.0000998 0.0000000000000000113</Power>
            </SOPNode>
            <SATNode>
                <Saturation>1798787.01</Saturation>
            </SATNode>
        </ColorCorrection>
    </ColorDecision>
    <ColorDecision>
        <InputDescription>CD Input Desc Text 2</InputDescription>
        <Description>CD description 1</Description>
        <Description>CD description 2</Description>
        <ColorCorrection id="f54.112">
            <SOPNode>
                <Slope>0.2331 0.678669 1.0758</Slope>
                <Offset>0.031 0.128 -0.096</Offset>
                <Power>1.8 0.97 0.961</Power>
            </SOPNode>
            <SATNode>
                <Saturation>1.01</Saturation>
            </SATNode>
        </ColorCorrection>
    </ColorDecision>
    <ColorDecision>
        <ColorCorrection id="burp_100.x12">
            <SOPNode>
                <Slope>1.014 1.0104 0.62</Slope>
                <Offset>-0.00315 -0.00124 0.3103</Offset>
                <Power>1.0 0.9983 1.0</Power>
            </SOPNode>
            <SATNode>
                <Saturation>1.09</Saturation>
            </SATNode>
        </ColorCorrection>
    </ColorDecision>
    <ColorDecision>
        <ViewingDescription>12345</ViewingDescription>
        <ColorCorrectionRef ref="f54.112"/>
    </ColorDecision>
</ColorDecisionList>
"""

CCC_ODD_WRITE = """<?xml version="1.0" encoding="UTF-8"?>
<ColorCorrectionCollection xmlns="urn:ASC:CDL:v1.01">
    <Description>CCC description 1</Description>
    <Description>Raised1 saturation a little!?! ag... \/Offset</Description>
    <Description>Raised2 saturation a little!?! ag... \/Offset</Description>
    <ColorCorrection id="014_xf_seqGrade_v01">
        <SOPNode>
            <Description>Sop description 1</Description>
            <Description>Sop description 2</Description>
            <Description>Sop description 3</Description>
            <Slope>1.014 1.0104 0.62</Slope>
            <Offset>-0.00315 -0.00124 0.3103</Offset>
            <Power>1.0 0.9983 1.0</Power>
        </SOPNode>
    </ColorCorrection>
    <ColorCorrection id="f51.200">
        <SOPNode>
            <Slope>0.2331 0.678669 1.0758</Slope>
            <Offset>0.031 0.128 -0.096</Offset>
            <Power>1.8 0.97 0.961</Power>
        </SOPNode>
    </ColorCorrection>
    <ColorCorrection id="f55.100">
        <SATNode>
            <Saturation>1798787.01</Saturation>
        </SATNode>
    </ColorCorrection>
    <ColorCorrection id="f54.112">
        <SATNode>
            <Saturation>1.01</Saturation>
        </SATNode>
    </ColorCorrection>
    <ColorCorrection id="burp_200.x15">
        <SATNode>
            <Description>I am a lovely sat node</Description>
            <Saturation>1.01</Saturation>
        </SATNode>
    </ColorCorrection>
</ColorCorrectionCollection>
"""

CCC_BAD_TAG = """<?xml version="1.0" encoding="UTF-8"?>
<ColorCorrectionBollection xmlns="urn:ASC:CDL:v1.01">
    <Description>CCC description 1</Description>
    <Description>Raised1 saturation a little!?! ag... \/Offset</Description>
    <Description>Raised2 saturation a little!?! ag... \/Offset</Description>
    <ColorCorrection id="014_xf_seqGrade_v01">
        <SOPNode>
            <Description>Sop description 1</Description>
            <Description>Sop description 2</Description>
            <Description>Sop description 3</Description>
            <Slope>1.014 1.0104 0.62</Slope>
            <Offset>-0.00315 -0.00124 0.3103</Offset>
            <Power>1.0 0.9983 1.0</Power>
        </SOPNode>
    </ColorCorrection>
    <ColorCorrection id="f51.200">
        <SOPNode>
            <Slope>0.2331 0.678669 1.0758</Slope>
            <Offset>0.031 0.128 -0.096</Offset>
            <Power>1.8 0.97 0.961</Power>
        </SOPNode>
    </ColorCorrection>
    <ColorCorrection id="f55.100">
        <SATNode>
            <Saturation>1798787.01</Saturation>
        </SATNode>
    </ColorCorrection>
    <ColorCorrection id="f54.112">
        <SATNode>
            <Saturation>1.01</Saturation>
        </SATNode>
    </ColorCorrection>
    <ColorCorrection id="burp_200.x15">
        <SATNode>
            <Description>I am a lovely sat node</Description>
            <Saturation>1.01</Saturation>
        </SATNode>
    </ColorCorrection>
</ColorCorrectionBollection>
"""

# misc ========================================================================

UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER = 'abcdefghijklmnopqrstuvwxyz'

if sys.version_info[0] >= 3:
    enc = lambda x: bytes(x, 'UTF-8')
else:
    enc = lambda x: x

if sys.version_info[0] >= 3:
    builtins = 'builtins'
else:
    builtins = '__builtin__'

#==============================================================================
# TEST CLASSES
#==============================================================================


class TestParseCDLFull(unittest.TestCase):
    """Tests a full CDL parse"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.desc = [
            'CDL description 1',
            'CDL description 2',
            'CDL description 3',
            'CDL description 4',
            'CDL description 5'
        ]
        self.input_desc = 'CDL Input Desc Text'
        self.viewing_desc = 'CDL Viewing Desc Text'
        self.color_correction_ids = [
            '014_xf_seqGrade_v01',
            'f51.200',
            'f51.200',
            'f55.100',
            'f54.112',
            'burp_100.x12',
            'f54.112',
        ]
        self.media_ref_refs = [
            "/best/path/ever.dpx",
            None,
            "relative/path/13.jpg",
            None,
            None,
            None,
            None,
        ]
        self.color_decision_descs = [
            ['CD description 1', 'CD description 2', 'CD description 3'],
            [],
            [],
            [],
            ['CD description 1', 'CD description 2'],
            [],
            [],
        ]
        self.color_decision_input_descs = [
            'CD Input Desc Text',
            None,
            None,
            None,
            'CD Input Desc Text 2',
            None,
            None,
        ]
        self.color_decision_viewing_descs = [
            'CD WOOD VIEWER!? ////',
            None,
            None,
            None,
            None,
            None,
            '12345'
        ]
        self.color_decision_is_ref = [
            False,
            False,
            True,
            False,
            False,
            False,
            True,
        ]

        # Build our cdl
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(enc(CDL_FULL))
            self.filename = f.name

        self.node = cdl_convert.parse_cdl(self.filename)

    #==========================================================================

    def tearDown(self):
        # The system should clean these up automatically,
        # but we'll be neat.
        os.remove(self.filename)
        # We need to clear the ColorCorrection member dictionary so we don't
        # have to worry about non-unique ids.
        cdl_convert.reset_all()

    #==========================================================================
    # TESTS
    #==========================================================================

    def test_file_in(self):
        """Tests that the input_file has been set to the file in value"""
        self.assertEqual(
            self.filename,
            self.node.file_in
        )

    #==========================================================================

    def test_type(self):
        """Makes sure type is still set to ccc"""
        self.assertEqual(
            'cdl',
            self.node.type
        )

    #==========================================================================

    def test_descs(self):
        """Tests that the desc fields have been set correctly"""
        self.assertEqual(
            self.desc,
            self.node.desc
        )

    #==========================================================================

    def test_viewing_desc(self):
        """Tests that the viewing desc has been set correctly"""
        self.assertEqual(
            self.viewing_desc,
            self.node.viewing_desc
        )

    #==========================================================================

    def test_input_desc(self):
        """Tests that the input desc has been set correctly"""
        self.assertEqual(
            self.input_desc,
            self.node.input_desc
        )

    #==========================================================================

    def test_parse_cc_results(self):
        """Tests that the parser picked up all the cc's"""
        id_list = [i.cc.id for i in self.node.color_decisions]
        self.assertEqual(
            self.color_correction_ids,
            id_list
        )

    #==========================================================================

    def test_media_ref_refs(self):
        """Tests that all media ref refs were parsed correctly"""
        ref_list = [
            i.media_ref.ref if i.media_ref else None for i in self.node.color_decisions
        ]
        self.assertEqual(
            self.media_ref_refs,
            ref_list
        )

    #==========================================================================

    def test_color_decision_descs(self):
        """Tests that color decision descs are parsed correctly"""
        desc_list = [
            i.desc for i in self.node.color_decisions
        ]
        self.assertEqual(
            self.color_decision_descs,
            desc_list
        )

    #==========================================================================

    def test_color_decision_input_descs(self):
        """Tests that color decision input descs are parsed correctly"""
        desc_list = [
            i.input_desc for i in self.node.color_decisions
        ]
        self.assertEqual(
            self.color_decision_input_descs,
            desc_list
        )

    #==========================================================================

    def test_color_decision_viewing_descs(self):
        """Tests that color decision viewing descs are parsed correctly"""
        desc_list = [
            i.viewing_desc for i in self.node.color_decisions
        ]
        self.assertEqual(
            self.color_decision_viewing_descs,
            desc_list
        )

    #==========================================================================

    def test_color_decision_is_ref(self):
        """Tests that color decision references are parsed correctly"""
        ref_list = [
            i.is_ref for i in self.node.color_decisions
        ]
        self.assertEqual(
            self.color_decision_is_ref,
            ref_list
        )

'''
class TestParseCCCOdd(TestParseCCCFull):
    """Tests an odd CCC parse"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.desc = [
            'CCC description 1',
            'Raised1 saturation a little!?! ag... \/Offset',
            'Raised2 saturation a little!?! ag... \/Offset',
        ]
        self.input_desc = None
        self.viewing_desc = None
        self.color_correction_ids = [
            '014_xf_seqGrade_v01',
            'f51.200',
            'f55.100',
            'f54.112',
            'burp_200.x15',
        ]

        # Build our ccc
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(enc(CCC_ODD))
            self.filename = f.name

        self.node = cdl_convert.parse_ccc(self.filename)


class TestParseCCCExceptions(unittest.TestCase):
    """Tests that we run into the correct exceptions with bad XMLs"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.filename = None

    def tearDown(self):
        if self.filename:
            os.remove(self.filename)
        cdl_convert.reset_all()

    #==========================================================================
    # TESTS
    #==========================================================================

    def testBadTag(self):
        """Tests that a bad root tag raises a ValueError"""

        # Build our ccc
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(enc(CCC_BAD_TAG))
            self.filename = f.name

        self.assertRaises(
            ValueError,
            cdl_convert.parse_ccc,
            self.filename,
        )

    #==========================================================================

    def testEmptyCCC(self):
        """Tests that an empty CCC file raises a ValueError"""

        emptyCCC = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<ColorCorrectionCollection xmlns="urn:ASC:CDL:v1.01">\n'
                    '</ColorCorrectionCollection>')

        # Build our ccc
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(enc(emptyCCC))
            self.filename = f.name

        self.assertRaises(
            ValueError,
            cdl_convert.parse_ccc,
            self.filename,
        )
'''

class TestWriteCDLFull(unittest.TestCase):
    """Tests a full write of the CDL file

    This is an integration style test. If parse_cdl stops working, this stops
    working.

    """
    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        # Build our cdl
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(enc(CDL_FULL))
            self.filename = f.name

        self.cdl = cdl_convert.parse_cdl(self.filename)

        self.target_xml_root = enc(CDL_FULL_WRITE)
        self.target_xml = enc('\n'.join(CDL_FULL_WRITE.split('\n')[1:]))

    #==========================================================================

    def tearDown(self):
        os.remove(self.filename)
        cdl_convert.reset_all()

    #==========================================================================
    # TESTS
    #==========================================================================

    def test_root_xml(self):
        """Tests that root_xml returns the full XML as expected"""
        self.assertEqual(
            self.target_xml_root,
            self.cdl.xml_root
        )

    #==========================================================================

    def test_base_xml(self):
        """Tests that the xml atrib returns the XML minus root as expected"""
        self.assertEqual(
            self.target_xml,
            self.cdl.xml
        )

    #==========================================================================

    def test_element(self):
        """Tests that the element returned is an etree type"""
        self.assertEqual(
            'ColorDecisionList',
            self.cdl.element.tag
        )

    #==========================================================================

    def test_write(self):
        """Tests writing the cdl itself"""
        mockOpen = mock.mock_open()

        self.cdl._file_out = 'bobs_big_file.cdl'

        with mock.patch(builtins + '.open', mockOpen, create=True):
            cdl_convert.write_cdl(self.cdl)

        mockOpen.assert_called_once_with('bobs_big_file.cdl', 'wb')

        mockOpen().write.assert_called_once_with(self.target_xml_root)

'''
class TestWriteCCCOdd(TestWriteCCCFull):
    """Tests an odd write of the CCC file

    This is an integration style test. If parse_ccc stops working, this stops
    working.

    """
    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        cdl_convert.reset_all()

        # Build our ccc
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(enc(CCC_ODD))
            self.filename = f.name

        self.ccc = cdl_convert.parse_ccc(self.filename)

        self.target_xml_root = enc(CCC_ODD_WRITE)
        self.target_xml = enc('\n'.join(CCC_ODD_WRITE.split('\n')[1:]))
'''
#==============================================================================
# RUNNER
#==============================================================================
if __name__ == '__main__':
    unittest.main()
