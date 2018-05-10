# from OSOL_Extremum.arithmetics.interval import *
#
# import numpy as np
#
# import sys
# import os
#
# cwd = os.getcwd()
# sys.path.insert(0, cwd)
# sys.path.insert(0, cwd[:cwd.rindex('/')])
# sys.path.insert(0, cwd + '/temp')
#
#
# class DynamicSystem:
#
#     def __init__(self, f, controller, sampling_type, object_type):
#         self.f = f
#         self.controller = controller
#         self.sampling_type = sampling_type
#         if sampling_type == 'Euler':
#             self.prolong = self.prolong_Euler
#         elif sampling_type == 'RK4':
#             self.prolong = self.prolong_RK4
#         else:
#             raise Exception('Unknown sampling_type: {}'.format(sampling_type))
#         if object_type == 'real':
#             self.conversion = lambda v: v
#         elif object_type == 'interval':
#             self.conversion = lambda v: Interval.from_value(v)
#         else:
#             raise Exception('Unknown object_type: {}'.format(object_type))
#
#     def prolong_Euler(self, t, x, u, eps):
#         return x + self.f(t, x, u) * eps
#
#     def prolong_RK4(self, t, x, u, eps):
#         f = self.f
#         c = self.conversion
#         k1 = f(t, x, u)
#         k2 = f(t + c(0.5) * eps, x + k1 * c(0.5) * eps, u)
#         k3 = f(t + c(0.5) * eps, x + k2 * c(0.5) * eps, u)
#         k4 = f(t + eps, x + k3 * eps, u)
#         return x + (k1 + k2 * c(2.0) + k3 * c(2.0) + k4) * (eps / c(6.0))
#
#     def simulate(self, x0, eps, max_steps):
#         c = self.conversion
#         times = [c(0.0)]
#         states = [np.array(list(map(c, x0)))]
#         controls = []
#         _eps = c(eps)
#         for step_id in range(1, max_steps + 1):
#             t = times[-1]
#             x = states[-1]
#             u = self.controller(t, x)
#             x_next = self.prolong(t, x, u, _eps)
#             times.append(t + _eps)
#             states.append(x_next)
#             controls.append(u)
#         return times, states, controls
#
#
# def real(t):
#     return np.array([
#         1 - np.cos(t),
#         np.sin(t),
#         1 + t - np.sin(t) - np.cos(t)])
#
#
# def f(t, x, u):
#     x1 = x[0]
#     x2 = x[1]
#
#     dx1 = np.sin(t)
#     dx2 = np.cos(t)
#     dx3 = x1 + x2
#
#     return np.array([dx1, dx2, dx3])
#
#
# def controller(t, x):
#     return np.array([])
#
#
# ds = DynamicSystem(f, controller, sampling_type='RK4', object_type='real')
#
#
# times, states, controls = ds.simulate(x0=np.array([0, 0, 0]), eps=0.01, max_steps=1000)
#
# try:
#     states = list(map(lambda iv: np.array([i.middle_point for i in iv]), states))
#     times = np.array(list(map(lambda i: i.middle_point, times)))
# except Exception:
#     times = times
#     states = states
#
# real_states = []
# for t in times:
#     real_states.append(real(t))
#
# deltas = []
# for x1, x2 in zip(states, real_states):
#     deltas.append(np.linalg.norm(x1 - x2))
#
# print(np.array(deltas).max())
#
# #
# # intervals = np.array([Interval(1, 2), Interval(2, 3), Interval(3, 4)]) * 2
# # # i_sin = np.sqrt(intervals)
# # # for i1, i2 in zip(intervals, i_sin):
# # #     print(sqrt(i1), i2)
# #
# # for i in intervals:
# #     print(i)