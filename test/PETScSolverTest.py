#!/usr/bin/env python3
# 
import sys
import numpy as np
from scipy.sparse import bmat, spdiags
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

from fealpy.solver.petsc_solver import PETScSolver


class PETScSolverTest():

    def __init__(self):
        pass


    def solve_poisson_3d(self, n=5):
        from fealpy.pde.poisson_3d import CosCosCosData as PDE
        from fealpy.functionspace import LagrangeFiniteElementSpace
        from fealpy.boundarycondition import DirichletBC 

        pde = PDE()
        mesh = pde.init_mesh(n=n)
        space = LagrangeFiniteElementSpace(mesh, p=1)
        bc = DirichletBC(space, pde.dirichlet) 
        uh = space.function()
        A = space.stiff_matrix()
        F = space.source_vector(pde.source)

        A, F = bc.apply(A, F, uh)

        solver = PETScSolver()
        solver.solve(A, F, uh)
        error = space.integralalg.L2_error(pde.solution, uh)
        print(error)



test = PETScSolverTest()

if sys.argv[1] == 'poisson3d':
    n = int(sys.argv[2])
    test.solve_poisson_3d(n=n)
