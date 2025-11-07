import heapq
import matplotlib.pyplot as plt

# -------------------------
# Step 1: Define flights and gates
# -------------------------
flights = [
    {"id": "F1", "arrival": 8.00, "departure": 9.00},
    {"id": "F2", "arrival": 8.30, "departure": 10.00},
    {"id": "F3", "arrival": 9.10, "departure": 9.50},
    {"id": "F4", "arrival": 10.00, "departure": 11.00},
    {"id": "F5", "arrival": 9.30, "departure": 10.20},
]

gates = {
    "G1": {"distance": 10, "schedule": []},
    "G2": {"distance": 20, "schedule": []},
    "G3": {"distance": 30, "schedule": []},
}

# -------------------------
# Step 2: Helper — check overlap
# -------------------------
def overlaps(f1, f2):
    return not (f1["departure"] <= f2["arrival"] or f1["arrival"] >= f2["departure"])

# -------------------------
# Step 3: Heuristic function (for GBFS)
# -------------------------
def heuristic(flight, gate):
    # Simple heuristic: prefer closer gates and no overlap
    penalty = 0
    for f in gate["schedule"]:
        if overlaps(f, flight):
            penalty += 1000  # large penalty for conflict
    return gate["distance"] + penalty

# -------------------------
# Step 4: Greedy Best-First Search assignment
# -------------------------
assignments = {}

for flight in sorted(flights, key=lambda f: f["arrival"]):
    # Priority queue for possible gates
    pq = []
    for g_name, gate in gates.items():
        h = heuristic(flight, gate)
        heapq.heappush(pq, (h, g_name))

    best_gate = None
    while pq:
        _, g_name = heapq.heappop(pq)
        gate = gates[g_name]
        # Accept first gate with no conflict
        if all(not overlaps(f, flight) for f in gate["schedule"]):
            best_gate = g_name
            break

    if best_gate:
        gates[best_gate]["schedule"].append(flight)
        assignments[flight["id"]] = best_gate
    else:
        assignments[flight["id"]] = "WAIT/DELAYED"

# -------------------------
# Step 5: Print results
# -------------------------
print("🧭 Greedy Best-First Gate Assignment")
print("----------------------------------")
for f, g in assignments.items():
    print(f"{f} → {g}")

# -------------------------
# Step 6: Visualization
# -------------------------
colors = {"G1": "skyblue", "G2": "lightgreen", "G3": "salmon", "WAIT/DELAYED": "gray"}
fig, ax = plt.subplots(figsize=(10, 5))

for gate_name, gate_data in gates.items():
    for flight in gate_data["schedule"]:
        ax.barh(
            y=gate_name,
            width=flight["departure"] - flight["arrival"],
            left=flight["arrival"],
            color=colors.get(gate_name, "lightgray"),
            edgecolor='black',
            height=0.4
        )
        ax.text(flight["arrival"] + 0.05, gate_name, flight["id"], va='center', fontsize=9)

ax.set_xlabel("Time (Hours)")
ax.set_ylabel("Gate")
ax.set_title("✈️ Gate Assignment using Greedy Best-First Search")
ax.grid(True, axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
