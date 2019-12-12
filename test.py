import math
import unittest
import typing

import uvarint

class TestUvarint(unittest.TestCase):

    # Example values from the multiformats specification README
    # https://github.com/multiformats/unsigned-varint/blob/master/README.md
    examples: typing.List[typing.Tuple[int, bytes]] = [
        (1,     bytes([0b0000_0001])),
        (127,   bytes([0b0111_1111])),
        (128,   bytes([0b1000_0000, 0b0000_0001])),
        (255,   bytes([0b1111_1111, 0b0000_0001])),
        (300,   bytes([0b1010_1100, 0b0000_0010])),
        (16384, bytes([0b1000_0000, 0b1000_0000, 0b0000_0001]))
    ]

    upper_bound: typing.Tuple[int, bytes] = (2 ** 63 - 1, bytes([0b1111_1111] * 8 + [0b0111_1111]))
    over_limit: typing.Tuple[int, bytes] = (2 ** 63, bytes([0b1000_0000] * 9 + [0b0000_0001]))

    values: typing.List[typing.Tuple[int, bytes]] = examples + [upper_bound]
    all: typing.List[typing.Tuple[int, bytes]] = values + [over_limit]

    def test_encoding(self) -> None:
        decoded: int
        encoded: bytes

        for (decoded, encoded) in TestUvarint.all:
            self.assertEqual(uvarint.encode(decoded), encoded)

    def test_decoding(self) -> None:
        decoded: int
        encoded: bytes

        for (decoded, encoded) in TestUvarint.values:
            self.assertEqual(uvarint.decode(encoded), decoded)

    def test_limits(self) -> None:
        self.assertEqual(len(TestUvarint.upper_bound[1]), 9)

        decoded, encoded = TestUvarint.over_limit
        self.assertEqual(len(encoded), 10)

        self.assertEqual(uvarint.decode(encoded, max=math.inf), decoded)

        with self.assertRaises(OverflowError):
            uvarint.decode(encoded)

if __name__ == '__main__':
    unittest.main()
