from models import Route, Cave


class CaveSystem:
    def __init__(self, passages: list[str]):
        self.cave_map = {"start": Cave("start"), "end": Cave("end")}
        self.map_caves(passages)
        self.routes = []

    def get_or_add_cave(self, cave_name: str) -> Cave:
        if cave_name in self.cave_map:
            return self.cave_map[cave_name]
        else:
            cave = Cave(cave_name)
            self.cave_map[cave_name] = cave
            return cave

    def map_caves(self, passages: list[str]):
        for passage in passages:
            start, end = passage.split("-")

            start_cave = self.get_or_add_cave(start)
            end_cave = self.get_or_add_cave(end)

            if not end_cave.is_end:
                end_cave.exits.append(start_cave.name)
            if not start_cave.is_end:
                start_cave.exits.append(end_cave.name)

    def cave_available(
        self, route: Route, cave_name: str, with_new_rules: bool = False
    ) -> bool:
        cave = self.cave_map[cave_name]
        return not cave.is_start and (
            cave.is_big
            or cave.is_end
            or cave not in route.caves
            or (with_new_rules and route.bonus_traversal_available)
        )

    def traverse_cave(self, cave_name: str, route: Route, with_new_rules: bool = False):
        cave = self.cave_map[cave_name]
        route.add_cave(cave)
        valid_exits = [
            cave_exit
            for cave_exit in cave.exits
            if self.cave_available(route, cave_exit, with_new_rules)
        ]
        for exit_cave in valid_exits:
            self.traverse_cave(exit_cave, route.copy(), with_new_rules)

        if route.finished:
            self.routes.append(route)

    def get_all_possible_routes(self, with_new_rules: bool = False) -> list[Route]:
        route = Route()

        self.traverse_cave("start", route, with_new_rules)

        return self.routes
