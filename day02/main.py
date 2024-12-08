from typing import List

from input import read_input


def extract_reports(file_name: str) -> List[List[int]]:
    input_text = read_input(file_name)
    reports = []

    for line in input_text.splitlines():
        levels = list(map(lambda s: int(s), line.split()))
        reports.append(levels)

    return reports


def is_safe(report: List[int]) -> bool:
    if len(report) == 1:
        return True
    assert len(report) > 1

    differences = [a - b for a, b in zip(report[:-1], report[1:])]
    is_decreasing = all(d > 0 for d in differences)
    is_increasing = all(d < 0 for d in differences)
    is_gradual = all(1 <= abs(d) <= 3 for d in differences)

    return is_gradual and (is_decreasing or is_increasing)


def is_almost_safe(report: List[int]) -> bool:
    if is_safe(report):
        return True

    # We can either remove every possible index and check for safety...
    return any([is_safe(report[:index] + report[index + 1 :]) for index in range(len(report))])

    # ... or find the only possible level pair that causes the unsafeness

    # differences = [a - b for a,b in zip(report[:-1], report[1:])]
    # num_decreasing = sum(d > 0 for d in differences)
    # num_increasing = sum(d < 0 for d in differences)
    # num_non_gradual = sum(abs(d) < 1 or abs(d) > 3 for d in  differences)
    #
    # is_almost_increasing = num_decreasing <= 1
    # is_almost_decreasing = num_increasing <= 1
    # is_almost_gradual = num_non_gradual <= 1
    #
    # if (not is_almost_gradual):
    #     return False
    #
    # if (not is_almost_increasing and not is_almost_decreasing):
    #     return False
    #
    # bad_idx = None
    # if (num_non_gradual == 1):
    #     bad_idx = [i for i, d in enumerate(differences) if abs(d) < 1 or abs(d) > 3][0]
    # elif (num_decreasing == 1):
    #     bad_idx = [i for i, d in enumerate(differences) if d > 0][0]
    # elif (num_increasing == 1):
    #     bad_idx = [i for i, d in enumerate(differences) if d < 0][0]
    #
    # assert(isinstance(bad_idx, int))
    #
    # # remove either the entry at index bad_idx or bad_idx + 1 (since their difference was unsafe
    # return is_safe(report[:bad_idx] + report[bad_idx+1:]) or is_safe(report[:bad_idx+1] + report[bad_idx+2:])


def calculate_num_safe(reports: List[List[int]]) -> int:
    return sum(map(is_safe, reports))


def calculate_num_almost_safe(reports: List[List[int]]) -> int:
    return sum(map(is_almost_safe, reports))


def part1(file_name: str) -> int:
    reports = extract_reports(file_name)
    return calculate_num_safe(reports)


def part2(file_name: str) -> int:
    reports = extract_reports(file_name)
    return calculate_num_almost_safe(reports)


if __name__ == '__main__':
    result1 = part1('puzzle.txt')
    print(f'Total number of safe reports: {result1}')

    result2 = part2('puzzle.txt')
    print(f'Total number of almost safe reports: {result2}')
