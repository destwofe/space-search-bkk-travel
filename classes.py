from typing import NamedTuple


class Node(NamedTuple):
  id: int
  # parrentID: int
  visitedStations: list[str]
  state: str # current station
  vehicle: str # current vehicle
  costMoney: int # cost money
  costDuration: int # cost duration
  f: int
  route: list[str]

class NodeMap(NamedTuple):
  origins: str
  destination: str
  duration: float
  cost: float
  description: str
