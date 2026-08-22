# -*- coding: utf-8 -*-

# Copyright (c) 2026 The Basicswap developers
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

from basicswap.util import COIN

# Dimecoin is an X11 UTXO coin (a Dash/Bitcoin fork). Address prefixes and WIF
# prefix differ from Bitcoin, bech32 HRP is "vx", no native segwit.
# bip44 is a placeholder - confirm the real SLIP-44 coin type before release.
params = {
    "name": "dimecoin",
    "ticker": "DIME",
    "display_name": "Dimecoin",
    "message_magic": "Dimecoin Signed Message:\n",
    "blocks_target": 60,
    "decimal_places": 5,
    "has_cltv": True,
    "has_csv": True,
    "has_segwit": False,
    "mainnet": {
        "rpcport": 8332,
        "pubkey_address": 15,
        "script_address": 9,
        "key_prefix": 143,
        "hrp": "vx",
        "bip44": 15,
        "min_amount": 100000,
        "max_amount": 10000000 * COIN,
    },
    "testnet": {
        "rpcport": 18332,
        "pubkey_address": 15,
        "script_address": 9,
        "key_prefix": 143,
        "hrp": "vx",
        "bip44": 1,
        "min_amount": 100000,
        "max_amount": 10000000 * COIN,
        "name": "testnet3",
    },
    "regtest": {
        "rpcport": 18332,
        "pubkey_address": 15,
        "script_address": 9,
        "key_prefix": 143,
        "hrp": "vx",
        "bip44": 1,
        "min_amount": 100000,
        "max_amount": 10000000 * COIN,
    },
}
