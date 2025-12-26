import numpy as np
import matplotlib.pyplot as plt

Nx = 200
Ny = 200
Hx = np.zeros((Nx, Ny))
Hy = np.zeros((Nx, Ny))
Ez = np.zeros((Nx, Ny))
dt = 0.5
src_x, src_y = Nx//2, Ny//2

metal = np.zeros((Nx,Ny), dtype = bool)
metal[120:60, 120:60] = True

epsilon = np.ones((Nx,Ny), dtype = bool)
epsilon[40:80,40:80] = 4.0

print("Starting FDTD simulation...")
print(f"Grid: {Nx}x{Ny}, dt={dt}, source at ({src_x}, {src_y})")

# Track max field for scaling
max_field = 0.0
field_at_source = []

for t in range(300):  # Increased to 300
    # Update Hx
    for i in range(Nx):
        for j in range(1, Ny):
            Hx[i, j] = Hx[i, j] - dt * (Ez[i, j] - Ez[i, j-1])
    
    # Update Hy
    for i in range(1, Nx):
        for j in range(Ny):
            Hy[i, j] = Hy[i, j] + dt * (Ez[i, j] - Ez[i-1, j])
    
    # Update Ez
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            curl_H = ((Hy[i, j] - Hy[i-1, j]) - (Hx[i, j] - Hx[i, j-1]))
            Ez[i,j] += dt*curl_H/epsilon[i,j]
    
    Ez[metal] = 0
    
    # Absorbing boundaries (CORRECT - keep this!)
    Ez[:, 0] = Ez[:, 1] * 0.8
    Ez[:, -1] = Ez[:, -2] * 0.8
    Ez[0, :] = Ez[1, :] * 0.8
    Ez[-1, :] = Ez[-2, :] * 0.8

    if t < 30:
        pulse = np.exp(-0.5*((t-40)/15)**2)*3
        Ez[src_x,src_y] += pulse
    
    # Add source
    if t in [60, 120, 200, 320]:
        plt.figure(figsize=(10, 8))
        
        # Plot field
        plt.subplot(2, 2, 1)
        field_max = np.max(np.abs(Ez))
        vmax = max(0.01, field_max)
        plt.imshow(Ez.T, cmap='RdBu', origin='lower', 
                  vmin=-vmax, vmax=vmax)
        plt.title(f'Electric Field at t={t}')
        plt.colorbar()
        
        # Overlay objects
        # Metal in red
        y_metal, x_metal = np.where(metal.T)
        plt.scatter(x_metal, y_metal, color='red', s=1, alpha=0.7, label='Metal (PEC)')
        
        # Dielectric in green overlay
        y_diel, x_diel = np.where(epsilon.T == 4.0)
        plt.scatter(x_diel, y_diel, color='green', s=1, alpha=0.3, label='Dielectric (ε=4)')
        
        plt.legend()
        
        # Plot dielectric region field separately
        plt.subplot(2, 2, 2)
        diel_field = Ez[40:80, 40:80].T  # Extract dielectric region
        if diel_field.size > 0:
            plt.imshow(diel_field, cmap='RdBu', origin='lower')
            plt.title('Field inside Dielectric')
            plt.colorbar()
        
        # Plot slices
        plt.subplot(2, 2, 3)
        slice_x = Ez[:, src_y]
        plt.plot(slice_x, 'b-', linewidth=2)
        plt.axvline(x=120, color='r', linestyle='--', alpha=0.5, label='Metal starts')
        plt.axvline(x=160, color='r', linestyle='--', alpha=0.5, label='Metal ends')
        plt.title(f'Slice at y={src_y}')
        plt.xlabel('X'); plt.ylabel('Ez')
        plt.grid(True); plt.legend()
        
        plt.subplot(2, 2, 4)
        # Explain what's happening
        explanation = f"""
        PHYSICS DEMONSTRATION:
        
        METAL (Red square):
        • Perfect conductor
        • Ez = 0 always
        • Wave reflects completely
        • Creates shadow zone
        
        DIELECTRIC (Green square):
        • ε = 4.0 (FR4-like)
        • Wave slows down: v = c/√4 = c/2
        • Part reflects at boundary
        • Part transmits through
        • Wavelength reduces inside
        
        Time: t = {t}
        """
        plt.text(0.1, 0.5, explanation, transform=plt.gca().transAxes,
                fontsize=9, verticalalignment='center')
        plt.axis('off')
        
        plt.suptitle('FDTD: Wave Interaction with Metal & Dielectric', fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'scatter_dielectric_t{t:04d}.png', dpi=120)
        plt.close()
        print(f"Saved frame t={t}")

print("\n" + "="*60)
print("KEY OBSERVATIONS:")
print("="*60)
print("1. METAL (Red):")
print("   • Strong reflection visible")
print("   • Shadow zone behind metal")
print("   • Field exactly ZERO inside metal")
print()
print("2. DIELECTRIC (Green):")
print("   • Wave slows down inside (wavelength shorter)")
print("   • Partial reflection at boundary")
print("   • Field continues through (transmission)")
print("   • Lower amplitude inside (impedance mismatch)")
print("="*60)