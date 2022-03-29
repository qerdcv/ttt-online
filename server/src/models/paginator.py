import math


class Paginator:
    page = 1
    limit = 10

    def __init__(self, total_count: int, page: str, limit: str):
        if page.isnumeric():
            page = int(page)
            if page > 1:
                self.page = page
        if limit.isnumeric():
            limit = int(limit)
            if limit > 100:
                self.limit = 100
            elif limit > 1:
                self.limit = limit
        self.count_games = math.ceil(total_count / self.limit)

    def to_json(self) -> dict:
        return {
                'page': self.page,
                'limit': self.limit,
                'total_games': self.count_games,
            }
