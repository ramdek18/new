from pathlib import Path
from typing import List
from blspy import AugSchemeMPL
from src.util.ints import uint32
from src.util.keychain import Keychain
from src.util.validate_alert import validate_alert_file, create_alert_file

ready = True
bitcoin_hash = None
bram_message = None

print("")
print("___________ BITCOIN BLOCK HASH ____________")
while True:
    bitcoin_hash = input("Insert Bitcoin block hash: ")
    print(f"Bitcoin block hash = {bitcoin_hash}")
    y_n = input("Does this look good (y/n): ").lower()
    if y_n == "y":
        break

print("")
print("___________ BRAM MESSAGE ____________")
while True:
    bram_message = input("Insert message from Bram: ")
    print(f"Bram message = {bram_message}")
    y_n = input("Does this look good (y/n): ").lower()
    if y_n == "y":
        break

genesis_challenge_preimage = f"bitcoin_hash:{bitcoin_hash},bram_message:{bram_message}"


keychain: Keychain = Keychain()
print("")
print("___________ SELECT KEY ____________")

private_keys = keychain.get_all_private_keys()
if len(private_keys) == 0:
    print("There are no saved private keys.")
    quit()
print("Showing all private keys:")
for sk, seed in private_keys:
    print("")
    print("Fingerprint:", sk.get_g1().get_fingerprint())
print("")

selected_key = None
while True:
    user_input = input("Enter fingerprint of the key you want to use, or enter Q to quit: ").lower()
    if user_input == "q":
        quit()
    for sk, seed in private_keys:
        fingerprint = sk.get_g1().get_fingerprint()
        pub = sk.get_g1()
        if int(user_input) == fingerprint:
            print(f"Selected: {fingerprint}")
            selected_key = sk
            break

    if selected_key is not None:
        break

print("")
print("___________ HD PATH ____________")
while True:
    hd_path = input("Enter the HD path in the form 'm/12381/8444/n/n', or enter Q to quit: ").lower()
    if hd_path == "q":
        quit()
    verify = input(f"Is this correct path: {hd_path}? (y/n) ").lower()
    if verify == "y":
        break


k = Keychain()
private_keys = k.get_all_private_keys()
path: List[uint32] = [uint32(int(i)) for i in hd_path.split("/") if i != "m"]

# Derive HD key using path form input
for c in path:
    selected_key = AugSchemeMPL.derive_child_sk(selected_key, c)
print("Public key:", selected_key.get_g1())

# get file path
file_path = None
while True:
    file_path = input("Enter the path where you want to save signed alert file, or q to quit: ")
    if file_path == "q" or file_path == "Q":
        quit()
    file_path = file_path.strip()
    y_n = input(f"Is this correct path (y/n)?: {file_path} ").lower()
    if y_n == "y":
        break
f_path: Path = Path(file_path)

create_alert_file(f_path, selected_key, genesis_challenge_preimage)

pubkey = f"{bytes(selected_key.get_g1()).hex()}"
validated = validate_alert_file(f_path, pubkey)
if validated:
    print(f"Signature has passed validation for pubkey: {pubkey}")
else:
    print(f"Signature has failed validation for pubkey: {pubkey}")
    assert False
