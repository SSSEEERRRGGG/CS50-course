import sys

def main():
    if len(sys.argv)!=2 or not sys.argv[1].isdigit():
        print("Wrong number of arguments. Please try again.")
        return 1
    
    k = int(sys.argv[1])
    
    p = input("plaintext: ")
    print("ciphertext: ", end="")
    for i in range(len(p)):
        if p[i].isupper():
            print(chr(ord('A') + (ord(p[i]) - ord('A') + k) % 26 ), end="")
        elif p[i].islower():
            print(chr(ord('a') + (ord(p[i]) - ord('a') + k) % 26 ), end="")
        else:
            print(p[i], end="")
    
    print("")
    
    return 0
    
    
if __name__ == "__main__":
    main()