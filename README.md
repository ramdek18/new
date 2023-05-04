# chia-blockchain

[![Chia Network logo](https://www.chia.net/wp-content/uploads/2022/09/chia-logo.svg "Chia logo")](https://www.chia.net/)

| Latest Release | Latest Pre-release |
|         :---:          |          :---:         |
| ![GitHub Latest Rlease)](https://img.shields.io/github/v/release/Chia-Network/chia-blockchain?&label=release&logo=github) | ![GitHub Latest Pre-Release)](https://img.shields.io/github/v/release/Chia-Network/chia-blockchain?include_prereleases&label=pre-release&logo=github) |

![GitHub commit activity](https://img.shields.io/github/commit-activity/w/Chia-Network/chia-blockchain?logo=GitHub)

![GitHub all releases](https://img.shields.io/github/downloads/Chia-Network/chia-blockchain/total?logo=GitHub)

![GitHub contributors](https://img.shields.io/github/contributors/Chia-Network/chia-blockchain?logo=GitHub)

[![YouTube](https://img.shields.io/badge/subscribers-8.78k-red?logo=youtube&style=flat)](https://www.youtube.com/@Chia-Network)

[![Chia Discord](https://dcbadge.vercel.app/api/server/chia?style=flat&theme=full-presence)](https://discord.gg/chia)

<!-- ![Discord Shield](https://discordapp.com/api/guilds/1034523881404370984/widget.png?style=shield)

[![Discord](https://img.shields.io/discord/1034523881404370984.svg?label=Discord&logo=discord&colorB=1e2b2f)](https://discord.gg/chia) -->

Chia is a modern cryptocurrency built from scratch, designed to be efficient, decentralized, and secure. Here are some of the features and benefits:
* [Proof of space and time](https://docs.google.com/document/d/1tmRIb7lgi4QfKkNaxuKOBHRmwbVlGL4f7EsBDr_5xZE/edit) based consensus which allows anyone to farm with commodity hardware
* Very easy to use full node and farmer GUI and cli (thousands of nodes active on mainnet)
* [Chia seeder](https://github.com/Chia-Network/chia-blockchain/wiki/Chia-Seeder-User-Guide), which maintains a list of reliable nodes within the Chia network via a built-in DNS server.
* Simplified UTXO based transaction model, with small on-chain state
* Lisp-style Turing-complete functional [programming language](https://chialisp.com/) for money related use cases
* BLS keys and aggregate signatures (only one signature per block)
* [Pooling protocol](https://github.com/Chia-Network/chia-blockchain/wiki/Pooling-User-Guide) that allows farmers to have control of making blocks
* Support for light clients with fast, objective syncing
* A growing community of farmers and developers around the world

Please check out the [Chia website](https://www.chia.net/), the [wiki](https://github.com/Chia-Network/chia-blockchain/wiki), and [FAQ](https://github.com/Chia-Network/chia-blockchain/wiki/FAQ) for
information on this project.

Python 3.7+ is required. Make sure your default python version is >=3.7
by typing `python3`.

If you are behind a NAT, it can be difficult for peers outside your subnet to
reach you when they start up. You can enable
[UPnP](https://www.homenethowto.com/ports-and-nat/upnp-automatic-port-forward/)
on your router or add a NAT (for IPv4 but not IPv6) and firewall rules to allow
TCP port 8444 access to your peer.
These methods tend to be router make/model specific.

Most users should only install harvesters, farmers, plotter, full nodes, and wallets.
Setting up a seeder is best left to more advanced users.
Building Timelords and VDFs is for sophisticated users, in most environments.
Chia Network and additional volunteers are running sufficient Timelords
for consensus.

## Installing

Install instructions are available in the
[INSTALL](https://github.com/Chia-Network/chia-blockchain/wiki/INSTALL)
section of the
[chia-blockchain repository wiki](https://github.com/Chia-Network/chia-blockchain/wiki).

## Running

Once installed, a
[Quick Start Guide](https://github.com/Chia-Network/chia-blockchain/wiki/Quick-Start-Guide)
is available from the repository
[wiki](https://github.com/Chia-Network/chia-blockchain/wiki).
