import argparse


# Generate extradata for adding to genesis.json

def process(signer_addresses):
    # Step 1: Concatenate 32 zero bytes
    zero_bytes_32 = "00" * 32

    # Step 2: Concatenate all signer addresses
    all_signer_addresses = ''.join(signer_addresses)

    # Step 3: Concatenate 65 further zero bytes
    further_zero_bytes_65 = "00" * 65

    # Step 4: Combine all the strings
    encoded_extradata = zero_bytes_32 + all_signer_addresses + further_zero_bytes_65

    # Step 5: Use the result in genesis.json (replace "your_extradata_value" with the encoded_extradata)
    genesis_json = {
        "extradata": f"0x{encoded_extradata}"
    }

    return genesis_json


def main():
    parser = argparse.ArgumentParser(description="Generate extradata for adding to genesis.json")
    parser.add_argument("-signer_addresses", required=True, help="Signer Address or several addresses separated by ,")
    args = parser.parse_args()
    signer_addresses = []

    if ',' in args.signer_addresses:
        for item in args.signer_addresses.split(','):
            signer_addresses.append(item)
    else:
        signer_addresses.append(args.signer_addresses)

    print(process(signer_addresses))


if __name__ == "__main__":
    main()
