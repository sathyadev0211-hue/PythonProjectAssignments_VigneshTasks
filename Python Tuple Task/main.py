"""
Task - 4: Python List Problems
Author: Student
Description: Solutions to 10 Python list and number problems.
"""

# ============================================================
# Task 1: Separate Even and Odd numbers from a list
# ============================================================

def separate_even_odd(numbers):
    """Separate even and odd numbers into two separate lists."""
    even_list = [num for num in numbers if num % 2 == 0]
    odd_list = [num for num in numbers if num % 2 != 0]
    return even_list, odd_list

numbers = [10, 501, 22, 37, 100, 999, 87, 351]
even_numbers, odd_numbers = separate_even_odd(numbers)
print("Task 1:")
print(f"  Original List : {numbers}")
print(f"  Even Numbers  : {even_numbers}")
print(f"  Odd Numbers   : {odd_numbers}")
print()


# ============================================================
# Task 2: Count and collect Prime Numbers from a list
# ============================================================

def is_prime(n):
    """Check whether a given number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_prime_numbers(numbers):
    """Return a list of prime numbers from the given list."""
    return [num for num in numbers if is_prime(num)]

numbers = [10, 501, 22, 37, 100, 999, 87, 351]
prime_numbers = get_prime_numbers(numbers)
print("Task 2:")
print(f"  Original List  : {numbers}")
print(f"  Prime Numbers  : {prime_numbers}")
print(f"  Count of Primes: {len(prime_numbers)}")
print()


# ============================================================
# Task 3: Find Happy Numbers in a list
# ============================================================

def is_happy(n):
    """Check whether a number is a Happy Number."""
    seen = set()
    while n != 1:
        if n in seen:
            return False
        seen.add(n)
        n = sum(int(digit) ** 2 for digit in str(n))
    return True

def get_happy_numbers(numbers):
    """Return a list of happy numbers from the given list."""
    return [num for num in numbers if is_happy(num)]

numbers = [10, 501, 22, 37, 100, 999, 87, 351]
happy_numbers = get_happy_numbers(numbers)
print("Task 3:")
print(f"  Original List  : {numbers}")
print(f"  Happy Numbers  : {happy_numbers}")
print(f"  Count          : {len(happy_numbers)}")
print()


# ============================================================
# Task 4: Sum of first and last digit of an integer
# ============================================================

def sum_first_last_digit(n):
    """Find the sum of the first and last digit of an integer."""
    n_str = str(abs(n))  # Use abs to handle negative numbers
    first_digit = int(n_str[0])
    last_digit = int(n_str[-1])
    return first_digit + last_digit

number = 12345
result = sum_first_last_digit(number)
print("Task 4:")
print(f"  Number         : {number}")
print(f"  First Digit    : {str(abs(number))[0]}")
print(f"  Last Digit     : {str(abs(number))[-1]}")
print(f"  Sum            : {result}")
print()


# ============================================================
# Task 5: Find all ways to make Rs. 10 using Rs. 1, 2, 5, 10
# ============================================================

def coin_combinations(target, coins):
    """Find all combinations of coins that sum to the target amount."""
    combinations = []

    def backtrack(remaining, current_combo, start_index):
        """Recursively build combinations using backtracking."""
        if remaining == 0:
            combinations.append(list(current_combo))
            return
        for i in range(start_index, len(coins)):
            if coins[i] <= remaining:
                current_combo.append(coins[i])
                backtrack(remaining - coins[i], current_combo, i)
                current_combo.pop()

    backtrack(target, [], 0)
    return combinations

target_amount = 10
coin_denominations = [1, 2, 5, 10]
all_combinations = coin_combinations(target_amount, coin_denominations)
print("Task 5:")
print(f"  Target Amount  : Rs. {target_amount}")
print(f"  Coins Available: {coin_denominations}")
print(f"  Total Ways     : {len(all_combinations)}")
print("  Combinations:")
for combo in all_combinations:
    print(f"    {combo}")
print()


# ============================================================
# Task 6: Find duplicates across three lists
# ============================================================

def find_duplicates_in_three_lists(list1, list2, list3):
    """Find all elements that appear in more than one of the three lists."""
    set1, set2, set3 = set(list1), set(list2), set(list3)
    # Elements common in at least two lists
    duplicates = (set1 & set2) | (set1 & set3) | (set2 & set3)
    return sorted(duplicates)

list_a = [1, 2, 3, 4, 5]
list_b = [3, 4, 5, 6, 7]
list_c = [5, 6, 7, 8, 9]
duplicates = find_duplicates_in_three_lists(list_a, list_b, list_c)
print("Task 6:")
print(f"  List 1     : {list_a}")
print(f"  List 2     : {list_b}")
print(f"  List 3     : {list_c}")
print(f"  Duplicates : {duplicates}")
print()


# ============================================================
# Task 7: Find the first non-repeating element in a list
# ============================================================

def first_non_repeating(numbers):
    """Find the first element that does not repeat in the list."""
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    for num in numbers:
        if frequency[num] == 1:
            return num
    return None  # All elements repeat

int_list = [4, 5, 1, 2, 0, 4, 5, 2, 1, 3]
result = first_non_repeating(int_list)
print("Task 7:")
print(f"  List                      : {int_list}")
print(f"  First Non-Repeating Element: {result}")
print()


# ============================================================
# Task 8: Find minimum element in a rotated and sorted list
# ============================================================

def find_min_in_rotated_sorted(numbers):
    """Find the minimum element in a rotated sorted list using binary search."""
    left, right = 0, len(numbers) - 1

    # If list is not rotated or has one element
    if numbers[left] <= numbers[right]:
        return numbers[left]

    while left < right:
        mid = (left + right) // 2
        if numbers[mid] > numbers[right]:
            left = mid + 1
        else:
            right = mid

    return numbers[left]

rotated_list = [4, 5, 6, 7, 0, 1, 2]
minimum = find_min_in_rotated_sorted(rotated_list)
print("Task 8:")
print(f"  Rotated Sorted List: {rotated_list}")
print(f"  Minimum Element    : {minimum}")
print()


# ============================================================
# Task 9: Find a triplet in a list whose sum equals a given value
# ============================================================

def find_triplet_with_sum(numbers, target):
    """Find a triplet in the list whose sum equals the target value."""
    n = len(numbers)
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if numbers[i] + numbers[j] + numbers[k] == target:
                    return (numbers[i], numbers[j], numbers[k])
    return None

triplet_list = [10, 20, 30, 9]
target_sum = 59
triplet = find_triplet_with_sum(triplet_list, target_sum)
print("Task 9:")
print(f"  List        : {triplet_list}")
print(f"  Target Sum  : {target_sum}")
print(f"  Triplet Found: {triplet}")
print()


# ============================================================
# Task 10: Check if a sub-list with sum equal to Zero exists
# ============================================================

def has_zero_sum_sublist(numbers):
    """Check if there exists a sub-list (subarray) with sum equal to zero."""
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)  # Base case: empty subarray

    for num in numbers:
        prefix_sum += num
        if prefix_sum in seen_sums:
            return True
        seen_sums.add(prefix_sum)

    return False

zero_sum_list = [4, 2, -3, 1, 6]
result = has_zero_sum_sublist(zero_sum_list)
print("Task 10:")
print(f"  List                          : {zero_sum_list}")
print(f"  Sub-list with Zero Sum Exists : {result}")
print()
