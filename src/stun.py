import struct
import socket
import os
import functools
import logging
import select

from . import stun_list

TLV_MAP_ADDR = 1
TLV_RESP_ADDR = 2  # Obsolete in RFC5389
TLV_CHG_REQ = 3    # Obsolete in RFC5389
TLV_SRC_ADDR = 4   # Obsolete in RFC5389
TLV_CHG_ADDR = 5   # Obsolete in RFC5389
TLV_USER = 6
TLV_PASS = 7       # Obsolete in RFC5389
TLV_MSG_INT = 8
TLV_ERR_CODE = 9
TLV_UNKNOWN = 10
TLV_REFLECT = 11   # Obsoleted in RFC5389

# From RFC5389
TLV_REALM = 0x14
TLV_NONCE = 0x15
TLV_XOR_MAP_ADDR = 0x20


# From RFC3489bis-02
TLV_XOR_MAP_ADDR_bis = 0x8020
TLV_XOR_ONLY = 0x8021

# From RFC5389
TLV_SOFTWARE = 0x8022
TLV_ALT_SERVER = 0x8023
TLV_FINGERPRINT = 0x8028


def create_transaction_id():
    """Generate a 96 bit (12 byte) random number"""
    return functools.reduce(lambda x, y: (x << 8) + y, os.urandom(12))


def create_msg_header(msg_type, msg_length, tran_id):
    """STUN header is 20 bytes, 2 bytes msg_type, 2 bytes msg length, 16 bytes
    Transaction ID"""
    magic = 0x2112A442
    return struct.pack(">HHLLQ", msg_type, msg_length, magic, tran_id >> 64,
                       tran_id & 0xFFFFFFFFFFFFFFFF)


def extract_msg_header(hdr):
    msg_type, msg_len, magic, part1, part2 = struct.unpack(">HHLLQ", hdr)
    resp_tran_id = part1 << 64 | part2
    if magic != 0x2112A442:
        logging.error("Invalid STUN magic cookie")
    return msg_type, msg_len, resp_tran_id


def create_binding_request(tran_id):
    """Create a binding request, message type is 1 (see RFC5389)"""
    return create_msg_header(1, 0, tran_id)


def extract_tlv(msg):
    name, val_len = struct.unpack(">HH", msg[:4])
    if name != 0:
        value = msg[4:4+val_len]
        return name, value, msg[4+val_len:]
    raise RuntimeError("name is 0")


def process_tlv_addr(value):
    family, port = struct.unpack(">xBH", value[:4])
    if family == 0x01:   # IPv4
        addr = ".".join([str(x) for x in value[4:]])
    elif family == 0x02:  # IPv6
        addr = ":".join([("%04X" % x) for x in struct.unpack(">HHHHHHHH",
                        value[4:])])
    else:
        raise RuntimeError("family '%i' unknown" % family)
    return (addr, port)


def process_map_addr(value):
    """Process the MAPPED-ADDRESS attribute"""
    addr_port = process_tlv_addr(value)
    logging.debug("MAPPED-ADDRESS=%s" % str(addr_port))
    return addr_port


def process_src_addr(value):
    """Process the SOURCE-ADDRESS attribute"""
    addr_port = process_tlv_addr(value)
    logging.debug("SOURCE-ADDRESS=%s" % str(addr_port))
    return addr_port


def process_chg_addr(value):
    """Process the CHANGED-ADDRESS attribute"""
    addr_port = process_tlv_addr(value)
    logging.debug("CHANGED-ADDRESS=%s" % str(addr_port))
    return addr_port


def process_refl_addr(value):
    """Process the REFLECT-FROM attribute"""
    addr_port = process_tlv_addr(value)
    logging.debug("REFLECT-FROM=%s" % str(addr_port))
    return addr_port


def process_xor_map_addr(value):
    """Process the XOR-MAPPED-ADDRESS attribute"""
    family, port = struct.unpack(">xBH", value[:4])
    port = port ^ 0x2112
    if family == 0x01:   # IPv4
        addr = ".".join([str(x ^ m) for x, m in zip(value[4:],
                        (0x21, 0x12, 0xA4, 0x42))])
    elif family == 0x02:  # IPv6
        raise RuntimeError("IPv6 not supported yet")
    else:
        raise RuntimeError("family '%i' unknown" % family)
    logging.debug("XOR-MAPPED-ADDRESS=%s" % str((addr, port)))
    return (addr, port)


def process_software(value):
    """Process the SOFTWARE attribute"""
    logging.info("SOFWARE=%s" % value.decode('utf8'))


def process_binding_response(body):
    """Body should have MAPPED-ADDRESS, SOURCE-ADDRESS, CHANGED-ADDRESS.
    Optional MESSAGE-INTEGRITY, conditionally REFLECTED-FROM"""
    while len(body) > 0:
        name, value, body = extract_tlv(body)
        if name == TLV_MAP_ADDR:
            mapped = process_map_addr(value)
        elif name == TLV_SRC_ADDR:
            src = process_src_addr(value)
        elif name == TLV_CHG_ADDR:
            chg = process_chg_addr(value)
        elif name == TLV_MSG_INT:
            logging.debug("TLV_MSG_INT")
            pass
        elif name == TLV_REFLECT:
            refl = process_refl_addr(value)
        elif (name == TLV_XOR_MAP_ADDR) or (name == TLV_XOR_MAP_ADDR_bis):
            mapped = process_xor_map_addr(value)
        elif name == TLV_SOFTWARE:
            process_software(value)
        else:
            logging.warning("Unknown TLV = %i" % name)
    return mapped[0]


def process_response(buf, req_tran_id):
    hdr = buf[:20]
    msg_type, msg_len, resp_tran_id = extract_msg_header(hdr)
    body = buf[20:20+msg_len]

    if resp_tran_id != req_tran_id:
        print("Mis-match between Request and Response Transaction ID")
        return None
    if msg_type == 0x101:   # Binding Response
        return process_binding_response(body)
    elif msg_type == 0x111:  # Binding Error Response
        pass
    elif msg_type == 0x102:  # Shared Secret Response
        pass
    elif msg_type == 0x112:  # Shared Secret Error Response
        pass
    else:
        print("Invalid STUN response msg type (%04x)", msg_type)
        return None


def do_stun_transaction():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 54320))

    public_addr = None

    for server_tries in range(5):
        if public_addr:
            break
        stun_server = stun_list.pick_server()
        logging.info("Connecting to %s" % str(stun_server))
        tran_id = create_transaction_id()
        logging.debug("TID=%i" % tran_id)
        msg = create_binding_request(tran_id)
        timeout = 0.5
        for msg_tries in range(7):
            if public_addr:
                break
            try:
                s.sendto(msg, stun_server)
            except socket.gaierror:
                break

            rds, wrs, ers = select.select([s], [], [], timeout)
            if len(rds) > 0:
                buf, addr = s.recvfrom(2048)
                public_addr = process_response(buf, tran_id)
            else:
                timeout = 2*timeout
                logging.warning("Timed out waiting for response")
    s.close()
    return public_addr


if __name__ == "__main__":
    print(do_stun_transaction())
