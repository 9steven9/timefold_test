from timefold.solver.score import (constraint_provider, HardSoftScore, Joiners,
                                   ConstraintFactory, Constraint)

from domain import ShiftAssignment


@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        # Hard constraints
        employee_works_store_at_most_once(constraint_factory),
        shift_period_constraint(constraint_factory),
        doubly_assigned_shift_conflict(constraint_factory)
        
        # Soft constraints
    ]


def shift_period_constraint(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each(ShiftAssignment)
            .filter(lambda shift_assignment: shift_assignment.period != shift_assignment.shift.period)
            .penalize(HardSoftScore.ONE_HARD)
            .as_constraint("Assigned shift in wrong period!"))


def doubly_assigned_shift_conflict(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each_unique_pair(ShiftAssignment,
                                Joiners.equal(lambda shift_assignment: shift_assignment.shift))
            .penalize(HardSoftScore.ONE_HARD)
            .as_constraint("Shift assigned more than once!"))


def employee_works_store_at_most_once(constraint_factory: ConstraintFactory) -> Constraint:
    return (constraint_factory
            .for_each_unique_pair(ShiftAssignment,
                                  Joiners.equal(lambda shift_assignment: shift_assignment.employee),
                                  Joiners.equal(lambda shift_assignment: shift_assignment.shift.store))
            .penalize(HardSoftScore.ONE_HARD)
            .as_constraint("Employee works at same store more than once conflict!"))
