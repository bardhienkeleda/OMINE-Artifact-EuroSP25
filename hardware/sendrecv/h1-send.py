# *************************************************************************
#
# Copyright 2022 Tushar Swamy (Stanford University),
#                Alexander Rucker (Stanford University),
#                Annus Zulfiqar (Purdue University),
#                Muhammad Shahbaz (Stanford/Purdue University)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# *************************************************************************
from scapy.all import *
from scapy.utils import rdpcap
from helper import *
import numpy
import csv

MAX_PKT_COUNT = 5000

def c_to_fix(float_value):
    # Scaling by 2^16 (65536) for 16 bits fractional part
    scaled_value = float_value * 65536

    # Converting to integer (rounding or truncating as necessary)
    integer_value = int(round(scaled_value))

    # Converting to 32-bit binary representation
    # Format the integer value as a binary string with 32 bits, padding with zeros if necessary
    binary_representation = format(integer_value, '032b')

    return int(binary_representation,2)

def main():
    data = list(csv.reader(open("./batched_2000_test.csv"), delimiter='\t'))
    result = numpy.array(data).astype("float")

    # Creates packets by using data from the CSV file
    import time
    for y in range(MAX_PKT_COUNT):
        z = [c_to_fix(x) for x in result[y]]
        k = int(result[y][8])
        pkt = Ether()/IP()/FeatureHeader(field0=z[1], field1=z[2], field2=z[3], field3=z[4], field4=z[5], field5=z[6], field6=z[7], label=k, output=5)
        sendp(pkt,iface="h1-eth0", inter= .1/10)
        if(y % 100 == 0):
            time.sleep(20)
            
if __name__ == "__main__":
    
    main()
