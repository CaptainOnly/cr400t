import argparse
import rflib
import sys

def to_bits(bit_string):
    if bit_string == '0':
        return 0b010;
    if bit_string == '1':
        return 0b110;
    bits = 0
    for c in bit_string:
        if c == '0':
            bits = (bits << 3) + 0b010;
        elif c == '1':
            bits = (bits << 3) + 0b110;
        else:
            raise ValueError()
    return bits

PREAMBLE = 0b010
SW_WIDTH = 15
DIM_WIDTH = 3
CMD_WIDTH = 18
CMD_REL  = to_bits('000000')
CMD_OFF  = to_bits('000001')
CMD_STOP = to_bits('000010')
CMD_REV  = to_bits('000100')
CMD_1    = to_bits('001000')
CMD_ON   = to_bits('001001')
CMD_2    = to_bits('001010')
CMD_3    = to_bits('010000')
CMD_4    = to_bits('011000')
CMD_6    = to_bits('100000')
CMD_5    = to_bits('100010')

def make_packet(switch, command, dim='0'):
    packet = PREAMBLE
    packet = (packet << SW_WIDTH) + to_bits(switch)
    packet = (packet << DIM_WIDTH) + to_bits(dim)
    packet = (packet << CMD_WIDTH) + command
    packet = packet.to_bytes(8, 'big') # gives three bytes spacing
    return packet

def tx_packet(packet, repeat=6):
    d = rflib.RfCat()
    d.setFreq(303875000)
    d.setMdmDRate(2940)
    d.setMdmModulation(rflib.MOD_ASK_OOK)
    for _ in range(repeat):
        d.RFxmit(packet)
    d.setModeIDLE()
    d.cleanup()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--switches", required=True, help="Position of switches 1-5 (On: '1', Off: '0')")
    p.add_argument("--command", required=True, help="on, off, rev, stop, 1, 2, 3, 4, 5, 6")
    p.add_argument("--dim", required=False, default='0', help="Position of dimmer switch (On/Dimmer: '1', Off/OnOff: '0'")
    args = p.parse_args()

    if len(args.switches) != 5:
        sys.stderr.write(f"--switches must be five long (got {args.switches}")
        sys.exit(-1)

    command = 0;
    if args.command == "on":
        command = CMD_ON
    elif args.command == "off":
        command = CMD_OFF
    elif args.command == "rev":
        command = CMD_REV
    elif args.command == "stop":
        command = CMD_STOP
    elif args.command == "1":
        command = CMD_1
    elif args.command == "2":
        command = CMD_2
    elif args.command == "3":
        command = CMD_3
    elif args.command == "4":
        command = CMD_4
    elif args.command == "5":
        command = CMD_5
    elif args.command == "6":
        command = CMD_6

    tx_packet(make_packet(args.switches, command))
