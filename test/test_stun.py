
import unittest
import struct

from track_my_ip import stun


class StunTests(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_transaction_id(self):
        collection = []
        for i in range(30):
            uuid = stun.create_transaction_id()
            self.assertIsInstance(uuid, int)
            self.assertNotIn(uuid, collection)
            collection.append(uuid)

    def test_create_msg_header(self):
        hdr = stun.create_msg_header(11, 13, (17 << 64) + 19)
        self.assertEqual(20, len(hdr))
        self.assertEqual((11,13,0x2112A442, 17, 19), struct.unpack(">HHLLQ", hdr))

    def test_create_binding_request(self):
        hdr = stun.create_binding_request((23 << 64) + 29)
        self.assertEqual(20, len(hdr))
        self.assertEqual((1,0,0x2112A442, 23, 29), struct.unpack(">HHLLQ", hdr))

    def test_extract_tlv(self):
        msg = struct.pack(">HH", 12, 4) + b"STUFF"
        self.assertEqual((12,b"STUF",b"F"), stun.extract_tlv(msg))


def main():
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(StunTests))

    suiteAll = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run( suiteAll )


if __name__ == '__main__':
    main()

