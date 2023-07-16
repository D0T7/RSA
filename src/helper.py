from math import gcd


class RSA_HELPER:

    @staticmethod
    def multiplicative_inverse(a, m):
        if gcd(a, m) != 1:
            return None  # The modular inverse doesn't exist
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (
                (u1 - q * v1),
                (u2 - q * v2),
                (u3 - q * v3),
                v1,
                v2,
                v3,
            )

        return u1 % m

    @staticmethod
    def modular_exponentiation(base, exponent, modulus):
        result = 1
        base = base % modulus

        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            base = (base * base) % modulus
            exponent = exponent // 2

        return result
