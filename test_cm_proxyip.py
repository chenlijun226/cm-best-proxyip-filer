import unittest

import cm反代ip高优筛选订阅 as generator


class BestFilterOrderTests(unittest.TestCase):
    def test_groups_lines_by_as_suffix_in_first_seen_order(self):
        lines = [
            "1.1.1.1:443#US-Provider-AS906",
            "2.2.2.2:443#US-Provider-AS40065",
            "3.3.3.3:443#US-Provider-AS906",
            "4.4.4.4:443#US-Provider-AS25820",
        ]

        ordered = generator.sort_best_filter_lines(lines)

        self.assertEqual(
            ordered,
            [
                "1.1.1.1:443#US-Provider-AS906",
                "3.3.3.3:443#US-Provider-AS906",
                "2.2.2.2:443#US-Provider-AS40065",
                "4.4.4.4:443#US-Provider-AS25820",
            ],
        )


if __name__ == "__main__":
    unittest.main()
