import os
from enum import Enum


def main():
    currentFolderPath = os.path.dirname(__file__)
    rootFolderPath = os.path.join(currentFolderPath, "..\\")
    tspFilePath = os.path.join(rootFolderPath, "data\\ulysses16.tsp")
    print(os.path.isfile(tspFilePath))

    tsp = TSP(tspFilePath)
    print(tsp.name)
    print(tsp.comment)
    print(tsp.type.name)
    print(tsp.dimension)
    print(tsp.edgeWeightType.name)


class TSP_TYPE(Enum):
    TSP = 1
    ATSP = 2
    SOP = 3
    HCP = 4
    CVRP = 5
    TOUR = 6


class EDGE_WEIGHT_TYPE(Enum):
    EXPLICIT = 1
    EUC_2D = 2
    EUC_3D = 3
    MAX_2D = 4
    MAX_3D = 5
    MAN_2D = 6
    MAN_3D = 7
    CEIL_2D = 8
    GEO = 9
    ATT = 10
    XRAY1 = 11
    XRAY2 = 12
    SPECIAL = 13


class EDGE_WEIGHT_FORMAT(Enum):
    FUNCTION = 1
    FULL_MATRIX = 2
    UPPER_ROW = 3
    LOWER_ROW = 4
    UPPER_DIAG_ROW = 5
    LOWER_DIAG_ROW = 6
    UPPER_COL = 7
    LOWER_COL = 8
    UPPER_DIAG_COL = 9
    LOWER_DIAG_COL = 10


class EDGE_DATA_FORMAT(Enum):
    EDGE_LIST = 1
    ADJ_LIST = 2


class NODE_COORD_TYPE(Enum):
    TWOD_COORDS = 1
    THREED_COORDS = 2
    NO_COORDS = 3


class DISPLAY_DATA_TYPE(Enum):
    COORD_DISPLAY = 1
    TWOD_DISPLAY = 2
    NO_DISPLAY = 3


class TSP:
    name: str
    comment: str
    type: TSP_TYPE
    dimension: int
    capacity: int
    edgeWeightType: EDGE_WEIGHT_TYPE
    edgeWeightFormat: EDGE_WEIGHT_FORMAT
    edgeDataFormat: EDGE_DATA_FORMAT
    nodeCoordType: NODE_COORD_TYPE
    displayDataType: DISPLAY_DATA_TYPE
    _filePath: str
    _fileContent: list[str]

    def __init__(self, filePath: str) -> None:
        self._filePath = filePath
        self._fileContent = self._readTSPFile(filePath)
        self._parseAllMetadata(self._fileContent)

    def _readTSPFile(self, filePath: str) -> list[str]:
        if not filePath.lower().endswith(".tsp"):
            raise ValueError("Incorrect filePath. File should be .tsp file")

        lines: list[str] = []
        with open(filePath) as file:
            for line in file:
                lines.append(line.rstrip())

        return lines

    def _parseAllMetadata(self, fileContent: list[str]):
        metadataDict: dict[str, str] = {}

        for line in fileContent:
            if ":" in line:
                lineParts = line.split(":", maxsplit=2)
                metadataDict[lineParts[0].strip()] = lineParts[1].strip()

        for key, value in metadataDict.items():
            match (key):
                case "NAME":
                    self.name = value
                case "TYPE":
                    self.type = TSP_TYPE[value]
                case "COMMENT":
                    self.comment = value
                case "DIMENSION":
                    self.dimension = int(value)
                case "CAPACITY":
                    self.capacity = int(value)
                case "EDGE_WEIGHT_TYPE":
                    self.edgeWeightType = EDGE_WEIGHT_TYPE[value]
                case "EDGE_WEIGHT_FORMAT":
                    self.edgeWeightFormat = EDGE_WEIGHT_FORMAT[value]
                case "EDGE_DATA_FORMAT":
                    self.edgeDataFormat = EDGE_DATA_FORMAT[value]
                case "NODE_COORD_TYPE":
                    self.nodeCoordType = NODE_COORD_TYPE[value]
                case "DISPLAY_DATA_TYPE":
                    self.displayDataType = DISPLAY_DATA_TYPE[value]
                case _:
                    pass


if __name__ == "__main__":
    main()
