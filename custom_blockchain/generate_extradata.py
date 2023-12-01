#Generate extradata for adding to genesis.json

# Define the signer addresses
signer_addresses = [
    "8043e40446e8f377D2beC152fF4Bf471d12555FD",
    "2d862b18BC5816B438c49931f8264926c2144190"
    # Add more signer addresses here if needed
]

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

print(genesis_json)