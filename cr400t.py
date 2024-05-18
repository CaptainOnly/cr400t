import rflib

def to_bits(bit_string):
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

SWx_WIDTH = 3
SW1 = 0b110
SW2 = 0b110
SW3 = 0b110
SW4 = 0b110
SW5 = 0b010

SW1 = 0b010
SW2 = 0b110
SW3 = 0b010
SW4 = 0b110
SW5 = 0b010

XX1_WIDTH = 3
XX1 = 0b010

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

command = PREAMBLE
command = (command << SWx_WIDTH) + SW1
command = (command << SWx_WIDTH) + SW2
command = (command << SWx_WIDTH) + SW3
command = (command << SWx_WIDTH) + SW4
command = (command << SWx_WIDTH) + SW5
command = (command << XX1_WIDTH) + XX1
command = (command << CMD_WIDTH) + CMD_ON
command = (command << 1)

command = command.to_bytes(8, 'big') 

d = rflib.RfCat()
d.setFreq(303875000)
d.setMdmDRate(2940)
d.setMdmModulation(rflib.MOD_ASK_OOK)
for _ in range(6):
    d.RFxmit(command)
d.setModeIDLE()
d.cleanup()
