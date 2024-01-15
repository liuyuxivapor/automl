import numpy as np

with open('testInput_f32_1kHz_15kHz.bin', 'rb') as file:
    testInput_f32_1kHz_15kHz = np.fromfile(file, dtype=np.float32, count=320)
    
with open('refOutput.bin', 'rb') as file:
    refOutput = np.fromfile(file, dtype=np.float32, count=320)
    
scaler = 0.01
    
# Scale the FIR coefficients to the range [-scaler, scaler]
max_abs_value = np.max(np.abs(testInput_f32_1kHz_15kHz))
x_data_scaled = scaler * testInput_f32_1kHz_15kHz / max_abs_value

# Scale the FIR coefficients to the range [-scaler, scaler]
max_abs_value = np.max(np.abs(refOutput))
y_data_scaled = scaler * refOutput / max_abs_value

np.savetxt('train.x', x_data_scaled)
np.savetxt('train.y', y_data_scaled)
np.savetxt('test.x', x_data_scaled)
np.savetxt('test.y', y_data_scaled)