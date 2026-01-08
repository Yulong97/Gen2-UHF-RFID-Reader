from gnuradio import gr
from gnuradio import uhd
from gnuradio import blocks
from gnuradio import filter
from gnuradio import analog
from gnuradio import digital
import rfid
import sys

class minimal_block(gr.top_block):
    def __init__(self):
        print("Entering minimal_block __init__")
        gr.top_block.__init__(self, "Minimal Block")
        print("Exiting minimal_block __init__")

if __name__ == "__main__":
    print("Instantiating minimal_block")
    tb = minimal_block()
    print("Done")
