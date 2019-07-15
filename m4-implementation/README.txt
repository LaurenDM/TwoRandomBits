Required software

- arm-none-eabi-gcc (https://launchpad.net/gcc-arm-embedded)
  Probably available through your package manager.
  On some Linux distro's it might be required to install libnewlib-arm-none-eabi separately.
- libopencm3 library (should be bundled with the supporting material)
- stlink (https://github.com/texane/stlink)
- pyserial (https://github.com/pyserial/pyserial)
  Probably known as python-serial or python-pyserial in your package manager. Otherwise it can be installed through pip(3).

Required hardware

- An STM32F407 development board. If you have a different board, minor changes might be needed in the code.
- A USB to TTL UART connector with a PL2303 chip.
- Dupont jumper cables.
- USB to mini-USB cable.

Setup
- Plug in the UART/USB connector. On Linux, your kernel will probably detect it correctly. On macOS, the pl2303 driver needs to be installed.
- Connect TX(D) of the USB connector to the PC11 pin on the board with a dupont cable. (Only used for trace acquisition with analysis.c though.)
- Connect RX(D) of the USB connector to the PC10 pin on the board with a dupont cable.
- Connect GND of the USB connector to a GND pin on the board with a dupont cable.
- Connect the USB to mini-USB cable for power and flashing.

Benchmarking
- With everything connected, call 'make' to create a binary.
- Execute 'common/host.py' to listen on /dev/ttyUSB0 and keep that window open.
- Execute 'deploy.sh' to flash the binary to the board.
- Some output should be visible in the other window.

The current C file only does benchmarking and prints cycle counts. To see other output, this file needs to be changed.
