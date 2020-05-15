from sys import argv

def main():
    with open(argv[1], "r+") as file:
        recaps = []
        counter = 0
        for line in file:
            if line.startswith("__"):
                counter = (counter + 1) % 10
                recaps.append(line[2:-3])
                print(f"{'.' if counter else '|'}", end="")
        
        file.seek(0, 2)
        file.write("\n### Zusammenfassungszusammenfassung\n")
        file.write("\n".join(recaps))

if __name__ == "__main__":
    main()