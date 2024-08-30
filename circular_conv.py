import numpy as np
import sys

def circular_convolution(x, h):
    L = len(x)
    M = len(h)
    N = max(L, M)

    # Extend x and h to length N if necessary
    x_extended = np.zeros(N)
    h_extended = np.zeros(N)

    x_extended[:L] = x
    h_extended[:M] = h
    
    # Prepare output array
    y = np.zeros(N)

    for n in range(N):
        temp_sum = 0
        # Calculating value for each index, h(n) keeps moving to the right
        for k in range(N):
            m = (n - k) % N
            temp_sum += x_extended[k] * h_extended[m]
        y[n] = temp_sum

    return y

def main():
    # Get L and x[n] from the user
    L = int(input("Enter the length of x[n] (L): "))
    print("Enter the values for x(n): ", end='')
    x = list(map(float, input().strip().split()))
    if len(x) != L:
        sys.exit("Incorrect number of values for x(n)")

    # Get M and h[n] from the user
    M = int(input("Enter the length of h[n] (M): "))
    print("Enter the values for h(n): ", end='')
    h = list(map(float, input().strip().split()))
    if len(h) != M:
        sys.exit("Incorrect number of values for h(n)")

    y = circular_convolution(x, h)
    
    N = max(L, M)
    # Print results
    print("\n x[n] = ", end="")
    for i in range(N):
        if i < L:
            print(f"{x[i]:4.2f}  ", end="")
        else:
            print("0.00  ", end="")  # Padding value for array display

    print("\n h[n] = ", end="")
    for i in range(N):
        if i < M:
            print(f"{h[i]:4.2f}  ", end="")
        else:
            print("0.00  ", end="")

    print("\n y[n] = ", end="")
    for i in range(N):
        print(f"{y[i]:4.2f}  ", end="")

if __name__ == "__main__":
    main()
