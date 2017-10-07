def main():
    while True:
        height = int(input("Height: "))
        if height == 0:
            return 0
        if height > 1 or height < 23:
            break

    for i in range(height):
        for j in range(height-i-1):
            print(" ", end="")
            
        for k in range(i+2):
            print("#", end="")
        print("")
        
    return 0

if __name__ == "__main__":
    main()