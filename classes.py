from typing import NamedTuple


class Node(NamedTuple):
  id: int
  visitedStations: list[str]
  state: str
  vehicle: str
  costMoney: int
  costDuration: int
  f: int
  route: list[str]

class NodeMap(NamedTuple):
  origins: str
  destination: str
  duration: float
  cost: float
  description: str
