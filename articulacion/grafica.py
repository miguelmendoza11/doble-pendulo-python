
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

g = 9.81
L1 = L2 = 1.0
m1 = m2 = 1.0

def doble_pendulo(t, y):
    θ1, θ2, ω1, ω2 = y
    Δ = θ2 - θ1

    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(Δ)**2
    den2 = (L2 / L1) * den1

    dθ1 = ω1
    dθ2 = ω2

    dω1 = (m2 * L1 * ω1**2 * np.sin(Δ) * np.cos(Δ) +
           m2 * g * np.sin(θ2) * np.cos(Δ) +
           m2 * L2 * ω2**2 * np.sin(Δ) -
           (m1 + m2) * g * np.sin(θ1)) / den1

    dω2 = (-m2 * L2 * ω2**2 * np.sin(Δ) * np.cos(Δ) +
           (m1 + m2) * g * np.sin(θ1) * np.cos(Δ) -
           (m1 + m2) * L1 * ω1**2 * np.sin(Δ) -
           (m1 + m2) * g * np.sin(θ2)) / den2

    return [dθ1, dθ2, dω1, dω2]

θ1_0 = θ2_0 = np.pi / 2
ω1_0 = ω2_0 = 0
y0 = [θ1_0, θ2_0, ω1_0, ω2_0]

t_span = (0, 10)
t_eval = np.linspace(*t_span, 1000)

sol = solve_ivp(doble_pendulo, t_span, y0, t_eval=t_eval, method='RK45')

plt.figure(figsize=(10, 5))
plt.plot(t_eval, np.degrees(sol.y[0]), label='θ₁ (húmero)')
plt.plot(t_eval, np.degrees(sol.y[1]), label='θ₂ (antebrazo)')
plt.xlabel("Tiempo [s]")
plt.ylabel("Ángulo [°]")
plt.title("Evolución de los ángulos")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
