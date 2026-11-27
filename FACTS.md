# FACTS: sources for every checked claim (EN set)

c2pool source: `frstrtr/c2pool` master @ `58728c9fff378dbf89ae26904df01d41a0d56283` (2026-11-27 16:07 +04), latest release tag `v0.2.12.16` (2026-11-25).
Bitcoin Core source: tag `v28.1` unless stated. Paths below are relative to those trees.
Original pages: the Google Site https://sites.google.com/view/p2pool-scientific-basics/main and the `gh-pages` branch of `frstrtr/c2pool` @ `9d2e6c7` (https://frstrtr.github.io/c2pool/).

Legend: **C** = changed from the original text, **N** = new text, **K** = kept from the original and re-checked, **H** = kept as dated history, not re-verified.

## c2pool-today (N)
| Claim | Source |
|---|---|
| C++ reimplementation of p2pool, V36 share format, one binary per parent chain | README.md:6, 187 |
| Chain table (algorithms, merged children, status words) | README.md:189-197 |
| "Live" definition; only LTC and Dash in production | README.md:199-203 |
| DGB runs Scrypt as a standalone parent, not an AuxPoW child; mainnet only | README.md:194, 205 |
| BIP-110: SHA256d below 961640, BLAKE2b from it | README.md:154-157, 207 |
| Monero row quoted verbatim; "Mainnet pool mode is disabled in code" | README.md:197, 283-289 |
| LTC/DOGE embedded nodes: header sync over P2P, UTXO for fees, mempool, own templates | making-of (original), README.md:6-8; `src/impl/ltc/coin/` |
| Dash daemonless: P2P only, no RPC credentials, DML/LLMQ/ChainLocks/DIP-4 rebuilt, blocks accepted on mainnet, v24 rules from v0.2.11.1, `--coin-rpc` fallback | README.md:40-61; tag `v0.2.11.1` |
| Share version 3601 since 2026-11-13 00:00:00 UTC, flag day not vote, merged payout rule changed, several aux chains | README.md:321-327, 1005-1031; `src/impl/ltc/config_pool.hpp:79` (1794528000 = 2026-11-13T00:00:00Z); tag `v0.2.12.1` |
| Only v0.2.12.1+ on the LTC share chain; Python p2pool not | README.md:323-327 |
| Python p2pool-merged-v36 / p2pool-dash no longer maintained | README.md:38 |
| PPLNS exponential decay, half-life CHAIN_LENGTH/4, window 8640, 15 s share period (LTC) | `src/impl/ltc/share_tracker.hpp:2245`; `src/impl/ltc/config_pool.hpp:50-51` |
| Public nodes list | README.md:178-181, 872, 1639; live HTTP 200 on 2026-11-27 for all six hosts |
| Packages, macOS universal and 26.0+, SHA256SUMS, .asc from v0.2.7, key URL and fingerprint | README.md:400-438; release assets of `v0.2.12.16` |
| V37 is design and prototype stage, not production | README.md:211-215 |

## references (C)
| Claim | Source |
|---|---|
| Link states | checked with curl -L on 2026-11-27. 418/403 answers are bot blocks; those links are kept. |
| Authors named only where the URL or file name carries them (Zamyatin) | link URLs |
| TU Wien thesis: "Merged mining: analysis of effects and implications", Zamyatin, Alexei, 2017, thesis; DOI 10.34726/hss.2017.41136 | https://repositum.tuwien.at/handle/20.500.12708/5239 (record metadata, 2026-11-28) |
| popeller.io answered 503 on 2026-11-27 and 2026-11-28; under maintenance, expected back | HTTP check; maintainer notice |
| SegWit done; Taproot soft fork required; P2TR payout not supported (20-byte payout hash); MWEB carried forward, empty extension block | `src/impl/ltc/params.hpp:51`; README.md:913-916, 949-954; `src/impl/ltc/coin/mweb_builder.hpp:6-12` |

## making-of-c2pool (H with C notes)
| Note | Source |
|---|---|
| mk-u00 overview of chains today | README.md:6-11, 189-203 |
| mk-u40 ratchet complete, 3601 flag day, peers below 3601 disconnected | README.md:321-327, 1005-1031 |
| mk-u74 2160 shares ≈ 9 h at 15 s (LTC); 18 h at 30 s (BTC) | `src/impl/ltc/share_tracker.hpp:2245`; `src/impl/ltc/config_pool.hpp:50-51`; `src/impl/btc/config_pool.hpp:53` |
| mk-u96 LTC share period 15 s | `src/impl/ltc/config_pool.hpp:50` |
| mk-u97 emergency rule: 20 share periods, doubling per 10 periods, linear interpolation, then ±10% clamp | `src/impl/ltc/share_tracker.hpp:2013-2047, 2050-2075` |
| mk-113 luck sentence corrected (found ÷ expected); mk-u113 effort model since v0.2.12.9 | `src/core/pool_luck.hpp:17-22`; README.md:28 (v0.2.12.9) |
| mk-118 "on our LAN" → "only between our test machines" (privacy rule) | editorial |
| mk-u125 `ui/c2pool-qt`, `ui/c2wallet-qt`, offline signer with no network code | `ui/`; README.md:142-143 |
| mk-u126 DGB live daemonless mainnet, standalone Scrypt parent, no testnet | README.md:194, 205 |
| mk-u127 Python p2pool off the LTC chain since 3601 | README.md:321-327 |
| mk-128 V37 box reworded: credit by target met; V37 design/prototype stage | README.md:211-215; paper §5 |
| mk-80 "contiguous std::deque" → std::deque (not contiguous) | `src/impl/ltc/share_tracker.hpp:331` (`std::deque<PPLNSEntry> m_entries`) |
| mk-87 the CHECKMULTISIG dummy is supplied by the spender; NULLDUMMY requires it empty | BIP 147 |
| mk-101 HogEx = "Hogwarts Express", the MWEB integration transaction | LIP-0003 (litecoin-project/lips, lip-0003.mediawiki:199) |
| mk-124 Litecoin retargets every 2016 blocks; Dogecoin at every block since DigiShield | `src/impl/ltc/coin/header_chain.hpp:186-189`; `src/impl/doge/coin/chain_params.hpp:6-30` |
| mk-u96 a ±10% clamp doubles the target in ≈ 7.3 shares and triples it in ≈ 11.5; the original "23 shares" is kept as written | arithmetic: ln 2 / ln 1.1, ln 3 / ln 1.1 |
| mk-u74 names both chains (LTC, BTC) | as above |
| wm-05 weights decide approval (contradiction with wm-upd removed) | editorial |
| mk-u93 1 MH/s on 90 GH/s at 15 s per share ≈ 15.6 days per share | arithmetic; `src/impl/ltc/config_pool.hpp:50` |
| Everything else (GENTX counts, timings, test topology, 12 address cases, OOM figures) | **H**: the original authors' June 2026 account, not re-verified |

## luck (K + N)
| Claim | Source |
|---|---|
| Folklore sections | **K** as published |
| lk-30 reworded: overshoot is not paid; a pool paying by it would overpay one hash | consistency with real-difficulty rd-19 |
| Pr[R ≥ r] = 1/r; median 2 | standard result: for a uniform hash below target T, Pr[hash ≤ T/r] = 1/r |
| "lonely tower at block ~1,450, R ≈ 7,000" | **H**: from the original chart data, not re-verified |
| Dashboard model: Poisson, λ = H/(D·2^32), effort = ∫λ dt, per-block luck 100/effort never averaged, ~450% with 30 blocks, period luck k/Σeffort with exact Poisson 95% interval | `src/core/pool_luck.hpp:7-22` |
| Exp(1): mean 1, median 0.69 | `web-static/dashboard.html:8833-8835` |
| Gross rate H = nonstale/(1 − stale_prop); sampled once a minute; partial coverage handling | `src/core/pool_luck.hpp:24-41` |
| Rounds from previous main-chain block; orphan never ends a round | `src/core/pool_luck.hpp:43-45` |
| Tags ⚡ < 1/3, ⚡⚡ < 0.1, 🐢 > 2, 🐢🐢 > 3 | `web-static/dashboard.html:8854` |
| Display only | `src/core/pool_luck.hpp:4-5` |

## real-difficulty (C)
| Claim | Source |
|---|---|
| nBits = 1-byte exponent + 3-byte mantissa; target = m·2^(8(e−3)) | Bitcoin Core `src/arith_uint256.cpp` SetCompact; c2pool `SetCompact` use `src/impl/ltc/coin/header_chain.hpp:211` |
| Genesis nBits 0x1d00ffff → 0xffff·2^208, difficulty-1 target | Bitcoin genesis header; `POW_LIMIT` check in the difficulty-adjustment code test (below) |
| ≈ D·2^32 hashes per block | 2^256 / (0xffff·2^208 / D) ≈ D·2^32 |
| PoW function table | README.md:189-197, 205-207 |
| Best share is an achieved difficulty | `web-static/dashboard.html:3896-3903` |
| Charts | **K** images from `gh-pages` `img/`, provenance as stated by the original authors |
| V37 box last paragraph aligned with paper §5 and §8 (count hashes at the lower target; overshoot not needed) | paper §5, §8 (frstrtr.github.io/c2pool, `gh-pages` @ `9d2e6c7`) |

## difficulty-adjustment (C)
| Claim | Source |
|---|---|
| Retarget uses nTime of last and of the block 2015 earlier | Bitcoin Core `src/pow.cpp:40-46, 55` |
| Clamp [T/4, 4T] | `src/pow.cpp:56-59` |
| new target = old · actual / T; capped at pow limit | `src/pow.cpp:77-78` (+ cap below) |
| MTP = median of 11; not a header field | `src/chain.h:276-281` |
| time-too-old rule | `src/validation.cpp:4183-4184` |
| BIP 113 locktime uses MTP | `src/validation.cpp:4224-4233` |
| Code example reproduces nBits 0x1d00d86a at height 32,256 (difficulty ≈ 1.18) | run locally with timestamps 1261130161 (block 30240) and 1262152739 (block 32255). Timestamps and the result match block data (blocks 30,240, 32,255 and 32,256). |
| MTP RPC example | **K** original code, correct as written |
| LTC 2.5 min, 3.5 days, 2016 blocks, full-interval lookback after the first period (Art Forz) | c2pool `src/impl/ltc/coin/header_chain.hpp:184-189, 276-291` |
| DOGE 4 h window (240 blocks) to 145,000, DigiShield from 145,000, AuxPoW from 371,337 | c2pool `src/impl/doge/coin/chain_params.hpp:6-37`; `src/impl/doge/coin/template_builder.hpp:183-198` |
| Share target from pool rate and share period; ±10% clamp; emergency rule | c2pool `src/impl/ltc/share_tracker.hpp:1975-2075`; `config_pool.hpp:50`; `src/impl/btc/config_pool.hpp:53` |
| da-25 ASERT walks no window but still depends on the latest timestamp | aserti3-2d definition |
| BCH uses an absolute schedule (ASERT) since November 2020 | c2pool `src/impl/bch/config_pool.hpp:27`; aserti3-2d upgrade of 15 November 2020 |

## taproot-coinbase (K + C + N)
| Claim | Source |
|---|---|
| Body sections | **K** as published, light fixes: x-only key `OP_1 <32 bytes>` (BIP 341), empty scriptSig reason |
| tr-41u output key public from mining; internal key and unused leaves private; MuSig2 | BIP 341, BIP 327 |
| tr-49u no addresses at protocol level; unspendable outputs valid | consensus: outputs carry scripts, not addresses |
| tr-c3 Taproot soft fork required | `src/impl/ltc/params.hpp:51` |
| tr-c3 P2TR/P2WSH LTC address cannot be carried by a V36 share (20-byte hash); payout redistributed; dashboard text | README.md:949-954 |
| tr-c3 DOGE payout from the LTC key (P2PKH/P2WPKH → P2PKH, P2SH → P2SH) unless an explicit DOGE address is given | README.md:913-925; `src/impl/ltc/share_check.hpp:850-895` |
| tr-61 owed-ledger remedy withdrawn; §9 withdrawn; no revised §9 | paper errata (frstrtr.github.io/c2pool); `src/sharechain/v37/PURPLE-PAPER.md:8, 56-58` |

## weighted-multisig (C)
| Claim | Source |
|---|---|
| OP_CHECKMULTISIG / OP_CHECKSIGADD count one per signature | BIP 342; Bitcoin script semantics |
| Weighted-sum script with A=5, B=3, C=2, threshold 6 | hand-checked stack trace (witness sig_C sig_B sig_A, Alice on top; OP_SWAP brings each next signature up). Checked against `src/script/interpreter.cpp` (v28.1) for all 8 signer sets: only A+B, A+C and A+B+C pass; each run ends on one stack element. |
| Empty signature → false; invalid non-empty → fail (BIP 342 consensus in tapscript; NULLFAIL policy for P2WSH) | BIP 342; Bitcoin Core policy `SCRIPT_VERIFY_NULLFAIL` |
| Box: p2pool/c2pool coinbase pays miners directly; no pooled funds; §15 Incentive | p2pool design; paper §15 |

## bitcoin-leveldb (C, rewritten)
| Claim | Source |
|---|---|
| Original text came from Bitcoin Stack Exchange answer 29418 (Pieter Wuille, CC BY-SA 4.0); the parser derived from answer 123610 (CC BY-SA 4.0) | https://bitcoin.stackexchange.com/a/29418 and https://bitcoin.stackexchange.com/questions/28168 (Stack Exchange API; text similarity 0.62, opening paragraphs verbatim) |
| Block index keys b, f, l, R, F | `src/node/blockstorage.cpp:44-48` |
| txindex in its own DB since 0.17 | Bitcoin Core 0.17.0 release notes, lines 27, 351-354 |
| Chainstate keys C, B, H (and legacy c) | `src/txdb.cpp:22-26` |
| Chainstate obfuscated; key `\000obfuscate_key` (serialized with length byte 0x0e) | `src/validation.cpp:1975`; `src/dbwrapper.cpp:258-269, 323` |
| Record layout: varints (version, height, status, nTx, file, data pos, undo pos) then header | `src/chain.h:377-397` |
| VARINT read/write | `src/serialize.h:388-389, 432-443`; code tested: round-trip 0…10^9, 128 → 80 00, 65535 → 82 fe 7f |
| Parser output on the block-80,000 record (height, nTx 2, bits 0x1b5bede6, hash 000000000043a8c0…93baf6 recomputed from the header) | run locally |
| blk*.dat: magic, size, block; XOR with `blocks/xor.dat` from 28.0, only on a fresh blocks dir; `-blocksxor` | `doc/release-notes/release-notes-28.0.md:269-271`; `src/node/blockstorage.cpp:1148-1173` |
| Charts made by reading blk00000.dat | **H**: provenance as stated by the original authors |

## purple-paper (N)
| Claim | Source |
|---|---|
| Canonical copy, MIT, © frstrtr | frstrtr.github.io/c2pool/ (`gh-pages` @ 9d2e6c7) |
| Errata text and section summaries | frstrtr.github.io/c2pool (`gh-pages` @ `9d2e6c7`) |
| No revised §9 published | `src/sharechain/v37/PURPLE-PAPER.md:8, 56-58`, last commit 3a413d581 (2026-10-04) |
| §4/§6 window is not the current Monero lane | README.md:236-241 (Path B); paper §4 |

## monero-ccs (N)
| Claim | Source |
|---|---|
| Gist title, date 2026-09-19 19:25Z, summary line | https://gist.github.com/SChernykh/636eca0b73181277ea85401b6b1e24ba (GitHub gist API: created_at), `c2pool-payout-review.md:1-5` |
| SChernykh is the author of Monero's P2Pool | `docs/xmr-lane/PROVENANCE.md:143-144` (c2pool tree) |
| MR !699 title, opened 2026-09-25T06:30:41Z, closed 2026-10-04T13:37:01Z | https://repo.getmonero.org/monero-project/ccs-proposals/-/merge_requests/699 (GitLab API: created_at, closed_at) |
| Closing comment verbatim | https://repo.getmonero.org/monero-project/ccs-proposals/-/merge_requests/699#note_37517 |
| Gist comments: times, authors, quoted sentences | GitHub gist comments API (ids 6394929, 6402841, 6405381, 6406006, 6406115, 6406130) |
| 3.94×, 0.47 of 0.6 instead of 0.12; anchor 61 heights; hopper 1.312 vs 1.000 | comment 6406006 |
| IRC discussion 2026-10-03 | https://libera.monerologs.net/monero-community/20261003 |
| Status line | README.md:290-292 (verbatim) |
| Monero lane quote | README.md:197, 283-289 |

## Corrections after the fact check of 2026-11-27
| Block | Source |
|---|---|
| mk-u38 thresholds count shares; work weighting only in the tail guard | `src/impl/ltc/auto_ratchet.hpp` (vote_pct, tail-work condition); p2pool-merged-v36 |
| mk-u44 each share is verified by its own version (v36_active = VERSION ≥ 36) | `src/impl/ltc/share_check.hpp:2069-2074`; p2pool `data.py:1519` |
| mk-u45 CONFIRMED ~100 shares early, 24,000+ GENTX failures overnight | c2pool commit `a5f17c4e58` (31 March 2026) |
| mk-u57 a found LTC block is sent full (HogEx, no room in compact block v2) | c2pool #2144 and the LTC block relay code |
| mk-u102 `--ltc-mweb-ext litecoind`; default none | `src/c2pool/main_ltc.cpp:680, 1028, 1406` |
| mk-u39 July 2026 false-activation modes guarded; class not claimed closed | README.md:299-308 |
| mk-98 whale departure: below 50% of the 30-minute average, easiest target the clamp allows, non-consensus | `src/impl/ltc/whale_departure.hpp:4-18` |
| mk-08 "the script types" (no interpreter in src/btclibs) | `src/btclibs/` |
| da-23 example runs (getblockheader nTime; tip height ≥ 10) | run locally against a stub RPC |
| da-42 the emergency rule comes from p2pool V36 | `src/impl/ltc/share_tracker.hpp:2013-2014` |
| da-25 a window retarget depends on the timestamps at its two ends | Bitcoin Core `src/pow.cpp:39-43` |
| wm-19 small donation output to a fixed script beside the miners' outputs | README.md:308-320 (donation script) |
| tr-c3 redistribution target depends on the `--redistribute` mode | README.md:939-946; `src/core/stratum_server.cpp:1372-1384`; `src/core/web_server.cpp:503-548` |
| ld-12 v28.1 refuses a chainstate in the old 'c' format (`-reindex-chainstate`) | Bitcoin Core `src/node/chainstate.cpp:119-124`, `src/txdb.cpp:28-35` |
| ld-24 the block index record holds header, positions and status | Bitcoin Core `src/chain.h:377-388` |
| lk-dash-01 since v0.2.12.9 | README.md:28 |
| lk-30 block 1,430, R = 6,989 over the first 4,032 hashes | recomputed from block hashes |

## Open items
1. Hand-check in a browser: Medium links, the lists.linuxfoundation.org archive links, diyhpl.us transcripts (all refuse automated clients).
2. Find the current home of the gnusha.org #bitcoin-wizards logs; re-check popeller.io after its maintenance.
3. The `gh-pages` copy of the LevelDB article still carries the Stack Exchange text under "© technocore.one, all rights reserved".
