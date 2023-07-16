#include <iostream>
#include <chrono>
#include <gmp.h>

bool is_prime(const mpz_t &number, int k = 5)
{
    if (mpz_cmp_ui(number, 2) == 0 || mpz_cmp_ui(number, 3) == 0)
        return true;
    if (mpz_cmp_ui(number, 2) < 0 || mpz_even_p(number) != 0)
        return false;

    mpz_t d;
    mpz_init(d);
    mpz_sub_ui(d, number, 1);

    int r = 0;
    while (mpz_even_p(d) != 0)
    {
        r += 1;
        mpz_divexact_ui(d, d, 2);
    }

    mpz_t a, x;
    mpz_inits(a, x, NULL);

    for (int i = 0; i < k; i++)
    {
        gmp_randstate_t state;
        gmp_randinit_default(state);

        mpz_urandomm(a, state, number);
        mpz_add_ui(a, a, 2);

        mpz_powm(x, a, d, number);
        if (mpz_cmp_ui(x, 1) == 0 || mpz_cmp(x, number - 1) == 0)
            continue;

        for (int j = 0; j < r - 1; j++)
        {
            mpz_powm_ui(x, x, 2, number);
            if (mpz_cmp(x, number - 1) == 0)
                break;
        }

        if (mpz_cmp(x, number - 1) != 0)
        {
            mpz_clears(d, a, x, NULL);
            return false;
        }
    }

    mpz_clears(d, a, x, NULL);
    return true;
}

void generate_large_prime(mpz_t &prime, int bit_length)
{
    gmp_randstate_t state;
    gmp_randinit_default(state);
    mpz_urandomb(prime, state, bit_length);

    while (!is_prime(prime))
    {
        mpz_nextprime(prime, prime);
    }

    gmp_randclear(state);
}

int main()
{
    auto start = std::chrono::high_resolution_clock::now();
    int bit_length = 4096; // Adjust the desired size of the prime number

    mpz_t prime;
    mpz_init(prime);
    generate_large_prime(prime, bit_length);

    std::cout << "Prime number: " << mpz_get_str(NULL, 10, prime) << std::endl;
    std::cout << "Number of digits: " << mpz_sizeinbase(prime, 10) << std::endl;

    mpz_clear(prime);

    auto end = std::chrono::high_resolution_clock::now();
    double duration = std::chrono::duration<double>(end - start).count();
    std::cout << "Time taken = " << std::fixed << duration << " seconds" << std::endl;

    return 0;
}
