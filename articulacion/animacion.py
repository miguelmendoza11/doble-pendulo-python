
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import matplotlib.animation as animation
import matplotlib

# Ruta explícita corregida al ejecutable ffmpeg
matplotlib.rcParams['animation.ffmpeg_path'] = r"C:\Users\Usuario 1\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
from matplotlib.animation import FFMpegWriter

# Parámetros físicos
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

x1 = L1 * np.sin(sol.y[0])
y1 = -L1 * np.cos(sol.y[0])
x2 = x1 + L2 * np.sin(sol.y[1])
y2 = y1 - L2 * np.cos(sol.y[1])

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.set_aspect('equal')
ax.grid()
line, = ax.plot([], [], 'o-', lw=2)
trace, = ax.plot([], [], '-', lw=1, alpha=0.5)
x2_trace, y2_trace = [], []

def init():
    line.set_data([], [])
    trace.set_data([], [])
    return line, trace

def update(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]
    line.set_data(thisx, thisy)
    x2_trace.append(x2[i])
    y2_trace.append(y2[i])
    trace.set_data(x2_trace, y2_trace)
    return line, trace

ani = animation.FuncAnimation(fig, update, frames=len(t_eval),
                              init_func=init, blit=True, interval=10)

writer = FFMpegWriter(fps=30, codec='libx264')
ani.save("animacion_doble_pendulo.mp4", writer=writer)
