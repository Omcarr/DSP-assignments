import sys
def linear_convolution(x, h):
    # Get the length of the input and output signals
    L = len(x)
    M = len(h)
    N = L + M - 1
    # Initialize the output with zeros
    y = [0] * N
    for k in range(N):
        temp = 0
        i = k + 1
        for j in range(N):
            # Move index backward to align x and h
            i -= 1
            # Check if indices are valid to prevent out-of-bound error
            if i >= 0 and j < L and i < M:
                temp += x[j] * h[i]
            if i == 0:
                i += N
        y[k] = temp
    return y


def main():
    # getting L and x(n)
    L = int(input("Enter the length of x[n] ie L = "))
    print('Enter all values for x(n):', end=' ')

    x = list(map(float, input().split()))
    if len(x) != L:
        sys.exit('Incorrect number of values for x(n)')

    # getting M and h(n)
    M = int(input("Enter the length of h[n] ie M = "))
    print('Enter all values for h(n):', end=' ')

    h = list(map(float, input().split()))
    if len(x) != L:
        sys.exit('Incorrect number of values for h(n)')

    # calculate the Linear convolution y(n)
    y = linear_convolution(x, h)
    
    #print the result
    print("\n x[n] = ", end="")
    for i in range(L):
        print(f"{x[i]:4.2f}  ", end="")

    print("\n h[n] = ", end="")
    for i in range(M):
        print(f"{h[i]:4.2f}  ", end="")
    
    print("\n y[n] = ", end="")
    for i in range(L + M - 1):
        print(f"{y[i]:4.2f}  ", end="")


if __name__ == "__main__":
    main()
