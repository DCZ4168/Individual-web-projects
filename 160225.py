import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 🔧 Define key parameters
bus_departure = 15 + 25/60  # Convert 15:25 to decimal hours
sigma1 = 1.5/60  # Small variance for "just-in-time" passengers
sigma2 = 4/60    # Higher variance for "early arrivals"
sigma3 = 1/60    # Low variance for "near-miss" passengers
weight1 = 0.55   # 55% arrive just in time
weight2 = 0.35   # 35% prefer to wait longer
weight3 = 0.10   # 10% arrive just after departure

# 🎲 Define the number of simulation runs (days)
N = 1000  # Simulating passenger behavior for 1000 bus departures

# 🏃‍♂️ Generate arrival times for different groups of passengers
just_in_time = np.random.normal(bus_departure - 5/60, sigma1, int(N * weight1))  # Arrive ~5 min before
early_arrivals = np.random.normal(bus_departure - 10/60, sigma2, int(N * weight2))  # Arrive ~10 min before
late_arrivals = np.random.normal(bus_departure + 1.5/60, sigma3, int(N * weight3))  # Arrive ~1.5 min too late

# 📊 Combine all passenger arrivals into a single dataset
arrival_times = np.concatenate((just_in_time, early_arrivals, late_arrivals))

# 🕒 Compute waiting times (only for those who arrive before the bus)
waiting_times = bus_departure - arrival_times
waiting_times = waiting_times[waiting_times > 0]  # Exclude those who missed the bus

# ❌ Count the percentage of passengers who miss the bus
missed_passengers = np.sum(arrival_times > bus_departure) / N * 100

# 📊 Compute key percentiles for waiting times
p50 = np.percentile(waiting_times, 50) * 60  # Median waiting time in minutes
p90 = np.percentile(waiting_times, 90) * 60  # 90th percentile
p99 = np.percentile(waiting_times, 99) * 60  # 99th percentile

# 🎨 Visualizing the waiting time distribution
sns.set(style="darkgrid")
plt.figure(figsize=(8, 5))
sns.histplot(waiting_times * 60, bins=30, kde=True, color="royalblue", edgecolor='black')
plt.axvline(p50, color='red', linestyle='--', label=f"Median: {p50:.2f} min")
plt.axvline(p90, color='orange', linestyle='--', label=f"90th percentile: {p90:.2f} min")
plt.axvline(p99, color='purple', linestyle='--', label=f"99th percentile: {p99:.2f} min")
plt.xlabel("Waiting Time (minutes)")
plt.ylabel("Frequency")
plt.title("Passenger Waiting Time Distribution")
plt.legend()
plt.show()

# 🚀 Simulating the impact of bus delays on missed passengers
delays = [0, 3, 5, 7]  # Test different bus delays (minutes)
missed_passengers_delayed = []

for delay in delays:
    new_departure = bus_departure + delay/60  # Adjust departure time
    new_missed = np.sum(arrival_times > new_departure) / N * 100  # Compute new missed rate
    missed_passengers_delayed.append(new_missed)

# 📉 Visualizing how delays affect missed passengers
plt.figure(figsize=(8, 5))
plt.plot(delays, missed_passengers_delayed, marker='o', linestyle='-', color='crimson')
plt.xlabel("Bus Delay (min)")
plt.ylabel("Missed Passengers (%)")
plt.title("Impact of Bus Delays on Passengers Who Miss the Bus")
plt.grid()
plt.show()

# 📊 Display simulation results
print(f"📌 Median Waiting Time: {p50:.2f} min")
print(f"📌 90th Percentile: {p90:.2f} min")
print(f"📌 99th Percentile: {p99:.2f} min")
print(f"❌ Missed Passengers (on-time bus): {missed_passengers:.2f}%")

# 📌 Print results for different delay scenarios
for d, m in zip(delays, missed_passengers_delayed):
    print(f"⏳ With a delay of {d} min, {m:.2f}% of passengers miss the bus.")
