import math

#function to perform 4-point DIT-FFT
def DITFFT_4_Point(N, x):
    t = [[0, 0] for _ in range(N)]  
    G = [[0, 0] for _ in range(N)]  
    H = [[0, 0] for _ in range(N)]  
    
    #Calculate G[k] and H[k] based on even and odd indexed elements
    G[0][0] = x[0][0] + x[2][0]
    G[0][1] = x[0][1] + x[2][1]
    G[1][0] = x[0][0] - x[2][0]
    G[1][1] = x[0][1] - x[2][1]
    H[0][0] = x[1][0] + x[3][0]
    H[0][1] = x[1][1] + x[3][1]
    H[1][0] = x[1][0] - x[3][0]
    H[1][1] = x[1][1] - x[3][1]
    
    #Combine G[k] and H[k] with the twiddle factor WNnk
    e = 6.283185307179586 / N

    for k in range(2):
        # Calculate FFT results for the first half of the array
        t[k][0] = G[k][0] + (H[k][0] * math.cos(e * k) + H[k][1] * math.sin(e * k))
        t[k][1] = G[k][1] + (H[k][1] * math.cos(e * k) - H[k][0] * math.sin(e * k))
        
        # Calculate FFT results for the second half of the array
        t[k + 2][0] = G[k][0] + (H[k][0] * math.cos(e * (k + 2)) + H[k][1] * math.sin(e * (k + 2)))
        t[k + 2][1] = G[k][1] + (H[k][1] * math.cos(e * (k + 2)) - H[k][0] * math.sin(e * (k + 2)))
    
    return t

#function to perform 8-point DIT-FFT using two 4-point FFTs
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

def main():
    x = [[0, 0] for _ in range(8)]
    X = [[0, 0] for _ in range(8)] 

    L = int(input("Choose the length of x[n] (4 or 8): "))
    N = 8 if L > 4 else 4

    #Real
    print("Enter the real part of x[n]: ", end='')
    x_values_real= list(map(float, input().split()))
    #imag
    print("Enter the Imaginary part of x[n]: ", end='')
    x_values_imag = list(map(float, input().split()))

    for i in range(L):
        x[i][0] = x_values_real[i]
    
    for i in range(L):
        x[i][1] = x_values_imag[i]
    
    print()
    print("Input signal x[n] = ", end="")
    for i in range(L):
        if x[i][0]>=0:
            print(f"{x[i][0]:4.2f} + {x[i][1]:4.2f} j ", end=" ")
        else:
            print(f"{x[i][0]:4.2f} {x[i][1]:4.2f} j ", end=" ")

    # Perform DIT-FFT
    if N == 4:
        X = DITFFT_4_Point(N, x)
    elif N == 8:
        X = DITFFT_8_Point(N, x)
    else:
        exit(0)

    print("\n\nFFT results X[k]: ")
    for k in range(N):
        print(f"{X[k][0]:7.3f}  + j  {X[k][1]:7.3f}")

    for i in range(N):
        x[i][0] = 0
        x[i][1] = 0

    #complex conjugate of X[k]
    for k in range(N):
        X[k][1] *= -1

    #FFT on the conjugate
    if N == 4:
        x = DITFFT_4_Point(N, X)
    elif N == 8:
        x = DITFFT_8_Point(N, X)
    else:
        exit(0)

    #Normalize the result to get the inverse FFT
    for n in range(N):
        x[n][0] /= N
        x[n][1] = (-1) * x[n][1] / N

    print("\nInverse FFT results x[n]:")
    for n in range(N):
        print(f"{x[n][0]:7.3f}  + j  {x[n][1]:7.3f}")

if __name__ == "__main__":
    main()
