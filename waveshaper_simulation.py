import os
import sys
from scipy import signal
import numpy as np
import math

import matplotlib.pyplot as plt
import matplotlib.pyplot as y1_plt
import matplotlib.pyplot as y2_plt
import matplotlib.pyplot as y3_plt


cycle_length = 200
cycle_count = 2
wave_length = cycle_length*cycle_count
buffer_length = cycle_length*cycle_count
r1 = 1000.0
r2 = 2000.0
r3 = 500.0
r4 = 120.0
r5 = 50.0
gain = 5
edge = 1
mix = 1.0

k = [[0.0]*5 for i in range(5)]
v = [[0.0]*4 for i in range(3)]
x = range(0, wave_length)
wave = [0]*wave_length
line = [0]*wave_length
v_in = [0]*wave_length
v_in2 = [0]*wave_length
v_out1 = [0]*wave_length
v_out2 = [0]*wave_length
v_out_filtered = [0]*wave_length


k[4][0] = r2*r3*r4*r5
k[4][1] = r1*r3*r4*r5
k[4][2] = r1*r2*r4*r5
k[4][3] = r1*r2*r3*r5
k[4][4] = r1*r2*r3*r4

k[3][0] = r2*r3*r4
k[3][1] = r1*r3*r4
k[3][2] = r1*r2*r4
k[3][3] = r1*r2*r3
k[3][4] = 0

k[2][0] = r2*r3
k[2][1] = r1*r3
k[2][2] = r1*r2
k[2][3] = 0
k[2][4] = 0

k[1][0] = r2
k[1][1] = r1
k[1][2] = 00
k[1][3] = 00
k[1][4] = 0

k[0][0] = 1
k[0][1] = 0
k[0][2] = 0
k[0][3] = 0
k[0][4] = 0

v[0][0] = 0.10
v[0][1] = 0.400
v[0][2] = 0.7
v[0][3] = 1.0
v[1][0] = 0.30
v[1][1] = 0.600
v[1][2] = 0.9
v[1][3] = 1.1
v[2][0] = 0.80
v[2][1] = 0.900
v[2][2] = 1.0
v[2][3] = 1.1

v1 = 0.0
v2 = 0.0
v3 = 0.0
v4 = 0.0


for i in range(0,wave_length):
        wave[i] = 1.0000*math.sin(math.pi*2*i/(cycle_length))
        v_in[i] = math.sin(math.pi*2*i/(cycle_length))

break_state = 0

kIndex = 0
old_kIndex = 0
last_out = 0.0
reset_kIndex_count = 0
v_measure = 0.0
for j in range(0,cycle_count):

    for i in range(0,cycle_length):

        if(0.000 <= v_in[200*j+i]):
            v1 = v[edge][0]
            v2 = v[edge][1]
            v3 = v[edge][2]
            v4 = v[edge][3]
            while True:
                k1 = k[kIndex][0]
                k2 = k[kIndex][1]
                k3 = k[kIndex][2]
                k4 = k[kIndex][3]
                k5 = k[kIndex][4]
                v_out1[200*j+i] = (v_in[200*j+i]*gain*k1 + v1*k2 + v2*k3 + v3*k4 + v4*k5)/(k1 + k2 + k3 + k4 + k5)

                if kIndex == 0:
                    if v_out1[200*j+i] > v[edge][kIndex]: #too high, increment kIndex
                        kIndex += 1
                    else:
                        break
                elif kIndex == 4:
                    if v_out1[200*j+i] < v[edge][kIndex-1]: #too low, decrement kIndex
                        kIndex -= 1
                    else:
                        break
                else:
                    if v_out1[200*j+i] > v[edge][kIndex]: #too high, increment kIndex
                        kIndex += 1
                    elif v_out1[200*j+i] < v[edge][kIndex-1]: #too low, decrement kIndex
                        kIndex -= 1
                    else:
                        break
        else:
            v1 = -v[edge][0]
            v2 = -v[edge][1]
            v3 = -v[edge][2]
            v4 = -v[edge][3]
            while True:
                k1 = k[kIndex][0]
                k2 = k[kIndex][1]
                k3 = k[kIndex][2]
                k4 = k[kIndex][3]
                k5 = k[kIndex][4]
                v_out1[200*j+i] = (v_in[200*j+i]*gain*k1 + v1*k2 + v2*k3 + v3*k4 + v4*k5)/(k1 + k2 + k3 + k4 + k5)
                if kIndex == 0:
                    if v_out1[200*j+i] < -v[edge][kIndex]: #too low, increment kIndex
                        kIndex += 1
                    else:
                        break
                elif kIndex == 4:
                    if v_out1[200*j+i] > -v[edge][kIndex-1]: #too high, decrement kIndex
                        kIndex -= 1
                    else:
                        break
                else:
                    if v_out1[200*j+i] < -v[edge][kIndex]: #too low, increment kIndex
                        kIndex += 1
                    elif v_out1[200*j+i] > -v[edge][kIndex-1]: #too high, decrement kIndex
                        kIndex -= 1
                    else:
                        break
        v_out2[200*j+i] = 1.5*((1.0-mix)*v_in[200*j+i]+ mix*v_out1[200*j+i])

for i in range(0,wave_length):
    if(i < 4):
        v_out_filtered[i] = v_out2[i]
    else:
        v_out_filtered[i] = (v_out2[i-4]+v_out2[i-3]+v_out2[i-2]+v_out2[i-1]+v_out2[i])/5;

y1_plt.plot(x, v_in)
y2_plt.plot(x, line,'k')
y3_plt.plot(x, v_out_filtered)

plt.grid(which='both', axis='both')

plt.show()
