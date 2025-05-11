import heapq
import sys

from collections import deque


# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def bfs(source, data, rows, cols):
    si, sj = source
    queue = deque([(si, sj, 0, 0)])
    seen = {(si, sj)}
    result = {}
    while queue:
        i, j, dist, req = queue.popleft()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if not (0 <= ni < rows and 0 <= nj < cols):
                continue
            if (ni, nj) in seen:
                continue
            ch = data[ni][nj]
            if ch == '#':
                continue
            nreq = req
            if 'A' <= ch <= 'Z':
                nreq |= 1 << (ord(ch.lower()) - ord('a'))
            seen.add((ni, nj))
            if 'a' <= ch <= 'z':
                result[ch] = (dist + 1, nreq)
            queue.append((ni, nj, dist + 1, nreq))
    return result


def solve(data):
    rows, cols = len(data), len(data[0])
    key_positions = {}
    starts = []
    for i in range(rows):
        for j in range(cols):
            c = data[i][j]
            if c == '@':
                starts.append((i, j))
            elif 'a' <= c <= 'z':
                key_positions[c] = (i, j)
    nodes = starts + [key_positions[k] for k in sorted(key_positions)]
    n_starts = len(starts)
    total_keys = len(key_positions)
    all_keys_mask = (1 << total_keys) - 1
    graph = [None] * len(nodes)
    for idx, pos in enumerate(nodes):
        graph[idx] = bfs(pos, data, rows, cols)
    start_state = tuple(range(n_starts))
    heap = [(0, start_state, 0)]
    visited = { (start_state, 0): 0 }
    while heap:
        steps, positions, mask = heapq.heappop(heap)
        if mask == all_keys_mask:
            return steps
        if visited[(positions, mask)] < steps:
            continue
        for ri in range(n_starts):
            node_idx = positions[ri]
            for key, (dist, req) in graph[node_idx].items():
                km = 1 << (ord(key) - ord('a'))
                if mask & km or req & ~mask:
                    continue
                new_positions = list(positions)
                key_idx = n_starts + sorted(key_positions).index(key)
                new_positions[ri] = key_idx
                new_mask = mask | km
                new_steps = steps + dist
                state = (tuple(new_positions), new_mask)
                if visited.get(state, float('inf')) > new_steps:
                    visited[state] = new_steps
                    heapq.heappush(heap, (new_steps, state[0], new_mask))
    return -1


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()