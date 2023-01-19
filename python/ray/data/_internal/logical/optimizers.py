from typing import List

from ray.data._internal.execution.interfaces import PhysicalOperator
from ray.data._internal.logical.interfaces import Rule, Optimizer, LogicalOperator


class LogicalOptimizer(Optimizer):
    """The optimizer for logical operators."""

    @property
    def rules(self) -> List[Rule]:
        # TODO: Add logical optimizer rules.
        return []


class PhysicalOptimizer(Optimizer):
    """The optimizer for physical operators."""

    @property
    def rules(self) -> List["Rule"]:
        # TODO: Add physical optimizer rules.
        return []


class LogicalPlan:
    """The plan with a DAG of logical operators."""

    def __init__(self, dag: LogicalOperator):
        self._dag = dag

    def get_new_plan(self, operator: LogicalOperator) -> "LogicalPlan":
        """Get a new logical plan with the given operator to add."""
        assert self._dag is not None
        operator.set_input_dependencies([self._dag])
        return LogicalPlan(operator)

    def get_execution_dag(self) -> PhysicalOperator:
        """Get the DAG of physical operators to execute.

        This process has 3 steps:
        (1).logical optimization: optimize logical operators.
        (2).convert logical to physical operators.
        (3).physical optimization: optimize physical operators.
        """
        logical_optimizer = LogicalOptimizer()
        optimized_logical_dag = logical_optimizer.optimize(self._dag)
        physical_dag = optimized_logical_dag.get_physical_dag()
        return PhysicalOptimizer().optimize(physical_dag)
