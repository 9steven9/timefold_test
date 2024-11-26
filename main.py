from timefold.solver.config import (SolverConfig, ScoreDirectorFactoryConfig,
                                    TerminationConfig, Duration)
from timefold.solver import SolverFactory, SolutionManager
import logging

from domain import *
from constraints import define_constraints


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('app')


def main():
    solver_factory = SolverFactory.create(
        SolverConfig(
            solution_class=Schedule,
            entity_class_list=[ShiftAssignment],
            score_director_factory_config=ScoreDirectorFactoryConfig(
                constraint_provider_function=define_constraints
            ),
            termination_config=TerminationConfig(
                spent_limit=Duration(seconds=50)
            )
        ))

    # Load the problem
    problem = generate_demo_data()

    # Solve the problem
    solver = solver_factory.build_solver()
    solution = solver.solve(problem)

    solution_manager = SolutionManager.create(solver_factory)
    score_analysis = solution_manager.analyze(solution)

    # Visualize the solution
    print_solution(solution, score_analysis)


def generate_demo_data() -> Schedule:

    def id_generator():
        current = 0
        while True:
            yield str(current)
            current += 1

    ids = id_generator()

    employees = [Employee(next(ids), 'Employee ' + str(i)) for i in range(10)]
    stores = [Store(next(ids), 'Store' + str(i)) for i in range(10)]
    shifts = [Shift(next(ids), store, i) for store in stores for i in range(10)]

    shift_assignments = [ShiftAssignment(next(ids), period, employee) for employee in employees for period in range(10)]
    # Comment the line above and uncomment the next line to see that there is a valid solution.
    #shift_assignments = [ShiftAssignment(next(ids), (j+i)%10, employees[j], shifts[(10*i + (i+j)%10)]) for i in range(10) for j in range(10)]

    return Schedule(next(ids), shifts, shift_assignments)


def print_solution(schedule, score_analysis) -> None:
    LOGGER.info("")
    
    for shift_assignment in schedule.shift_assignments:
        employee_name = shift_assignment.employee.name
        store_name = shift_assignment.shift.store.name
        period = shift_assignment.period
        
        print(employee_name + " works at " + store_name + " in period " +
            str(period) +  ".")

    print(score_analysis)
        

if __name__ == '__main__':
    main()
