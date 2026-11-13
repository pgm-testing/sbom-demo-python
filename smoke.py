from importlib.metadata import version
from stellar_sdk import Keypair
import tansu

for name, expected in (
    ("stellar-sdk", "17.0.1"),
    ("stellar-contract-bindings", "0.6.0b0"),
    ("strledger", "0.11.0"),
    ("requests", "2.34.2"),
    ("tansu", "1.0.1"),
):
    assert version(name) == expected, (name, version(name))
assert Keypair.from_raw_ed25519_seed(bytes(32)).public_key.startswith("G")
print("Pinned dependencies installed; offline Stellar SDK smoke check passed.")
