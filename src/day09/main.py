import copy
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from input import read_input

from template import Day


def extract_file_blocks(file_path: Path) -> List[Optional[int]]:
    """Returns a list with the corresponding file block ID at each position, or None if disk space is free"""
    input_text = read_input(file_path)
    assert len(input_text.splitlines()) == 1
    line = input_text.splitlines()[0]

    total_disk_space = sum([int(char) for char in line])
    disk = [None] * total_disk_space

    cur_pos = 0
    for pos, char in enumerate(line):
        block_len = int(char)
        if pos % 2 == 1:
            cur_pos += block_len
            continue

        disk[cur_pos : cur_pos + block_len] = [pos // 2] * block_len
        cur_pos += block_len

    return disk


def rearrange_blocks(disk: List[Optional[int]]) -> List[Optional[int]]:
    ordered = copy.deepcopy(disk)
    first_pointer = 0
    last_pointer = len(disk) - 1

    while first_pointer < last_pointer:
        if ordered[first_pointer] is not None:
            first_pointer += 1
            continue
        if ordered[last_pointer] is None:
            last_pointer -= 1
            continue

        assert first_pointer < last_pointer
        assert ordered[first_pointer] is None
        assert ordered[last_pointer] is not None

        ordered[first_pointer] = ordered[last_pointer]
        ordered[last_pointer] = None

    return ordered


def rearrange_files(disk: List[Optional[int]]) -> Dict[int, Tuple[int, int]]:
    def find_insert_pos(
        cur_pos: int, length: int, spans: Dict[int, Tuple[int, int]]
    ) -> Optional[int]:
        sorted_starts = sorted(spans.values(), key=lambda val: val[0])

        last_end = 0
        for start, end in sorted_starts:
            if start > cur_pos:
                return None

            free_space = start - last_end - 1
            if free_space >= length:
                return last_end + 1
            last_end = end

    # Compute a dict from file_id to (start_pos, end_pos)
    spans = dict()

    cur_id = None
    for pos, id in enumerate(disk):
        if id is None:
            cur_id = None
            continue

        if cur_id == id:
            start_pos, end_pos = spans[id]
            assert end_pos == pos - 1
            spans[id] = (start_pos, pos)
        else:
            spans[id] = (pos, pos)
            cur_id = id
        continue

    for file_id in reversed(range(max(spans.keys()) + 1)):
        start_pos, end_pos = spans[file_id]
        file_len = end_pos - start_pos + 1
        left_insert_pos = find_insert_pos(start_pos, file_len, spans)
        if left_insert_pos is not None:
            spans[file_id] = (left_insert_pos, left_insert_pos + file_len - 1)

    return spans


def calculate_checksum_from_start_ends(spans: Dict[int, Tuple[int, int]]) -> int:
    return sum(
        [file_id * pos for file_id, (start, end) in spans.items() for pos in range(start, end + 1)]
    )


class Day09(Day):
    def part1(self, file_path: Path) -> int:
        disk = extract_file_blocks(file_path)
        ordered = rearrange_blocks(disk)
        return sum([pos * id for pos, id in enumerate(ordered) if id is not None])

    def part2(self, file_path: Path) -> int:
        disk = extract_file_blocks(file_path)
        ordered_start_ends = rearrange_files(disk)
        return calculate_checksum_from_start_ends(ordered_start_ends)


if __name__ == '__main__':
    day = Day09()
    day.print_solution('puzzle.txt')
