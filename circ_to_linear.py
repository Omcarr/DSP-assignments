import numpy as np

def circular_convolution(x, h, N):
    y = np.zeros(N, dtype=int)
    for n in range(N):
        for k in range(N):
            j = (n - k + N) % N
            y[n] += x[k] * h[j]
    return y

def linear_convolution_using_circular(x, h):
    M = len(x)
    N = len(h)
    P = M + N - 1  # Length of the linear convolution

    # Zero-padding the sequences to length P
    x_padded = np.zeros(P, dtype=int)
    h_padded = np.zeros(P, dtype=int)

    x_padded[:M] = x
    h_padded[:N] = h

    # Perform circular convolution on the padded sequences
    return circular_convolution(x_padded, h_padded, P)

def main():
    M = int(input("Enter the length of x[n]: "))
    x = np.zeros(M, dtype=int)
    x = [float(i) for i in input("Enter the values of x[n]: ").split()]

    N = int(input("Enter the length of h[n]: "))
    h = np.zeros(N, dtype=int)
    h = [float(i) for i in input("Enter the values of h[n]: ").split()]

    # Perform linear convolution using circular convolution
    y = linear_convolution_using_circular(x, h)

    # Print results
    print("\nThe resulted linear convolution of:")
    print("\nx[n]:", ' '.join(map(str, x)))
    print("\nh[n]:", ' '.join(map(str, h)))
    print("\ny[n]:", ' '.join(map(str, y)))

if __name__ == "__main__":
    main()
