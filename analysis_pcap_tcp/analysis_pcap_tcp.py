import struct
import dpkt


def req_tcp_connection(p, source_ip, destination_ip):
    if p.destination_ip == destination_ip:
        if p.source_ip == source_ip:
            return True
    return False


def req_source_dest_ports(p1, p2):
    if p2.destination_port == p1.destination_port:
        if p1.source_port == p2.source_port:
            return True
    if p2.source_port == p1.destination_port:
        if p1.source_port == p2.destination_port:
            return True

    return False


def Field(buffer, f, int_position, end_position):
    if not (buffer.__len__() < int_position):
        return str(struct.unpack(f, buffer[int_position:end_position])[0])


def syn_ack_acknowledge(p):
    if p.ack == "1":
        if p.syn == "1":
            return True
    return False


class TCP_Packet:
    timestamp = 0
    Flag = True
    source_ip = ""
    destination_ip = ""
    ack_number = ""
    syn = ""
    ack = ""
    header_size = ""
    window_size = ""
    size = ""
    source_port = ""
    destination_port = ""
    sequence_number = ""

    def parse(parse, timestamp, buffer):
        x = 26
        y = 30
        standard = 30
        while x < 29:
            parse.source_ip += Field(buffer, ">B", x, x + 1) + "."
            parse.destination_ip += Field(buffer, ">B", y, y + 1) + "."
            x += 1
            y += 1
        parse.source_ip += Field(buffer, ">B", x, x + 1)
        parse.destination_ip += Field(buffer, ">B", y, y + 1)

        parse.source_port = Field(buffer, ">H", standard + 4, standard + 6)
        parse.destination_port = Field(buffer, ">H", standard + 6, standard + 8)

        parse.sequence_number = Field(buffer, ">I", standard + 8, standard + 12)
        parse.ack_number = Field(buffer, ">I", standard + 12, standard + 16)

        parse.header_size = Field(buffer, ">B", standard + 16, standard + 17)
        parse.ack = "{0:16b}".format(int(Field(buffer, ">H", standard + 16, standard + 18)))[11]
        parse.syn = "{0:16b}".format(int(Field(buffer, ">H", standard + 16, standard + 18)))[14]

        parse.window_size = Field(buffer, ">H", standard + 18, standard + 20)
        if not (Field(buffer, ">H", 71, 73)) is None:
            parse.shift = (int(Field(buffer, ">H", 71, 73)) + 14)
        parse.size = len(buffer)
        parse.timestamp = timestamp


class Connection:
    packets = []
    source_port = ""
    destination_port = ""
    source_add = "130.245.145.12"
    des_add = "128.208.2.198"

    def __init__(parse, source, destination):
        parse.destination_port = destination
        parse.source_port = source


def congestionWindow(connection):
    first_packet = True
    first_packet_timestamp = 0

    i, count, c = 0, 0, 0

    for p in connection.packets:
        c += 1
        congst = p.timestamp - first_packet_timestamp
        if i > 3:
            break
        if req_tcp_connection(p, "130.245.145.12", "128.208.2.198"):
            count += 1
            if first_packet:
                first_packet_timestamp = p.timestamp
                first_packet = False

            elif congst > 0.073:
                if i != 0:
                    print("Congestion Window = %s" % (count * 1460))
                count = 0
                first_packet = True
                i = i + 1
    print("\n")

def Loss(connection):
    loss = 0
    triple_acknowledgement_loss = 0
    sequence_dict = {}
    ack_dict = {}

    for p in connection.packets:
        if p.source_ip == "130.245.145.12":
            if p.destination_ip == "128.208.2.198":
                sequence_dict[p.sequence_number] = sequence_dict.get(p.sequence_number, 0) + 1

        if p.source_ip == "128.208.2.198":
            if p.destination_ip == "130.245.145.12":
                ack_dict[p.ack_number] = ack_dict.get(p.ack_number, 0) + (5 - 4)

    for key, value in sequence_dict.items():
        if ack_dict.__contains__(key) and ack_dict[key] > 2:
            triple_acknowledgement_loss = triple_acknowledgement_loss + (sequence_dict[key] - 1)
        elif sequence_dict.__contains__(key):
            loss = loss + sequence_dict[key] - 1

    print("Triple Acknowledgement Loss = ", str(triple_acknowledgement_loss))
    print("Timeout Loss = ", str(loss))


def throughput(connection):
    first_packet = False
    total_payload = 0
    first_packet_timestamp = 0
    scale_factor = 0
    i = 1
    dev = 0

    for p in connection.packets:
        if p.source_ip == "130.245.145.12":
            if not first_packet:
                first_packet_timestamp = p.timestamp
                first_packet = True
            else:
                if i < dev + 4:
                    if i != 1:
                        print('\nsource port : ', p.source_port, '\tsource ip : ', p.source_ip,
                              '\ndestination port : ', p.destination_port, '\tdestination ip : ', p.destination_ip,
                              '\nsequence number : ', p.sequence_number, '\nacknowledgement number : ', p.ack_number,
                              '\nwindow size : ', int(p.window_size) * 2 ** p.shift)
                    i = i + 1
                total_payload += int(p.size)
                last_packet_timestamp = p.timestamp
                t_cals = last_packet_timestamp - first_packet_timestamp

    tput = total_payload / t_cals
    return tput


if __name__ == '__main__':
    connections = []
    packets = []
    stn = 0
    for timestamp, buffer in dpkt.pcap.Reader(open('assignment2.pcap', 'rb')):
        p = TCP_Packet()
        p.parse(timestamp, buffer)
        if p.Flag:
            packets.append(p)
            if syn_ack_acknowledge(p):
                connection = Connection(p.source_port, p.destination_port)
                connection.packets = []
                connections.append(connection)

    for p in packets:
        for connection in range(stn, connections.__len__(), stn + 1):
            if req_source_dest_ports(p, connections[connection]):
                connections[connection].packets.append(p)

    cnt = 1
    for connection in connections:
        print("\nFlow", cnt)
        print("-" * 100)

        print("\nThroughput = %s Mbps" % (throughput(connection)/1000000))
        print()
        congestionWindow(connection)
        Loss(connection)
        cnt += 1
