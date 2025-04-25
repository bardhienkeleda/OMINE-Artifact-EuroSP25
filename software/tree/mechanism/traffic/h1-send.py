
# *************************************************************************
# 
#  Copyright 2025 Enkeleda Bardhi (TU Delft),
#                 Chenxing Ji (TU Delft),
#                 Ali Imran (University of Michigan),
#                 Muhammad Shahbaz (University of Michigan),
#                 Riccardo Lazzeretti (Sapienza University of Rome),
#                 Mauro Conti (University of Padua),
#                 Fernando Kuipers (TU Delft)
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# 
# *************************************************************************
from scapy.all import *
from scapy.utils import rdpcap
from helper import *
import numpy
import csv

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

    data = list(csv.reader(open("./batched_cicids_5000_test.csv"), delimiter='\t'))

    result = numpy.array(data).astype("float")

    # Creates packets by using data from the CSV file
    import time
    for y in range(5000):
        z = [c_to_fix(x) for x in result[y]]
        k = int(result[y][8])
        pkt = Ether(src="00:00:00:00:00:01",dst="00:00:00:00:00:04")/IP(
            len=80, src="10.0.0.1", dst="10.0.0.4")/FeatureHeader(
            field0=z[1], field1=z[2], field2=z[3], field3=z[4], field4=z[5], field5=z[6], field6=z[7], label=k, 
            count=0, weight5 = 0xde, weight5_2=0xad, output5=0xbe, output6=0xef)
        # pkt.show()
        sendp(pkt,iface="h1-eth0")
        if( y % 5 == 4):
            print("Sent packet count: {}".format(y+1))
            time.sleep(40)
        else:
            time.sleep(0.1)

    
if __name__ == "__main__":
    
    main()
