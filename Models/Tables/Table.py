import numpy as np
from numpy import ndarray


class Table:
    def __init__(self, columns: list, rows: list):
        self.columns = columns
        self.rows = rows
        self.cells = self.get_cells_by_column()

    def __get_headers(self) -> ndarray:
        first_row = self.rows[0]
        center = [int(box.x + box.w / 2) for box in first_row if box]
        center = np.array(center)
        center.sort()

        return center

    def get_cells_by_column(self):
        headers = self.__get_headers()
        boxes_list = []
        total_cells = len(headers)

        for row in self.rows:
            l = [[] for _ in range(total_cells)]  # empty columns
            for box in row:
                box_center_x = box.x + box.w / 4  # heuristic offset, can tweak
                diff = abs(headers - box_center_x)
                indexing = list(diff).index(min(diff))  # closest header column
                l[indexing].append(box)
            boxes_list.append(l)

        return boxes_list
