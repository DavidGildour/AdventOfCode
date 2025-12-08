from point import Point


class CircuitTracker:
    def __init__(self):
        self.__next_circuit_id = 0
        self.__circuit_dict: dict[int, set[Point]] = dict()

    def add_circuit(self, starting_point: Point):
        self.__circuit_dict[self.__next_circuit_id] = {starting_point}
        starting_point.circuit_id = self.__next_circuit_id
        self.__next_circuit_id += 1

    def get_circuit(self, circuit_id: int) -> set[Point]:
        return self.__circuit_dict[circuit_id]

    def remove_circuit(self, circuit_id: int):
        del self.__circuit_dict[circuit_id]

    def merge_circuits(self, circuit_id_a: int, circuit_id_b: int):
        if circuit_id_a == circuit_id_b:
            return

        circuit_b = self.get_circuit(circuit_id_b)
        self.__circuit_dict[circuit_id_a] = self.get_circuit(circuit_id_a).union(
            circuit_b
        )

        for point in circuit_b:
            point.circuit_id = circuit_id_a

        self.remove_circuit(circuit_id_b)

    def sorted(self) -> list[set[Point]]:
        return sorted((points for points in self.__circuit_dict.values()), key=len)

    def circuit_count(self) -> int:
        return len(self.__circuit_dict)

    def __repr__(self):
        builder = ["\n"]

        for k, points in self.__circuit_dict.items():
            builder.append(f"{k}:")
            builder += [f"\t{point}" for point in points]

        return "\n".join(builder)
