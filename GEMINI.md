# Gen2 UHF RFID Reader

## Project Overview
This project is a Gen2 UHF RFID Reader implementation for GNU Radio (`gr-rfid`). It is designed to identify commercial Gen2 RFID Tags using FM0 line coding and a 40kHz data rate (BLF).

**Key Features:**
*   **Hardware Support:** USRPN200/N210 with RFX900 or SBX daughterboards.
*   **Protocol:** EPC Gen2 (ISO/IEC 18000-6C).
*   **Components:**
    *   **Gate:** Detects reader commands.
    *   **Tag Decoder:** Syncs and decodes tag responses (FM0).
    *   **Reader:** Generates reader commands (Query, ACK, etc.).

## Building and Installation

### Dependencies
*   GNU Radio (v3.7.4 tested)
*   UHD Driver
*   log4cpp

### Build Instructions
The project uses the standard CMake build system for GNU Radio modules.

```bash
cd gr-rfid
mkdir build
cd build
cmake ../  # Ensure logging is enabled if debugging is needed
make
sudo make install
sudo ldconfig
```

## Running the Reader

### Real-Time Execution
Execute the main Python script. High priority scheduling is recommended to meet timing constraints.

```bash
cd gr-rfid/apps/
sudo GR_SCHEDULER=STS nice -n -20 python ./reader.py
```
*   **Note:** If using an SBX daughterboard, uncomment `#self.source.set_auto_dc_offset(False)` in `reader.py`.

### Offline Mode
To run with pre-recorded traces without hardware:
1.  Edit `apps/reader.py` and set `DEBUG = True`.
2.  Run `python ./reader.py`.

## Configuration

### Runtime Configuration
Edit `apps/reader.py` to adjust:
*   **USRP Address:** `self.usrp_address_source` / `self.usrp_address_sink` (default: 192.168.10.2)
*   **Frequency:** `self.freq` (default: 910MHz)
*   **Tx Amplitude:** `self.ampl` (default: 0.1)
*   **Rx Gain:** `self.rx_gain` (default: 20)

### Protocol & Logic Configuration
Edit `include/rfid/global_vars.h` for core logic settings (requires recompilation):
*   **Max Queries:** `MAX_NUM_QUERIES` (Termination condition)
*   **Q Parameter:** `FIXED_Q` (Collision arbitration slots)
*   **Timing:** `T1_D`, `T2_D`, etc. (Protocol timings)

## Development Conventions

*   **Structure:** Follows standard GNU Radio OOT module layout.
    *   `include/rfid/`: C++ headers (API definitions).
    *   `lib/`: C++ implementation of blocks (`Gate`, `Tag Decoder`, `Reader`).
    *   `swig/`: Interface files for Python bindings.
    *   `grc/`: XML definitions for GNU Radio Companion.
    *   `apps/`: Python flowgraphs and scripts.
*   **Logging:** Uses `GR_LOG` macros. Ensure `log4cpp` is installed for detailed debug output.
*   **Debugging:** Use `blocks.file_sink` in `reader.py` to dump intermediate signals to `misc/data/` for analysis (e.g., using `misc/code/plot_signal.m`).
