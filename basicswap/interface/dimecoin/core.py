# -*- coding: utf-8 -*-

# Copyright (c) 2026 The Basicswap developers
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

import os

from basicswap.interface.dimecoin.chainparams import params
from basicswap.interface.prepare_util import CoinPrepareModule, PrepareContext

DIME_VERSION = os.getenv("DIME_VERSION", "2.4.0.0")
DIME_VERSION_TAG = os.getenv("DIME_VERSION_TAG", "")

DIME_RPC_HOST = os.getenv("DIME_RPC_HOST", "127.0.0.1")
DIME_RPC_PORT = int(os.getenv("DIME_RPC_PORT", 8332))
DIME_ONION_PORT = int(os.getenv("DIME_ONION_PORT", 11931))  # nDefaultPort
DIME_RPC_USER = os.getenv("DIME_RPC_USER", "")
DIME_RPC_PWD = os.getenv("DIME_RPC_PWD", "")


class DIMEPrepare(CoinPrepareModule):
    def getConfigSegment(self, ctx: PrepareContext) -> dict:
        config = {
            "connection_type": "rpc",
            "manage_daemon": ctx.should_manage_daemon(self.ticker),
            "rpchost": DIME_RPC_HOST,
            "rpcport": DIME_RPC_PORT + ctx.port_offset,
            "onionport": DIME_ONION_PORT + ctx.port_offset,
            "datadir": os.getenv(
                "DIME_DATA_DIR", os.path.join(ctx.data_dir, self.name)
            ),
            "bindir": os.path.join(ctx.bin_dir, self.name),
            "use_segwit": False,
            "use_csv": True,
            "blocks_confirmed": 1,
            "conf_target": 2,
            "core_version_no": self.version + self.version_tag,
            "core_version_group": 18,
        }

        if self.rpc_user != "":
            config["rpcuser"] = self.rpc_user
            config["rpcpassword"] = self.rpc_password

        return config

    def getReleaseFilename(self, ctx: PrepareContext, arch_name: str) -> str:
        return f"dimecoin-{self.version}-{arch_name}.{ctx.file_ext}"

    def getReleaseUrl(self, ctx: PrepareContext, release_filename: str) -> str:
        return f"https://github.com/dime-coin/dimecoin/releases/download/v{self.version}{self.version_tag}/{release_filename}"

    def getAssertUrl(
        self,
        ctx: PrepareContext,
        os_name: str,
        os_dir_name: str,
        signing_key_name: str,
        use_guix: bool,
    ) -> str:
        return f"https://github.com/dime-coin/dimecoin/releases/download/v{self.version}{self.version_tag}/SHA256SUMS"

    def getExtractPath(
        self,
        ctx: PrepareContext,
        bin_name: str,
        release_path: str,
        extra_opts: dict,
    ) -> str:
        return f"dimecoin-{self.version}/bin/{bin_name}"

    def writeCoinConfig(
        self,
        ctx: PrepareContext,
        fp,
        chain: str,
        salt: str,
        settings: dict,
        extra_opts: dict,
    ) -> None:
        fp.write("prune=4000\n")
        fp.write("fallbackfee=0.0002\n")
        self.writeRpcAuth(fp, salt)


prepare_module = DIMEPrepare(
    name=params["name"],
    ticker=params["ticker"],
    version=DIME_VERSION,
    version_tag=DIME_VERSION_TAG,
    signers={},
    rpc_user=DIME_RPC_USER,
    rpc_password=DIME_RPC_PWD,
    onion_port=DIME_ONION_PORT,
)
