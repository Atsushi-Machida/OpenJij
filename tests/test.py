import unittest
import numpy as np

import openjij as oj

class UtilsTest(unittest.TestCase):
    def test_benchmark(self):
        h = {0: 1}
        J = {(0, 1):-1.0, (1,2): -1.0}

        bqm = oj.BinaryQuadraticModel(h, J)
        samp = oj.Sampler(bqm)

        solver = lambda param, iterations: samp.simulated_annealing(step_num=param, iteration=iterations)
        ground_state = [-1, -1, -1]
        ground_energy = bqm.calc_energy(ground_state)
        step_num_list = np.linspace(10, 50, 5, dtype=np.int)
        print(step_num_list)
        bm_res = oj.benchmark([ground_state], ground_energy, solver, param_list=step_num_list)
        self.assertTrue(set(bm_res) >= {'time', 'error', 'e_res', 'tts', 'tts_threshold_prob'})

        self.assertEqual(len(bm_res) ,len(step_num_list))


class ModelTest(unittest.TestCase):
    def test_bqm(self):
        h = {}
        J = {(0,1): -1.0, (1,2): -3.0}
        bqm = oj.BinaryQuadraticModel(h=h, J=J)

        self.assertEqual(type(bqm.ising_interactions()), np.ndarray)
        correct_mat = np.array([[0, -1, 0,],[-1, 0, -3],[0, -3, 0]])
        np.testing.assert_array_equal(bqm.ising_interactions(), correct_mat.astype(np.float))

class SamplerOptimizeTest(unittest.TestCase):

    def setUp(self):
        h = {0: -1, 1: -1}
        J = {(0,1): -1.0, (1,2): -1.0}
        self.bqm = oj.BinaryQuadraticModel(h=h, J=J)  
        self.samp = oj.Sampler(model=self.bqm)

    def test_sa(self):
        response = self.samp.simulated_annealing()
        self.assertEqual(len(response.states), 1)
        self.assertListEqual(response.states[0], [1,1,1])

    def test_sqa(self):
        response = self.samp.simulated_quantum_annealing()
        self.assertEqual(len(response.states), 1)
        self.assertListEqual(response.states[0], [1,1,1])


if __name__ == '__main__':
    unittest.main()