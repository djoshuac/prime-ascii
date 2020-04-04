from sympy import isprime
from itertools import combinations_with_replacement, chain
import numpy as np
from threading import Thread


def parse_template(filename):
    with open(filename) as file:
        chars = []
        for row in file:
            chars.append([
                # -1 indicates a position can be any digit
                -1 if c == ' ' else int(c)
                for c in row.strip()
                if row.strip() != ''
            ])
        return list(chain(*chars)), len(chars), len(chars[0])


def find_prime(template, parallel_strategy=(1, 0)):
    """
    Find prime numbers that match the given template.

    To enable multithreading, the parallel_strategy `(n, r)` splits up the work
    roughly evenly using the remainder of dividing a candiate prime by `n`.
    Specifically, this function skips all numbers c where `r != c % n`
    """
    n, r = parallel_strategy

    # verify the template is primable by checking the last digit
    l = template[-1]
    is_even = l % 2 == 0
    is_five = l == 5
    if is_even or is_five:
        raise Exception(
            'Do not waste your time. Last digit cannot be 5 or even'
        )

    # the indexes of the variable digits
    variables = [
        i
        for (i, d) in enumerate(template)
        if d == -1
    ]
    for digits in combinations_with_replacement(range(10), len(variables)):
        template = list(template)  # make a copy to allow mutation
        for i, d in zip(variables, digits):
            template[i] = d
        candidate = int(''.join(map(str, template)))
        if candidate % n != r:
            continue
        if isprime(candidate):
            yield template


def print_ascii(asc, out=print):
    for row in asc:
        out(''.join(map(str, row)))


def default_input(prompt, default):
    response = input(prompt)
    return default if response == '' else response


def file_writer(filename):
    file = open(filename, 'w')
    return lambda x: file.write(x + '\n')


def make_thread(template, nthreads, thread_number):
    out = file_writer(f'../tmp/work-{thread_number}')
    template = list(template)

    def target():
        print(f'Starting thread {thread_number}')
        for prime in find_prime(template, (nthreads, thread_number)):
            out(''.join(map(str, prime)))
        print(f'Thread {thread_number} finished')

    return Thread(
        name=f'Thread-{thread_number}',
        target=target
    )


if __name__ == '__main__':
    """
    Template example:

    11111 1
    11   23
    9 99999
    12312 7

    Spaces are variable digits
    """
    filename = default_input('Template filename: ', '../templates/demo.txt')
    nthreads = int(default_input('Number of threads: ', '1'))

    template, height, width = parse_template(filename)

    # find primes with multithreading
    # If you notice some primes have been found in the `tmp/work-x`
    # files, you can comment out these lines and rerun to print the
    # formatted results. Otherwise, you can wait a long time for them
    # to finish
    threads = [
        make_thread(template, nthreads, tx)
        for tx in range(nthreads)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # clean up tmp/work and print out primes
    primes = []
    for t in range(nthreads):
        with open(f'../tmp/work-{t}') as file:
            print(t)
            for prime in file.readlines():
                asc = np.array(list(map(int, prime.strip())))
                print(asc)
                asc.shape = (height, width)
                primes.append(asc)
    for prime in primes:
        print_ascii(prime)
        print()
