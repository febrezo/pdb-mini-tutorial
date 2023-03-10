import sys

def main(params):
    length = len(params)
    print(f"Total params: {length}")

    print("Listing parametersâ€¦")
    for i, p in enumerate(params):
        print(f"\t- Param #{i}: {p}")

    print("Finishing executionâ€¦")

if __name__ == "__main__":
    print(f"Params: {sys.argv}")
    main(sys.argv)
