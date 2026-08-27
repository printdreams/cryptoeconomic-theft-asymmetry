#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (a) 2026 Alex Breton

"""
Shamir's 2-of-2 Threshold Secret Sharing Implementation over GF(2^256).

This module provides finite field arithmetic over Galois Field GF(2^256)
and functions to split and reconstruct a 256-bit key using polynomial
evaluation and Lagrange interpolation (Shamir, 1979).
"""

import os

# Irreducible primitive polynomial for GF(2^256): x^256 + x^10 + x^5 + x^2 + 1
# 2^10 + 2^5 + 2^2 + 2^0 = 1061 = 0x425
POLYNOMIAL = (1 << 256) | 0x425


def gf_add(a: int, b: int) -> int:
    """Galois Field GF(2^256) addition (bitwise XOR)."""
    return a ^ b


def gf_mul(a: int, b: int) -> int:
    """Galois Field GF(2^256) multiplication using Russian Peasant algorithm."""
    p = 0
    for _ in range(256):
        if b & 1:
            p ^= a
        b >>= 1
        a <<= 1
        if a & (1 << 256):
            a ^= POLYNOMIAL
    return p


def gf_pow(base: int, exp: int) -> int:
    """Galois Field GF(2^256) exponentiation."""
    res = 1
    while exp > 0:
        if exp & 1:
            res = gf_mul(res, base)
        base = gf_mul(base, base)
        exp >>= 1
    return res


def gf_inv(a: int) -> int:
    """Galois Field GF(2^256) multiplicative inverse via Fermat's Little Theorem."""
    if a == 0:
        raise ValueError("Cannot invert zero in Galois Field.")
    return gf_pow(a, (1 << 256) - 2)


def split_secret_2_of_2(
    master_key_bytes: bytes,
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Splits a 256-bit master key K into two shares over GF(2^256) (Shamir, 1979)."""
    if len(master_key_bytes) != 32:
        raise ValueError("Master key must be exactly 32 bytes (256 bits).")

    K = int.from_bytes(master_key_bytes, byteorder="big")

    # Generate random degree-1 polynomial coefficient a1 from CSPRNG entropy
    a1 = int.from_bytes(os.urandom(32), byteorder="big")

    # f(x) = K + a1*x in GF(2^256)
    s1_y = gf_add(K, gf_mul(a1, 1))  # Share 1 at x=1
    s2_y = gf_add(K, gf_mul(a1, 2))  # Share 2 at x=2

    return ((1, s1_y), (2, s2_y))


def reconstruct_secret_2_of_2(
    share1: tuple[int, int], share2: tuple[int, int]
) -> bytes:
    """Reconstructs master key K via Lagrange interpolation at x=0 over GF(2^256)."""
    x1, y1 = share1
    x2, y2 = share2

    if x1 == x2:
        raise ValueError("Share evaluation points (x1, x2) must be distinct.")

    # Lagrange basis polynomials evaluated at x=0 in GF(2^256):
    # l1(0) = x2 / (x1 + x2),  l2(0) = x1 / (x1 + x2)
    denom = gf_add(x1, x2)
    inv_denom = gf_inv(denom)

    l1_0 = gf_mul(x2, inv_denom)
    l2_0 = gf_mul(x1, inv_denom)

    # K = (y1 * l1(0)) + (y2 * l2(0))
    term1 = gf_mul(y1, l1_0)
    term2 = gf_mul(y2, l2_0)
    K = gf_add(term1, term2)

    return K.to_bytes(32, byteorder="big")


def self_test() -> None:
    """Executes a self-test to verify mathematical correctness."""
    test_key = os.urandom(32)
    share1, share2 = split_secret_2_of_2(test_key)

    # Verify reconstruction
    recovered_key = reconstruct_secret_2_of_2(share1, share2)
    assert recovered_key == test_key, "Self-test failed: keys do not match!"

    # Verify single-share independence (corrupting share 2 produces incorrect key)
    corrupted_share2 = (2, gf_add(share2[1], 1))
    recovered_corrupted = reconstruct_secret_2_of_2(share1, corrupted_share2)
    assert (
        recovered_corrupted != test_key
    ), "Self-test failed: corrupted share produced original key!"

    print(
        "[+] Shamir GF(2^256) 2-of-2 secret sharing self-test passed successfully."
    )


if __name__ == "__main__":
    self_test()
