"""Setup check for the GAMSPy workshop.

Run:  python hello_gamspy.py
You should see "Status: OPTIMAL".
"""
import gamspy as gp

m = gp.Container()

# A tiny LP: make chairs and desks to maximize profit with limited wood and labor.
chairs = gp.Variable(m, "chairs", type="positive")
desks = gp.Variable(m, "desks", type="positive")

wood = gp.Equation(m, "wood")
labor = gp.Equation(m, "labor")
wood[...] = 2 * chairs + 5 * desks <= 100
labor[...] = 3 * chairs + 2 * desks <= 60

hello = gp.Model(m, "hello", equations=[wood, labor], problem="LP",
                 sense="max", objective=30 * chairs + 60 * desks)
hello.solve()

ok = hello.status in (gp.ModelStatus.OptimalGlobal, gp.ModelStatus.OptimalLocal)
print(f"Status: {'OPTIMAL' if ok else hello.status.name}")
print(f"Profit: {hello.objective_value:.1f}")
print(f"GAMSPy {gp.__version__} is ready.")
