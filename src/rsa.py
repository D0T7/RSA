import secrets
import random
from math import lcm
from src.helper import RSA_HELPER


class RSA:
    def __gen_rsa_primes(self, bit_length):
        def is_prime(number, k=5):
            """
            Miller-Rabin primality test.
            Returns True if `number` is likely to be prime, False otherwise.
            The parameter `k` determines the accuracy of the test.
            """
            if number == 2 or number == 3:
                return True
            if number < 2 or number % 2 == 0:
                return False

            # Write (number - 1) as 2^r * d
            r, d = 0, number - 1
            while d % 2 == 0:
                r += 1
                d //= 2

            # Perform the Miller-Rabin test `k` times
            for _ in range(k):
                a = random.randint(2, number - 2)
                x = pow(a, d, number)
                if x == 1 or x == number - 1:
                    continue
                for _ in range(r - 1):
                    x = pow(x, 2, number)
                    if x == number - 1:
                        break
                else:
                    return False
            return True

        while True:
            number = secrets.randbits(bit_length)
            # Set the highest and lowest bits
            number |= (1 << bit_length - 1) | 1
            if is_prime(number):
                return number
        
    @staticmethod    
    def generate_keys(bit_length):
        rsa = RSA()
        p = rsa.__gen_rsa_primes(bit_length)
        q = rsa.__gen_rsa_primes(bit_length)

        # p = 61
        # q = 53
        # print(len(str(p)), len(str(q)))

        n = p * q
        # print(n)
        # print(len(str(n)))

        phi = lcm((p - 1), (q - 1))
        # print(phi)
        # print(len(str(phi)))

        e = 65537 if phi > 65337 else 16
        # while e < phi:
        #     if gcd(e, phi) == 1:
        #         break
        #     e += 1

        # print(e)

        # Find d such that d is the multiplicative inverse of e modulo phi
        d = RSA_HELPER.multiplicative_inverse(e, phi)
        # print(d)

        # d = 2
        # while True:
        #     if (d * e) % phi == 1:
        #         break
        #     d += 1

        # Return public and private keys
        public_key = (e, n)
        private_key = (d, n)

        return public_key, private_key

    @staticmethod
    def encrypt(plain_text, public_key):
        e, n = public_key
        encrypted_data = RSA_HELPER.modular_exponentiation(plain_text, e, n)
        return encrypted_data

    @staticmethod
    def decrypt(encrypted_data, private_key):
        d, n = private_key
        decrypted_data = RSA_HELPER.modular_exponentiation(encrypted_data, d, n)
        return decrypted_data


