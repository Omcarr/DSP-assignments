import math
#calculating dft values
def dft(N, a, b):
    A = [0] * N
    B = [0] * N
    omega = 2.0 * math.pi / N
    
    for k in range(N):
        A[k] = 0
        B[k] = 0
        
        for n in range(N):
            arg = omega * k * n
            c = math.cos(arg)
            d = math.sin(arg)

            A[k] += a[n] * c + b[n] * d
            B[k] += -a[n] * d + b[n] * c
            
    return A, B

#calculating idft values
def idft(N, A, B):
    a = [0] * N
    b = [0] * N
    
    omega = 2.0 * math.pi / N

    for k in range(N):
        a[k] = 0
        b[k] = 0

        for n in range(N):
            arg = omega * k * n
            c = math.cos(arg)
            d = math.sin(arg)

            a[k] += A[n] * c - B[n] * d
            b[k] += A[n] * d + B[n] * c

        a[k] /= N
        b[k] /= N

    return a, b

# Calculate magnitude spectrum
def magnitude_spectrum(N, A, B):
    magnitude = [0] * N
    for k in range(N):
        magnitude[k] = math.sqrt(A[k]**2 + B[k]**2)
    return magnitude

def main():
    #gettinginput from the user
    N = int(input("Enter the length of x[n] ie N = "))

    print("Enter the real part of x[n]:",end=' ')
    a = list(map(float, input().split()))

    print("Enter the imaginary part of x[n]:",end=' ')
    b = list(map(float, input().split()))

    if len(a) < N or len(b) < N:
        raise ValueError("Number of inputs less than specified N")

    # Perform DFT
    A, B = dft(N, a, b)
    
    #print DFT 
    print("\nX[k] by DFT:")
    for i in range(N):
        print(f"{A[i]:6.2f} + j{B[i]:6.2f}")
    
    #calculate magnitude spectrum
    magnitude = magnitude_spectrum(N, A, B)

    #magnitude spectrum
    print("\nMagnitude Spectrum |X[k]|:")
    for i in range(N):
        print(f"|X[{i}]| = {magnitude[i]:6.2f}")




    # Perform IDFT
    a_reconstructed, b_reconstructed = idft(N, A, B)

    #print IDFT
    print("\nx[n] by IDFT:")
    for i in range(N):
        print(f"{a_reconstructed[i]:6.2f} + j{b_reconstructed[i]:6.2f}")

if __name__ == "__main__":
    main()
