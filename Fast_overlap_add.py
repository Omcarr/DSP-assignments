import math
import numpy as np

# Function to perform 4-point DIT-FFT
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
    e = 2 * math.pi / N

    for k in range(2):
        # Calculate FFT results for the first half of the array
        t[k][0] = G[k][0] + (H[k][0] * math.cos(e * k) + H[k][1] * math.sin(e * k))
        t[k][1] = G[k][1] + (H[k][1] * math.cos(e * k) - H[k][0] * math.sin(e * k))
        
        # Calculate FFT results for the second half of the array
        t[k + 2][0] = G[k][0] + (H[k][0] * math.cos(e * (k + 2)) + H[k][1] * math.sin(e * (k + 2)))
        t[k + 2][1] = G[k][1] + (H[k][1] * math.cos(e * (k + 2)) - H[k][0] * math.sin(e * (k + 2)))
    
    return t

# Function to perform 8-point DIT-FFT using two 4-point FFTs
def DITFFT_8_Point(N, x):
    t = [[0, 0] for _ in range(N)]
    
    # Divide the input array into two 4-point arrays
    X1 = [[x[2 * i][0], x[2 * i][1]] for i in range(4)]
    X2 = [[x[2 * i + 1][0], x[2 * i + 1][1]] for i in range(4)]
    
    # Perform 4-point FFT on both halves
    G = DITFFT_4_Point(4, X1)
    H = DITFFT_4_Point(4, X2)
    
    e = 2 * math.pi / N 

    for k in range(4):
        t[k][0] = G[k][0] + (H[k][0] * math.cos(e * k) + H[k][1] * math.sin(e * k))
        t[k][1] = G[k][1] + (H[k][1] * math.cos(e * k) - G[k][0] * math.sin(e * k))
        
        d = k + 4
        t[d][0] = G[k][0] + (H[k][0] * math.cos(e * d) + H[k][1] * math.sin(e * d))
        t[d][1] = G[k][1] + (H[k][1] * math.cos(e * d) - G[k][0] * math.sin(e * d))

    return t 
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

def overlap_add_convolution(x, h, B, K=None):
    """Overlap-Add convolution of x and h with block length B"""
    M = len(x)
    N = len(h)

    if K is None:
        K = max(B, next_power_of_2(N))

    # Calculate the number of input blocks
    num_input_blocks = np.ceil(M / B).astype(int)

    # Pad x to an integer multiple of B
    xp = pad_zeros_to(x, num_input_blocks*B)

    output_size = num_input_blocks * B + N - 1
    y = np.zeros((output_size,))

    # Convolve all blocks
    for n in range(num_input_blocks):
        # Extract the n-th input block
        xb = xp[n*B:(n+1)*B]

        # Fast convolution
        u = fft_convolution(xb, h, K)

        # Overlap-Add the partial convolution result
        y[n*B:n*B+len(u)] += u

    return y[:M+N-1]

def main():
    # Initialization
    max_len = 100  # Maximum size for signal arrays, adjust as needed
    x = np.zeros(max_len, dtype=float)
    h = np.zeros(max_len, dtype=float)
    y = np.zeros(max_len, dtype=float)

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

    # Overlap-Add Method (OAM)
    B = 8  # Block length, you can adjust this value as needed
    y = overlap_add_convolution(x[:length], h[:M], B)

    # Display the final result
    print('\n\nThe final output y[n] using Overlap Add method:')
    print("y[n] = ", end="")
    for i in range(length + M - 1):
        print(f"{y[i]:4.2f}  ", end="")
    print("\n\n")

if __name__ == "__main__":
    main()
