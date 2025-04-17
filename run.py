
import json


def check_capacity(max_capacity: int, guests: list) -> bool:
    # Реализация алгоритма
    events = []
    for guest in guests:
        check_in = guest['check-in']
        check_out = guest['check-out']
        events.append((check_in, 1))
        events.append((check_out, -1))
    events.sort()
    current_occupancy = 0
    for _, event_type in events:
        current_occupancy += event_type
        if current_occupancy > max_capacity:
            return False
    return True


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())


    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)


    result = check_capacity(max_capacity, guests)
    print(result)