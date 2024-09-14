import numpy as np

def detect(signal, original_length):
    for i in range(original_length):
        if signal[i] != 0:
            return i
    return original_length

def correlate(x, h):
    lx = len(x)
    lh = len(h)

    N = len(x) + 10 
    x_buffered = np.zeros(N)
    h_buffered = np.zeros(N)
    
    x_buffered[10:10+lx] = x
    h_buffered[10:10+lh] = h
    
    # Detect starting index of non-zero values
    stx = detect(x_buffered, N)
    sth = detect(h_buffered, N)
    
    print(f"stx = {stx}  lx = {lx}")
    print(f"sth = {sth}  lh = {lh}")

    # Correlate length calculations
    nneg = (sth - stx) + lh - 1
    npos = lx - (sth - stx)
    print(f"nneg = {nneg}  npos = {npos}")

    # Pre allocataing y based on calculated range for nneg and npos
    y = np.zeros(nneg + npos)

    # getting correlation using calculated index ranges
    for i in range(-nneg, npos):
        temp_sum = 0
        for j in range(10, 10 + lx):
            if 10 <= (j - i) < (10 + lh):
                temp_sum += x_buffered[j] * h_buffered[j - i]
        y[i + nneg] = temp_sum  # Adjust for negative offset index

    return y


def check_signal_symmetry(signal):
    # Check if time is symmetric around zero
    if np.array_equal(signal, np.flip(signal)):
        return 'even'
    elif np.array_equal(signal, -np.flip(signal)):
        return 'odd'
    else:
        return 'neither odd nor even'

def calculate_energy(signal):
    return np.sum(np.abs(signal)**2)

def calculate_power(signal):
    N = len(signal)
    return np.sum(np.abs(signal)**2) / N

#power/enegry classification
def classify_signal(signal):
    N = len(signal)

    # Calculate energy and power
    energy = calculate_energy(signal)
    power = calculate_power(signal)

    # Define thresholds for classification
    energy_threshold = 1e-10
    power_threshold = 1e-10

    if energy < energy_threshold and power > power_threshold:
        return 'energy signal'
    elif power < power_threshold and energy > energy_threshold:
        return 'power signal'
    else:
        return 'undefined'



def main():
    # Get lengths and values for x and h
    lx = int(input("Enter the length of x[n]: "))
    x_values = list(map(float, input(f"Enter {lx} values for x[n]: ").split()))

    lh = int(input("Enter the length of h[n]: "))
    h_values = list(map(float, input(f"Enter {lh} values for h[n]: ").split()))

    y = correlate(x_values, h_values)

    # Display x, h, and y
    print("\n x = ", end="")
    for value in x_values:
        print(f"{value:6.2f} ", end="")

    print("\n h = ", end="")
    for value in h_values:
        print(f"{value:6.2f} ", end="")

    print("\n y = ", end="")
    for value in y:
        print(f"{value:6.2f} ", end="")

    
    result = check_signal_symmetry(signal=y)
    print(f"\n\nThe signal is {result}.")

    #calculate energy
    energy = calculate_energy(signal=y)
    print(f"The energy of the signal is {energy}")

    #calculate power 
    power = calculate_power(signal=y)
    print(f"The power of the signal is {power}")
    
    #is enegry or power signal
    classification = classify_signal(signal=y)
    print(f"The signal is classified as: {classification}.")
    


if __name__ == "__main__":
    main()
