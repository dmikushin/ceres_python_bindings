import sys
import pytest

sys.path.insert(0, "../build")  # location of the PyCeres lib. By default this assumes you build the library
# using the stand mkdir build , cd build, cmake ..

import PyCeres  # Import the Python Bindings
import numpy as np


class PythonCostFunc(PyCeres.CostFunction):
    def __init__(self):
        super().__init__()
        self.set_num_residuals(2)
        self.set_parameter_block_sizes([3])

    def Evaluate(self,parameters, residuals, jacobians):
        x=parameters[0][0]
        y=parameters[0][1]
        z=parameters[0][2]

        residuals[0]=x+2*y+4*z
        residuals[1]=y*z
        if jacobians!=None:
            jacobian=jacobians[0]
            jacobian[0 * 2 + 0] = 1
            jacobian[0 * 2 + 1] = 0

            jacobian[1 * 2 + 0] = 2
            jacobian[1 * 2 + 1] = z

            jacobian[2 * 2 + 0] = 4
            jacobian[2 * 2 + 1] = y
        return True


def RunBasicProblem():
    cost_function = PythonCostFunc()

    data = [0.76026643, -30.01799744, 0.55192142]
    np_data = np.array(data)

    print(np_data)

    problem = PyCeres.Problem()

    problem.AddResidualBlock(cost_function, None, np_data)
    options = PyCeres.SolverOptions()
    options.linear_solver_type = PyCeres.LinearSolverType.DENSE_QR
    options.minimizer_progress_to_stdout = True
    summary = PyCeres.Summary()
    PyCeres.Solve(options, problem, summary)
    return summary.final_cost

def test_cost():
    cost=RunBasicProblem()
    assert pytest.approx(0.0, 1e-10) == cost

