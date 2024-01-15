import numpy as np
from scipy.fftpack import dct

seed_value = 36
np.random.seed(seed_value)

x_train_data = np.random.rand(32768)
y_train_data = dct(x_train_data, type=4, norm='ortho')

x_test_data = np.random.rand(2048)
y_test_data = dct(x_test_data, type=4, norm='ortho')

# Scale the DCT coefficients to the range [-1, 1]
max_abs_value = np.max(np.abs(y_train_data))
y_train_data_scaled = y_train_data / max_abs_value

# Scale the DCT coefficients to the range [-1, 1]
max_abs_value = np.max(np.abs(y_test_data))
y_test_data_scaled = y_test_data / max_abs_value


# print("Min value of x_train_normalized:", np.min(y_train_data_scaled))
# print("Max value of x_train_normalized:", np.max(y_train_data_scaled))

# print("Min value of x_test_normalized:", np.min(y_test_data_scaled))
# print("Max value of x_test_normalized:", np.max(y_test_data_scaled))


np.savetxt('train.x', x_train_data)
np.savetxt('train.y', y_train_data_scaled)

np.savetxt('test.x', x_test_data)
np.savetxt('test.y', y_test_data_scaled)
