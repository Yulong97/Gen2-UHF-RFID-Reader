#!/usr/bin/env python3
from gnuradio import gr
from gnuradio import uhd
from gnuradio import blocks
from gnuradio import qtgui
from gnuradio import filter
from gnuradio import fft
import rfid
from PyQt5 import QtWidgets, Qt
import sys
import sip

class usrp_test_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "USRP Test Block")

        # USRP Parameters
        self.usrp_addr = "addr=192.168.40.2"
        self.freq = 900e6
        self.rate = 1e6
        self.gain = 20
        self.antenna = "RX2"

        print(f"[-] Configuring USRP Source at {self.usrp_addr}...")
        print(f"    Freq: {self.freq/1e6} MHz, Rate: {self.rate/1e6} MS/s, Gain: {self.gain}, Ant: {self.antenna}")

        try:
            self.u_source = uhd.usrp_source(
                ",".join((self.usrp_addr, "")),
                uhd.stream_args(
                    cpu_format="fc32",
                    channels=range(1),
                ),
            )
            self.u_source.set_samp_rate(self.rate)
            self.u_source.set_center_freq(self.freq, 0)
            self.u_source.set_gain(self.gain, 0)
            self.u_source.set_antenna(self.antenna, 0)
            
            # Create a Qt GUI Frequency Sink
            self.qtgui_freq_sink = qtgui.freq_sink_c(
                1024, # fft_size
                fft.window.WIN_BLACKMAN_HARRIS, # window_type
                self.freq, # center_freq
                self.rate, # bandwidth
                "USRP Signal (Frequency)", # name
                1 # nconnections
            )
            
            # Create a Qt GUI Time Sink
            self.qtgui_time_sink = qtgui.time_sink_c(
                1024, # size
                self.rate, # samp_rate
                "USRP Signal (Time)", # name
                1 # nconnections
            )

            # Connect
            self.connect(self.u_source, self.qtgui_freq_sink)
            self.connect(self.u_source, self.qtgui_time_sink)
            print("[-] USRP Source Configured Successfully.")

        except Exception as e:
            print(f"[!] Error configuring USRP: {e}")
            sys.exit(1)

def main():
    qapp = QtWidgets.QApplication(sys.argv)
    
    tb = usrp_test_block()
    
    # Create a main window with a layout
    main_win = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    main_win.setLayout(layout)
    main_win.setWindowTitle("USRP Test - Signal Visualization")

    # Add Frequency Sink Widget
    freq_widget_ptr = tb.qtgui_freq_sink.qwidget()
    if freq_widget_ptr:
        freq_widget = sip.wrapinstance(freq_widget_ptr, QtWidgets.QWidget)
        layout.addWidget(freq_widget)
    
    # Add Time Sink Widget
    time_widget_ptr = tb.qtgui_time_sink.qwidget()
    if time_widget_ptr:
        time_widget = sip.wrapinstance(time_widget_ptr, QtWidgets.QWidget)
        layout.addWidget(time_widget)

    main_win.show()

    print("[-] Starting Flowgraph with GUI...")
    tb.start()
    
    # Run the Qt event loop
    qapp.exec_()
    
    tb.stop()
    tb.wait()

if __name__ == '__main__':
    main()