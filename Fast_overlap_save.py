import math
import numpy as np

def DITFFT_4_Point(N, x):
    t = [[0, 0] for _ in range(N)]
    G = [[0, 0] for _ in range(N)]
    H = [[0, 0] for _ in range(N)]
    
    # Calculate G[k] and H[k] based on even and odd indexed elements
    G[0][0] = x[0][0] + x[2][0]
    G[0][1] = x[0][1] + x[2][1]
    G[1][0] = x[0][0] - x[2][0]
    G[1][1] = x[0][1] - x[2][1]
    H[0][0] = x[1][0] + x[3][0]
    H[0][1] = x[1][1] + x[3][1]
    H[1][0] = x[1][0] - x[3][0]
    H[1][1] = x[1][1] - x[3][1]
    
    # Combine G[k] and H[k] with the twiddle factor WNnk
    e = 6.283185307179586 / N

    for k in range(2):
        t[k][0] = G[k][0] + (H[k][0] * math.cos(e * k) + H[k][1] * math.sin(e * k))
        t[k][1] = G[k][1] + (H[k][1] * math.cos(e * k) - H[k][0] * math.sin(e * k))
        
        t[k + 2][0] = G[k][0] + (H[k][0] * math.cos(e * (k + 2)) + H[k][1] * math.sin(e * (k + 2)))
        t[k + 2][1] = G[k][1] + (H[k][1] * math.cos(e * (k + 2)) - H[k][0] * math.sin(e * (k + 2)))
    
    return t

def DITFFT_8_Point(N, x):
    t = [[0, 0] for _ in range(N)]
    
    # Divide the input array into two 4-point arrays
    X1 = [[x[2 * i][0], x[2 * i][1]] for i in range(4)]
    X2 = [[x[2 * i + 1][0], x[2 * i + 1][1]] for i in range(4)]
    
    # Perform 4-point FFT on both halves
    G = DITFFT_4_Point(4, X1)
    H = DITFFT_4_Point(4, X2)
    
    e = 6.283185307179586 / N 

    for k in range(4):
        t[k][0] = G[k][0] + (H[k][0] * math.cos(e * k) + H[k][1] * math.sin(e * k))
        t[k][1] = G[k][1] + (H[k][1] * math.cos(e * k) - H[k][0] * math.sin(e * k))
        
        d = k + 4
        t[d][0] = G[k][0] + (H[k][0] * math.cos(e * d) + H[k][1] * math.sin(e * d))
        t[d][1] = G[k][1] + (H[k][1] * math.cos(e * d) - H[k][0] * math.sin(e * d))

    return t

def Fast_Circular_Convolve(x, N, h, y):
    # Initialize arrays
    X = np.zeros((N, 2), dtype=float)
    H = np.zeros((N, 2), dtype=float)
    Y = np.zeros((N, 2), dtype=float)
    t = np.zeros((N, 2), dtype=float)
    p = np.zeros((N, 2), dtype=float)

    # Copy x[n] to t[n][0]
    for i in range(N):
        t[i][0] = x[i]
        t[i][1] = 0

    # Find X[k]
    if N == 4:
        X = DITFFT_4_Point(N, t)
    elif N == 8:
        X = DITFFT_8_Point(N, t)

    # Copy h[n] to t[n][0]
    for i in range(N):
        t[i][0] = h[i]
        t[i][1] = 0

    # Find H[k]
    if N == 4:
        H = DITFFT_4_Point(N, t)
    elif N == 8:
        H = DITFFT_8_Point(N, t)

    # Find Y[k]
    for k in range(N):
        a, b = X[k][0], X[k][1]
        c, d = H[k][0], H[k][1]
        Y[k][0] = (a * c) - (b * d)
        Y[k][1] = (b * c) + (a * d)

    # Find Y*[k] (conjugate)
    for k in range(N):
        Y[k][1] *= -1

    # Find FFT{Y*[k]}
    if N == 4:
        p = DITFFT_4_Point(N, Y)
    elif N == 8:
        p = DITFFT_8_Point(N, Y)

    # Find p[n] = {FFT{Y*[k]} / N}*
    for i in range(N):
        p[i][0] /= N
        p[i][1] = (-1) * p[i][1] / N

    # Copy p[][] to y[n]
    for i in range(N):
        y[i] = p[i][0]
        
def next_power_of_2(x):
    """Finds the next power of 2 greater than or equal to x."""
    return 1 << (x - 1).bit_length()

def pad_zeros_to(x, length):
    """Pads the array x with zeros to make its length equal to 'length'."""
    return np.pad(x, (0, max(0, length - len(x))), 'constant')

def fft_convolution(x, h, N):
    """Performs FFT-based convolution."""
    X = np.fft.fft(x, N)
    H = np.fft.fft(h, N)
    Y = X * H
    return np.fft.ifft(Y).real
def overlap_save_convolution(x, h, B, K=None):
    """Overlap-Save convolution of x and h with block length B."""
    M = len(x)
    N = len(h)

    if K is None:
        K = max(B, next_power_of_2(N))
        
    # Calculate the number of input blocks
    num_input_blocks = np.ceil(M / B).astype(int) \
                     + np.ceil(K / B).astype(int) - 1

    # Pad x to an integer multiple of B
    xp = pad_zeros_to(x, num_input_blocks*B)

    output_size = num_input_blocks * B + N - 1
    y = np.zeros((output_size,))
    
    # Input buffer
    xw = np.zeros((K,))

    # Convolve all blocks
    for n in range(num_input_blocks):
        # Extract the n-th input block
        xb = xp[n*B:n*B+B]

        # Sliding window of the input
        xw = np.roll(xw, -B)
        xw[-B:] = xb

        # Fast convolution
        u = fft_convolution(xw, h, K)

        # Save the valid output samples
        y[n*B:n*B+B] = u[-B:]

    return y[:M+N-1]

def main():
    max_len = 1000
    x = np.zeros(max_len)
    h = np.zeros(max_len)

    # Input x[n]
    length = int(input("Enter the length of x[n]: "))
    print("Enter the values of x[n]: ", end='')
    x_values = list(map(float, input().split()))
    if len(x_values) != length:
        print("Error: The number of values entered does not match the specified length.")
        return
    for i in range(length):
        x[i] = x_values[i]

    # Input h[n]
    M = int(input("\nEnter the length of h[n]: "))
    print("Enter the values of h[n]: ", end='')
    h_values = list(map(float, input().split()))
    if len(h_values) != M:
        print("Error: The number of values entered does not match the specified length.")
        return
    for i in range(M):
        h[i] = h_values[i]

    # Display input x[n]
    print("\nx[n] = ", end="")
    for i in range(length):
        print(f"{x[i]:4.2f}  ", end="")
    
    # Display input h[n]
    print("\nh[n] = ", end="")
    for i in range(M):
        print(f"{h[i]:4.2f}  ", end="")

    # Overlap-Save Method
    B = 8  # Block length
    y = overlap_save_convolution(x[:length], h[:M], B)

    # Display the final result
    print("\n\nLinear Convolution Output using Overlap-Save Method:")
    print("y[n] = ", end="")
    for i in range(len(y)):
        print(f"{y[i]:4.2f} ", end="")
    print("\n\n")

if __name__ == "__main__":
    main()