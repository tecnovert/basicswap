#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 tecnovert
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

import copy
from enum import IntEnum
from basicswap.util.crypto import blake256
from basicswap.util.integer import decode_varint, encode_varint


class TxSerializeType(IntEnum):
    Full = 0
    NoWitness = 1
    OnlyWitness = 2


class COutpoint:
    __slots__ = ('hash', 'n', 'tree')


class CTxIn:
    __slots__ = ('prevout', 'sequence',
                 'value_in', 'block_height', 'block_index', 'signature_script')  # Witness


class CTxOut:
    __slots__ = ('value', 'version', 'script_pubkey')


class CTransaction:
    __slots__ = ('hash', 'version', 'vin', 'vout', 'locktime', 'expiry')

    def __init__(self, tx=None):
        if tx is None:
            self.version = 1
            self.vin = []
            self.vout = []
            self.locktime = 0
            self.expiry = 0
        else:
            self.version = tx.version
            self.vin = copy.deepcopy(tx.vin)
            self.vout = copy.deepcopy(tx.vout)
            self.locktime = tx.locktime
            self.expiry = tx.expiry


    def deserialize(self, data: bytes) -> None:

        version = int.from_bytes(data[:4], 'little')
        self.version = self.version & 0xffff
        ser_type: int = version >> 16
        o = 4

        if ser_type == TxSerializeType.Full or ser_type == TxSerializeType.NoWitness:
            num_txin, nb = decode_varint(data, o)
            o += nb

            for i in range(num_txin):
                txi = CTxIn()
                txi.prevout = COutpoint()
                txi.prevout.hash = int.from_bytes(data[o:o + 32], 'little')
                o += 32
                txi.prevout.n = int.from_bytes(data[o:o + 4], 'little')
                o += 4
                txi.prevout.tree = data[o]
                o += 1
                txi.sequence = int.from_bytes(data[o:o + 4], 'little')
                o += 4
                self.vin.append(txi)

            num_txout, nb = decode_varint(data, o)
            o += nb

            for i in range(num_txout):
                txo = CTxOut()
                txo.value = int.from_bytes(data[o:o + 8], 'little')
                o += 8
                txo.version = int.from_bytes(data[o:o + 2], 'little')
                o += 2
                script_bytes, nb = decode_varint(data, o)
                o += nb
                txo.script_pubkey = data[o:o + script_bytes]
                o += script_bytes
                self.vout.append(txo)

            self.locktime = int.from_bytes(data[o:o + 4], 'little')
            o += 4
            self.expiry = int.from_bytes(data[o:o + 4], 'little')
            o += 4

        num_wit_scripts, nb = decode_varint(data, o)
        o += nb

        if ser_type == TxSerializeType.OnlyWitness:
            self.vin = [CTxIn() for _ in range(num_wit_scripts)]
        else:
            if num_wit_scripts != len(self.vin):
                raise ValueError('non equal witness and prefix txin quantities')

        for i in range(num_wit_scripts):
            txi = self.vin[i]
            txi.value_in = int.from_bytes(data[o:o + 8], 'little')
            o += 8
            txi.block_height = int.from_bytes(data[o:o + 4], 'little')
            o += 4
            txi.block_index = int.from_bytes(data[o:o + 4], 'little')
            o += 4
            script_bytes, nb = decode_varint(data, o)
            o += nb
            txi.signature_script = data[o:o + script_bytes]
            o += script_bytes

    def serialize(self, ser_type=TxSerializeType.Full) -> bytes:
        data = bytearray()
        version = (self.version & 0xffff) | (ser_type << 16)
        data += version.to_bytes(4, 'little')

        if ser_type == TxSerializeType.Full or ser_type == TxSerializeType.NoWitness:
            data += encode_varint(len(self.vin))
            for txi in self.vin:
                data += txi.prevout.hash.to_bytes(32, 'little')
                data += txi.prevout.n.to_bytes(4, 'little')
                data += txi.prevout.tree.to_bytes(1)
                data += txi.sequence.to_bytes(4, 'little')

            data += encode_varint(len(self.vout))
            for txo in self.vout:
                data += txo.value.to_bytes(8, 'little')
                data += txo.version.to_bytes(2, 'little')
                data += encode_varint(len(txo.script_pubkey))
                data += txo.script_pubkey

            data += self.locktime.to_bytes(4, 'little')
            data += self.expiry.to_bytes(4, 'little')

        if ser_type == TxSerializeType.Full or ser_type == TxSerializeType.OnlyWitness:
            data += encode_varint(len(self.vin))
            for txi in self.vin:
                data += txi.value_in.to_bytes(8, 'little')
                data += txi.block_height.to_bytes(4, 'little')
                data += txi.block_index.to_bytes(4, 'little')
                data += encode_varint(len(txi.signature_script))
                data += txi.signature_script

        return data

    def TxHash(self) -> bytes:
        return blake256(self.serialize(TxSerializeType.NoWitness))[::-1]

    def TxHashWitness(self) -> bytes:
        raise ValueError('todo')

    def TxHashFull(self) -> bytes:
        raise ValueError('todo')