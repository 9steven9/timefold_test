from timefold.solver.domain import (planning_entity, planning_solution, PlanningId, PlanningVariable,
                                    PlanningEntityCollectionProperty,
                                    ProblemFactCollectionProperty, ValueRangeProvider,
                                    PlanningScore)
from timefold.solver.score import HardSoftScore
from dataclasses import dataclass, field
from typing import Annotated


@dataclass
class Employee:
    id: Annotated[str, PlanningId]
    name: str

    def __str__(self):
        return f'{self.name}'


@dataclass
class Store:
    id: Annotated[str, PlanningId]
    name: str

    def __str__(self):
        return f'{self.name}'


@planning_entity
@dataclass
class ShiftAssignment:
    id: Annotated[str, PlanningId]
    period: int
    employee: Employee
    shift: Annotated['Shift', PlanningVariable] = field(default=None)

    def __str__(self):
        return f'{self.name}'


@dataclass
class Shift:
    id: Annotated[str, PlanningId]
    store: Store
    period: int

    def __str__(self):
        return f'{self.name}'


@planning_solution
@dataclass
class Schedule:
    id: str
    shifts: Annotated[list[Shift],
                     ProblemFactCollectionProperty,
                     ValueRangeProvider]
    shift_assignments: Annotated[list[ShiftAssignment], PlanningEntityCollectionProperty]

    score: Annotated[HardSoftScore, PlanningScore] = field(default=None)
