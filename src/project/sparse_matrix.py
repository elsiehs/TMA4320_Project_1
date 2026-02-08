# """
# fdm.py, men med implementert sparse matrix for å effektivere prosessen. 
# For å kjøre denne må man endre data.py og _init_.py slik at
# de importerer solve_heat_equation fra denne filen, og ikke fdm. I tillegg kommentere ut fdm.py """

# """Finite Difference Method solver for the 2D heat equation."""

# import numpy as np
# from scipy.sparse import diags, kron, eye, csc_matrix
# from scipy.sparse.linalg import splu
# from .config import Config 


# def solve_heat_equation(cfg: Config) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
#     # Create grids
#     x = np.linspace(cfg.x_min, cfg.x_max, cfg.nx)
#     y = np.linspace(cfg.y_min, cfg.y_max, cfg.ny)
#     t = np.linspace(cfg.t_min, cfg.t_max, cfg.nt)

#     dx, dy = x[1] - x[0], y[1] - y[0]
#     dt = t[1] - t[0]

#     X, Y = np.meshgrid(x, y, indexing="ij")

#     # Storage: T[time, x, y]
#     T = np.zeros((cfg.nt, cfg.nx, cfg.ny))
#     T[0] = cfg.T_outside  # initial condition

#     # Sparse A and its factorization
#     A = _build_matrix_sparse(cfg, dx, dy, dt)
#     lu = splu(A)  # reusable LU factorization

#     # Time stepping
#     for k in range(cfg.nt - 1):
#         b_k = _build_rhs(cfg, T[k], X, Y, dx, dy, dt, t[k + 1])  # shape: (nx*ny,)
#         T_next_flat = lu.solve(b_k)  # fast solve with reused LU
#         T[k + 1] = T_next_flat.reshape(cfg.nx, cfg.ny)

#     return x, y, t, T



# #Build sparse matrix
# def _build_matrix_sparse(cfg: Config, dx: float, dy: float, dt: float):
#     """
#     Build the implicit Euler system matrix A as a SciPy sparse matrix
#     using Kronecker sums with Robin BCs folded into the 1D operators.
#     """
#     nx, ny = cfg.nx, cfg.ny
#     n = nx * ny

#     rx = cfg.alpha * dt / dx**2
#     ry = cfg.alpha * dt / dy**2

#     # Robin parameters 
#     beta_x = (cfg.h * dx) / cfg.k
#     beta_y = (cfg.h * dy) / cfg.k

#     # 1D operator in x with Robin BCs
#     main_x = 2.0 * np.ones(nx)
#     main_x[0]  = 1.0 + beta_x    # left boundary
#     main_x[-1] = 1.0 + beta_x    # right boundary
#     off_x = -1.0 * np.ones(nx - 1)
#     Lx = diags([off_x, main_x, off_x], offsets=[-1, 0, 1], format="csr")

#     #1D operator in y with Robin BCs
#     main_y = 2.0 * np.ones(ny)
#     main_y[0]  = 1.0 + beta_y    # bottom boundary
#     main_y[-1] = 1.0 + beta_y    # top boundary
#     off_y = -1.0 * np.ones(ny - 1)
#     Ly = diags([off_y, main_y, off_y], offsets=[-1, 0, 1], format="csr")

#     # Identity matrices
#     Ix = eye(nx, format="csr")
#     Iy = eye(ny, format="csr")

#     # Kronecker-sum assembly: A = I + rx*(Lx ⊗ Iy) + ry*(Ix ⊗ Ly)
#     A = eye(n, format="csr") + rx * kron(Lx, Iy, format="csr") + ry * kron(Ix, Ly, format="csr")


#     return csc_matrix(A)


# def _build_rhs(cfg: Config, T_curr, X, Y, dx, dy, dt, t_next):
#     """Build right-hand side for implicit system."""
#     rhs = T_curr.copy()

#     # Heat source
#     q = np.array(cfg.heat_source(X, Y, t_next))
#     rhs += dt * q

#     # Robin BC contributions
#     rx = cfg.alpha * dt / dx**2
#     ry = cfg.alpha * dt / dy**2
#     bc_term = cfg.T_outside

#     rhs[0, :] += rx * (cfg.h * dx / cfg.k) * bc_term
#     rhs[-1, :] += rx * (cfg.h * dx / cfg.k) * bc_term
#     rhs[:, 0] += ry * (cfg.h * dy / cfg.k) * bc_term
#     rhs[:, -1] += ry * (cfg.h * dy / cfg.k) * bc_term

#     return rhs.flatten()
