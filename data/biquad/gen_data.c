#include "arm_math.h"
#include "math_helper.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define NUM_STAGES 2
#define BLOCK_SIZE 2048
#define SCALER 0.1

// Coefficients for a low-pass filter -3dB 100-500Hz
const q31_t coeffs[10] = {
    536443447, -1072886894, 536443447, 1073741824, -536870912, 536443447, -1063777945, 527411186, 1062907350, -526144676,
};
float32_t coeffs_f32[10];

// State buffer for the filter
float32_t state[NUM_STAGES * 4];

float32_t input[BLOCK_SIZE];
float32_t output[BLOCK_SIZE];

int main() {
    // Convert q31_t data to float32_t data
    arm_q31_to_float(coeffs, coeffs_f32, 10);

    // Initialize the CMSIS DSP library
    arm_biquad_casd_df1_inst_f32 S;
    arm_biquad_cascade_df1_init_f32(&S, NUM_STAGES, coeffs_f32, state);

    srand(time(NULL));
    FILE *file_i = fopen("train.x", "w");
    for (int i = 0; i < BLOCK_SIZE; i++) {
        // Generate a random float between 0 and 1
        input[i] = (float)rand() / RAND_MAX * SCALER;
//        fprintf(file_i, "%f\n", input[i]);
//        printf("%f\n", input[i]);
    }

    // Apply the biquad filter to the input signal
    arm_biquad_cascade_df1_f32(&S, input, output, BLOCK_SIZE);

    FILE *file_o = fopen("train.y", "w");
    for (int i = 0; i < BLOCK_SIZE; i++) {
//        fprintf(file_o, "%f\n", output[i]);
        printf("%f\n", output[i]);
    }

    return 0;
}
