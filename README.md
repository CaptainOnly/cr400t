# Overview

This module is an [rfcat](https://github.com/atlas0fd00m/rfcat) based implementation of a cr400t remote (aka RC400) used with some models of Mika Aire ceiling fans.

It has been tested to with Mika Aire fan model F786 and a [Yard Stick One](https://greatscottgadgets.com/yardstickone) radio.

# How I did it

Devices that work with rfcat -- like the YardStickOne -- are radios; they return the demodulated signal not the IQ data that an SDR device would return. This means is you need to know or to guess the properties of the signal you are trying to replicate. Fortunately, with the information in the FCC registration you often know enough to guess the rest.

Look up the device on the [fcc database](https://www.fcc.gov/oet/ea/fccid). The cr400t has grantee 2AHC3 and product code CR400T. The information is also available at [fcc.io](https://fccid.io/2AHC3CR400T).  

Go to the details and open up any photos of the device to confirm you have the right one.

Go to the [test report](https://fcc.report/FCC-ID/2AHC3CR400T). For the cr400t the test report gives the operating frequency (303.875 MHz). Looking further down there are scope traces of an example signal which clearly has 13 symbols encoded as 3 bits each each (110 for a '1', 010 for a '0') using on-off-keying modulation. Note: That's clear because it's what similar devices use (see credits). One trace even gives a rough measurement of symbol timing which lets us estimate the baud rate (881us for 3 bits or roughly 3400). 

Now start verifying things.

From the rfcat interactive prompt (rfcat -r) set the expected frequency `d.setFreq(303875000)` and perform a simulated scan `d.specan()`. If you operate the remote you should see some energy around the center frequency. This confirms the frequency is correct.

Now set the expected modulation `d.setMdmModulation(MOD_ASK_OOK)`, disable sync mode `d.setMdmSyncMode(0)`, and set preamble quality to zero `d.setPktPQT(0)` so the radio is always demodulating. The `d.RFlisten()` operation will show mostly garbage but if a button is held on the remote a repeating signal may appear. The job now is to adjust radio parameters until the device's signal is appearing consistenty in the data. The backup plan here, if a signal never appears, is to get an SDR device and start going deeper.

The biggest unknown is the baud rate. I needed to iterate until I found the most reliable value: 2940. This was a ways off from my original estimate.

Now start decoding the signal. Turn the hex into bits, and groups the bits into threes. The bits '110' from the radio represent one symbol (say '1'), while the bits '001' represent another ('0'). If you see any other trios then you frequency, modulation, framing, or baud rate is wrong. Try something else! Decode the signal for various buttons until the scheme is clear.

To transmit a command go in reverse: encode your command as symbols, turn the symbols into trios of bits for the radio, assmble the bits into a byte sequence, call `d.RFxmit()`.

# Credits

I was inspired by the [labrfcat](https://github.com/idatum/labrfcat) project by [idatum](https://github.com/idatum) which supports a simiar (but different) remote. That repo and [this RTL-SDR](https://www.rtl-sdr.com/hak5-reverse-engineering-radio-protocols-with-sdr-and-the-yardstick-one/) post had most of what I needed to figure this out. Thanks to [Hak5](https://www.youtube.com/@hak5) and [Mike Ossmann](http://www.ossmann.com/mike/) for the videos. This [leonjza](https://leonjza.github.io/blog/2016/10/02/reverse-engineering-static-key-remotes-with-gnuradio-and-rfcat/) post was also helpful. 

