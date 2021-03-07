import pytest
import numpy as np
from lib import parser

class TestLineParsersUnit:
    """
    Pytest requires names of class to start with 'Test...'
    """
    def test_parse_keyword_DATE_line(self):
        input = "01 JUN 2018 /"
        output = "01 JUN 2018"
        assert parser.parse_keyword_DATE_line(input) == output

    def test_parse_keyword_COMPDAT_line(self):
        input = "'W1' 10 10 1 3 OPEN 1* 1 2 1 3* 1.0 /"
        output = ['W1', np.nan, '10', '10', '1', '3', 'OPEN', 'DEFAULT', '1',
                  '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '1.0']
        assert parser.parse_keyword_COMPDAT_line(input) == output

    def test_parse_keyword_COMPDATL_line(self):
        input = "'W3' 'LGR1' 10 10  2   2 	OPEN 	1* 	1	2 	1 	3* 			1.0918 /"
        output = ['W3', 'LGR1', '10', '10', '2', '2', 'OPEN', 'DEFAULT', '1',
                  '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '1.0918']
        assert parser.parse_keyword_COMPDATL_line(input) == output

    def test_default_params_unpacking_in_line(self):
        input = "'W1' 10 10 1 3 OPEN 1* 1 2 1 3* 1.0 /"
        output = "'W1' 10 10 1 3 OPEN DEFAULT 1 2 1 DEFAULT DEFAULT DEFAULT 1.0 /"
        assert parser.default_params_unpacking_in_line(input) == output

class TestUnitParser:
    @pytest.fixture
    def set_up(self):
        """
        Prepares info for reference input file(s)
        @return: None
        """
        self.keywords = ("DATES", "COMPDAT", "COMPDATL", "END")

        self.clean_file = "../input data/test_schedule.inc"

        self.parse_list_output_reference = [
        [np.nan, 'W1', np.nan, '10', '10', '1', '3', 'OPEN', 'DEFAULT', '1', '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '1.0'],
        [np.nan, 'W2', np.nan, '32', '10', '1', '3', 'OPEN', 'DEFAULT', '1', '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '2.0'],
        [np.nan, 'W3', np.nan, '5', '36', '2', '2', 'OPEN', 'DEFAULT', '1', '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '3.0'],
        [np.nan, 'W4', np.nan, '40', '30', '1', '3', 'OPEN', 'DEFAULT', '1', '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '4.0'],
        [np.nan, 'W5', np.nan, '21', '21', '4', '4', 'OPEN', 'DEFAULT', '1', '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '5.0'],
        ['01 JUN 2018', np.nan],
        ['01 JUL 2018', 'W3', np.nan, '32', '10', '1', '1', 'OPEN', 'DEFAULT', '1', '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '1.0718'],
        ['01 JUL 2018', 'W5', np.nan, '21', '21', '1', '3', 'OPEN', 'DEFAULT', '1', '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '5.0'],
        ['01 AUG 2018', np.nan],
        ['01 SEP 2018', 'W1', np.nan, '10', '10', '2', '3', 'OPEN', 'DEFAULT', '1', '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '1.0918'],
        ['01 SEP 2018', 'W2', np.nan, '32', '10', '1', '2', 'OPEN', 'DEFAULT', '1', '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '2.0'],
        ['01 SEP 2018', 'W3', 'LGR1', '10', '10', '2', '2', 'OPEN', 'DEFAULT', '1', '2', '1', 'DEFAULT', 'DEFAULT', 'DEFAULT', '1.0918'],
        ['01 OCT 2018', np.nan],
        ['01 NOV 2018', np.nan],
        ['01 DEC 2018', np.nan]]

    def test_parse_schedule(self, set_up):
        assert parser.parse_schedule(parser.read_schedule(self.clean_file), keywords=self.keywords) \
               == self.parse_list_output_reference
