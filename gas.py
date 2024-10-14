import os
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D22)

mcp = MCP.MCP3008(spi, cs)

chan0 = AnalogIn(mcp, MCP.P0)


last_read = 0   
tolerance = 250 


def gas():
						
    def remap_range(value, left_min, left_max, right_min, right_max):
            left_span = left_max - left_min
            right_span = right_max - right_min
            

            valueScaled = int(value - left_min) / int(left_span)
            

            return int(right_min + (valueScaled * right_span))

    while True:
            trim_pot_changed = False
            
            trim_pot = chan0.value
            
            pot_adjust = abs(trim_pot - last_read)
             
            if pot_adjust > tolerance:
                    trim_pot_changed = True
            
                    
            if trim_pot_changed:
                    set_volume = remap_range(trim_pot, 0, 65535, 0, 100)
                    set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' \
                    .format(volume = set_volume)
                    os.system(set_vol_cmd)
                    last_read = trim_pot
            print("")

    return set_volume
