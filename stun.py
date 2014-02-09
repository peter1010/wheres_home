import struct
import socket
import os
import functools

stun_servers_list = (
    ('stun.ekiga.net', 3478),
    ('stunserver.org', 3478),
    ('stun.ideasip.com', 3478),
    ('stun.softjoys.com', 3478),
    ('stun.voipbuster.com', 3478)
)


TLV_MAP_ADDR = 1
TLV_RESP_ADDR = 2
TLV_CHG_REQ = 3
TLV_SRC_ADDR = 4
TLV_CHG_ADDR = 5
TLV_USER = 6
TLV_PASS = 7
TLV_MSG_INT = 8
TLV_ERR_CODE = 9
TLV_UNKNOWN = 10
TLV_REFLECT = 11


def create_transaction_id():
    """Generate a 128 bit (16 byte) random number"""
    return functools.reduce(lambda x,y: (x << 8) + y, os.urandom(16))


def create_msg_header(msg_type, msg_length, tran_id):
    """STUN header is 20 bytes, 2 bytes msg_type, 2 bytes msg length, 16 bytes
    Transaction ID"""
    return struct.pack(">HHQQ", msg_type, msg_length, tran_id >> 64, 
            tran_id & 0xFFFFFFFFFFFFFFFF)


def create_binding_request(tran_id):
    """Create a binding request, message type is 1 (see RFC3489)"""
    return create_msg_header(1, 0, tran_id)

def extract_tlv(msg):
    name, val_len = struct.unpack(">HH", msg[:4])
    if name != 0:
        value = msg[4:4+val_len]
        return name, value, msg[4+val_len:]
    raise RuntimeError

def process_map_addr(value):
    family, port, a1, a2, a3, a4 = struct.unpack(">xBHBBBB", value)
    addr = ".".join([str(x) for x in (a1,a2,a3,a4)])
    return (addr, port)


def process_binding_response(body):
    """Body should have MAPPED-ADDRESS, SOURCE-ADDRESS, CHANGED-ADDRESS.
    Optional MESSAGE-INTEGRITY, conditionally REFLECTED-FROM"""
    while len(body) > 0:
        name, value, body = extract_tlv(body)
        if name == TLV_MAP_ADDR:
            mapped = process_map_addr(value)
            print("TLV_MAP_ADDR", mapped)
        elif name == TLV_SRC_ADDR:
            src = process_map_addr(value)
            print("TLV_SRC_ADDR", src)
        elif name == TLV_CHG_ADDR:
            chg = process_map_addr(value)
            print("TLV_CHG_ADDR", chg)
        elif name == TLV_MSG_INT:
            print("TLV_MSG_INT")
            pass
        elif name == TLV_REFLECT:
            refl = process_map_addr(value)
            print("TLV_REFLECT", refl)
        else:
            return None

def process_response(buf, req_tran_id):
    hdr = buf[:20]
    msg_type, msg_len, part1, part2 = struct.unpack(">HHQQ", hdr)
    resp_tran_id = part1 << 64 | part2
    if resp_tran_id != req_tran_id:
        print("Mis-match between Request and Response Transaction ID")
        return None
    if msg_type == 0x101:   # Binding Response
        return process_binding_response(buf[20:])
    elif msg_type == 0x111: # Binding Error Response
        pass
    elif msg_type == 0x102: # Shared Secret Response
        pass
    elif msg_type == 0x112: # Shared Secret Error Response
        pass
    else:
        print("Invalid STUN response msg type (%i)", msg_type)
        return None

def do_stun_transaction():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 54320))

    stun_server = stun_servers_list[0]

    tran_id = create_transaction_id()
    print("tran_id=", tran_id)
    msg = create_binding_request(tran_id)
    try:
        s.sendto(msg, stun_server)
    except socket.gaierror:
        return False
    buf, addr = s.recvfrom(2048)
    process_response(buf, tran_id)
    s.close()

if __name__ == "__main__":
    do_stun_transaction()
