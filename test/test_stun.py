
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

    def test_extract_msg_header(self):
        hdr = struct.pack(">HHLLQ", 11,13,0x2112A442, 17, 19)
        self.assertEqual((11, 13, (17 << 64) + 19), stun.extract_msg_header(hdr))


    def test_create_binding_request(self):
        hdr = stun.create_binding_request((23 << 64) + 29)
        self.assertEqual(20, len(hdr))
        self.assertEqual((1,0,0x2112A442, 23, 29), struct.unpack(">HHLLQ", hdr))

    def test_extract_tlv(self):
        msg = struct.pack(">HH", 12, 4) + b"STUFF"
        self.assertEqual((12,b"STUF",b"F"), stun.extract_tlv(msg))

    def test_process_tlv_addr_ip4(self):
        self.assertEqual(("128.10.12.1", 789),
                stun.process_tlv_addr(
                struct.pack(">xBHBBBB", 0x01, 789, 128, 10, 12, 1)))

    def test_process_tlv_addr_ip6(self):
        self.assertEqual(("1234:4567:789A:BCDE:F012:3456:789A:BCD7", 789),
                stun.process_tlv_addr(
                struct.pack(">xBHHHHHHHHH", 0x02, 789,
                0x1234, 0x4567, 0x789A, 0xBCDE, 0xF012, 0x3456, 0x789A, 0xBCD7)))

    def test_process_map_addr(self):
        self.assertEqual(("128.10.12.1", 789),
                stun.process_map_addr(
                struct.pack(">xBHBBBB", 0x01, 789, 128, 10, 12, 1)))

    def test_process_src_addr(self):
        self.assertEqual(("128.10.12.1", 789),
                stun.process_src_addr(
                struct.pack(">xBHBBBB", 0x01, 789, 128, 10, 12, 1)))

    def test_process_chg_addr(self):
        self.assertEqual(("128.10.12.1", 789),
                stun.process_chg_addr(
                struct.pack(">xBHBBBB", 0x01, 789, 128, 10, 12, 1)))

    def test_process_refl_addr(self):
        self.assertEqual(("128.10.12.1", 789),
                stun.process_chg_addr(
                struct.pack(">xBHBBBB", 0x01, 789, 128, 10, 12, 1)))

    def test_process_xor_map_addr(self):
        self.assertEqual(("128.10.12.1", 789),
                stun.process_xor_map_addr(
                struct.pack(">xBHBBBB", 0x01,
                789 ^ 0x2112, 128 ^ 0x21, 10 ^ 0x12, 12 ^ 0xA4, 1 ^ 0x42)))

    def test_process_software(self):
        stun.process_software(b"1.2.3")


    def test_process_binding_response1(self):
        msg = [\
            struct.pack(">HHxBHBBBB", 1, 8, 0x01, 789, 128, 10, 12, 1),
            struct.pack(">HHxBHBBBB", 2, 8, 0x01, 789, 128, 10, 12, 2),
            struct.pack(">HHxBHBBBB", 4, 8, 0x01, 789, 128, 10, 12, 4),
            struct.pack(">HHxBHBBBB", 5, 8, 0x01, 789, 128, 10, 12, 5),
            struct.pack(">HHxBHBBBB", 11, 8, 0x01, 789, 128, 10, 12, 11),
            struct.pack(">HH", 0x8022, 10) + b"MYSOFTWARE"]

        self.assertEqual("128.10.12.1", stun.process_binding_response(b"".join(msg)))


    def test_process_binding_response2(self):
        msg = [\
            struct.pack(">HHxBHBBBB", 2, 8, 0x01, 789, 128, 10, 12, 2),
            struct.pack(">HHxBHBBBB", 4, 8, 0x01, 789, 128, 10, 12, 4),
            struct.pack(">HHxBHBBBB", 5, 8, 0x01, 789, 128, 10, 12, 5),
            struct.pack(">HHxBHBBBB", 11, 8, 0x01, 789, 128, 10, 12, 11),
            struct.pack(">HHxBHBBBB", 0x20, 8, 0x01, 789, 128, 10, 12, 0x20),
            struct.pack(">HH", 0x8022, 10) + b"MYSOFTWARE"]
        self.assertEqual("161.24.168.98", stun.process_binding_response(b"".join(msg)))


    def test_process_binding_response3(self):
        msg = [\
            struct.pack(">HHxBHBBBB", 2, 8, 0x01, 789, 128, 10, 12, 2),
            struct.pack(">HHxBHBBBB", 4, 8, 0x01, 789, 128, 10, 12, 4),
            struct.pack(">HHxBHBBBB", 5, 8, 0x01, 789, 128, 10, 12, 5),
            struct.pack(">HHxBHBBBB", 11, 8, 0x01, 789, 128, 10, 12, 11),
            struct.pack(">HHxBHBBBB", 0x8020, 8, 0x01, 789, 128, 10, 12, 0x82),
            struct.pack(">HH", 0x8022, 10) + b"MYSOFTWARE"]
        self.assertEqual("161.24.168.192", stun.process_binding_response(b"".join(msg)))


    def test_process_response(self):
        msg = [\
            struct.pack(">HHLLQ", 0x101,12,0x2112A442, 17, 19),
            struct.pack(">HHxBHBBBB", 1, 8, 0x01, 789, 128, 10, 12, 2)]

        self.assertEqual("128.10.12.2", stun.process_response(b"".join(msg), (17 << 64) + 19))

def main():
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(StunTests))

    suiteAll = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run( suiteAll )


if __name__ == '__main__':
    main()

