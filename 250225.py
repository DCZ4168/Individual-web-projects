from pulp import *

N = 10
T_max = 60
trips = ["A-B", "A-C", "B-D", "C-E", "D-F", "E-G"]
distances = [15, 10, 20, 25, 30, 18]
costs = [2, 3, 1.5, 2.5, 2, 3]

times = [20, 15, 30, 40, 45, 25]
Vj = [2, 1, 2, 1, 2, 1]

x = [[LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(len(trips))] for i in range(N)]

model = LpProblem("Deadheading_Minimization", LpMinimize)

model += lpSum(costs[j] * distances[j] * x[i][j] for i in range(N) for j in range(len(trips)))

for i in range(N):
    model += lpSum(x[i][j] for j in range(len(trips))) <= 1

for i in range(N):
    model += lpSum(times[j] * x[i][j] for j in range(len(trips))) <= T_max

for j in range(len(trips)):
    model += lpSum(x[i][j] for i in range(N)) >= Vj[j]

model.solve() 

print("Status:", model.status)
for i in range(N):
    for j in range(len(trips)):
        if x[i][j].value() == 1:
            print(f"Bus {i+1} assigned to trip {trips[j]}")
