from math import ceil
from itertools import islice
from bisect import bisect_left


# String is a Smarandache-Wellin number
# The nth SWN s is such that s = concat(2...n-1th prime, nth prime)
# Find the nth SWN for the given length that is inclusive of the index
# Then, lazily generate the necessary amount of primes for
# the next five digits after the index and concatinate them together
# Then, grab the five digits that correspond to the index


# Helper functions

# Gets the closest member of a list, rounding down,
# for a given number, using bisect
def take_closest_rd(in_list, num):
    pos = bisect_left(in_list, num)
    if pos == 0:
        return in_list[0]
    if pos == len(in_list):
        return in_list[-1]
    return in_list[pos - 1]


# Same as above, without the rounding down
def take_closest(in_list, num):
    pos = bisect_left(in_list, num)
    if pos == 0:
        return in_list[0]
    if pos == len(in_list):
        return in_list[-1]
    before = in_list[pos - 1]
    after = in_list[pos]
    if after - num < num - before:
        return after
    else:
        return before


def concat_list(list):
    concat_list = ''.join(map(str, list))
    return concat_list


# Prime-related functions

# Yield arbitrary amount of primes
# using a version of the Sieve of Eratosthenes
# as a generator
def unbounded_sieve():
    counters = {}
    yield 2
    p = 3
    while True:
        while p in counters:
            for step in counters[p]:
                counters.setdefault(p + 2 * step, []).append(step)
            del counters[p]
            p += 2
        yield p
        counters[p * p] = [p]
        p += 2


# Get the nth prime number from the unbounded_sieve generator
def get_prime(n):
    primes = unbounded_sieve()
    if n == 0:
        index = 0
    else:
        index = n - 1
    nth_prime = next(islice(primes, index, None))
    return nth_prime


# Return the int length of the nth prime
# Uses OEIS A006880 as bounds for length of
# nth prime
def lenprime(n):
    if 0 <= n <= 4:
        length = 1
    elif 4 < n <= 25:
        length = 2
    elif 25 < n <= 168:
        length = 3
    elif 168 < n <= 1229:
        length = 4
    elif 1229 < n <= 9592:
        length = 5
    else:
        raise ValueError
    return length


# Determine the necessary amount of primes
# After the nth prime to get five digits,
# given any index on the nth prime
def get_neccessary_prime_amount(n):
    length = lenprime(n)
    if length < 4:
        return 6 - length
    elif length == 4:
        return 3
    else:
        return 2


# Creates the next few numbers in the sequence after the nth prime
# Since we already have the nth SWN, we can just calculate the nth, nth + 1,
# nth + 2, etc primes until we have five digits after the necessary index
def create_next_numbers(nth_prime):
    spread = get_neccessary_prime_amount(nth_prime) + 1
    primes = []
    for n in range(nth_prime, nth_prime + spread):
        primes.append(get_prime(n))
    concat = concat_list(primes)
    return concat


# Smarandache-Wellin number-related functions

# Length of the nth SWN
# For the nth SWN, given the set of
# number of primes P with at most m digits where m
# is the index of the set, the length is as follows:
# For P[m-1] < n <= P[m]:
# L(n) = L(P[m-1]) + m(n - P[m-1])
# I hardcoded the bounds bc for very large n
# the iterative method is 23x slower for n = 1000
def swn_length(n):
    if n == 0:
        length = 0
    elif 0 < n <= 4:
        length = n
    elif 4 < n <= 25:
        length = 4 + 2 * (n - 4)
    elif 25 < n <= 168:
        length = 46 + 3 * (n - 25)
    elif 168 < n <= 1229:
        length = 475 + 4 * (n - 168)
    elif 1229 < n <= 9592:
        length = 4719 + 5 * (n - 1229)
    else:
        raise ValueError
    return length

# Iterative method:
# This list is sequence A006880 in the OEIS
# a006880 = [0, 4, 25, 168, 1229, 9592, 78498, 664579, 5761455, 50847534, 455052511, 4118054813, 37607912018, 346065536839, 3204941750802, 29844570422669, 279238341033925, 2623557157654233, 24739954287740860, 234057667276344607, 2220819602560918840, 21127269486018731928, 201467286689315906290]

# The iterative method more clearly shows the generalized formula for the
# length of an SWN...but as mentioned is subopitmal


# def swn_length_iterative(n):
#     length = None
#     for index in range(0, len(a006880) - 1):
#         if n == 0:
#             length = 0
#         if a006880[index - 1] < n <= a006880[index]:
#             length = swn_length_iterative(a006880[index - 1]) + index * (n - a006880[index -1])
#             break
#         else:
#             continue
#
#     return length


# Gives a best guess as to the nth SWN given an estimated SWN length l
# Solves for length for each case of the SWN formula
# There are some cases of length for which there is no integer n
# We handle those in the nth_from_index function
def check_length(length):
    if length == 0:
        n = 0
    elif 0 < length <= 4:
        n = length
    elif 4 < length <= 46:
        n = (length + 4) / 2
    elif 46 < length <= 475:
        n = (length + 29) / 3
    elif 475 < length <= 4719:
        n = (length + 197) / 4
    elif 4719 < length <= 46534:
        n = (length + 1426) / 5
    return n


# Determines the closest valid SWN for a given index
# Also returns the drift/delta from end of that SWN
# And the index
def nth_from_index(string_index):
    poss_n = check_length(string_index)
    if swn_length(poss_n) == string_index:
        prime_start = poss_n
        init_position = 0
    else:
        spread = get_neccessary_prime_amount(poss_n)
        delta = int(ceil(spread / 2.0))
        lower_bound = poss_n - delta
        upper_bound = poss_n + delta + 1
        prime_dict = {}
        for m in range(lower_bound, upper_bound):
            prime_dict[swn_length(m)] = m
        prime_index = take_closest_rd(
            sorted(list(prime_dict.keys())), string_index)
        prime_start = prime_dict.get(prime_index)
        init_position = string_index - prime_index

    length = lenprime(poss_n)
    position = init_position + length - 1

    return prime_start, position


# Main program

def get_id_number(concated_primes, position):
    sliced_list = list(islice(concated_primes, position + 1, position + 6))
    return concat_list(sliced_list)


def solution(index):
    prime_start, position = nth_from_index(index)
    next_numbers = create_next_numbers(prime_start)
    id_number = get_id_number(next_numbers, position)
    return id_number
