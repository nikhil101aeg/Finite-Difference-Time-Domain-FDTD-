# 2D Finite-Difference Time-Domain (FDTD) Electromagnetic Simulator

**IIT Patna | Engineering Physics | CPI: 7.21**  
*A from-scratch implementation of Maxwell's equations solver using Yee's algorithm*

---

## 📚 Theoretical Foundation

### 1. Maxwell's Equations
The foundation of all electromagnetic phenomena:

$$
\nabla \times \mathbf{E} = -\mu \frac{\partial \mathbf{H}}{\partial t} \quad \text{(Faraday's Law)}
$$

$$
\nabla \times \mathbf{H} = \epsilon \frac{\partial \mathbf{E}}{\partial t} \quad \text{(Ampere's Law)}
$$

### 2. 2D Transverse Magnetic (TM) Mode
For computational efficiency while maintaining physical insight:

$$
\frac{\partial H_x}{\partial t} = -\frac{1}{\mu} \frac{\partial E_z}{\partial y}
$$

$$
\frac{\partial H_y}{\partial t} = \frac{1}{\mu} \frac{\partial E_z}{\partial x}
$$

$$
\frac{\partial E_z}{\partial t} = \frac{1}{\epsilon} \left( \frac{\partial H_y}{\partial x} - \frac{\partial H_x}{\partial y} \right)
$$

### 3. Yee's Staggered Grid Discretization
Spatial and temporal staggering for stable numerical solutions:

**Grid positions:**

$$
E_z(i,j) \rightarrow E_z(i\Delta x, j\Delta y, n\Delta t)
$$

$$
H_x(i,j) \rightarrow H_x\left(i\Delta x, \left(j+\frac{1}{2}\right)\Delta y, \left(n+\frac{1}{2}\right)\Delta t\right)
$$

$$
H_y(i,j) \rightarrow H_y\left(\left(i+\frac{1}{2}\right)\Delta x, j\Delta y, \left(n+\frac{1}{2}\right)\Delta t\right)
$$

### 4. Finite Difference Discretization
Central difference approximation for derivatives:

$$
\frac{\partial f}{\partial x} \approx \frac{f(x+\Delta x/2) - f(x-\Delta x/2)}{\Delta x} + \mathcal{O}(\Delta x^2)
$$

$$
\frac{\partial f}{\partial t} \approx \frac{f(t+\Delta t/2) - f(t-\Delta t/2)}{\Delta t} + \mathcal{O}(\Delta t^2)
$$

### 5. FDTD Update Equations

**Update H from E:**

$$
H_x^{n+\frac{1}{2}}\left(i,j+\frac{1}{2}\right) = H_x^{n-\frac{1}{2}}\left(i,j+\frac{1}{2}\right) - \frac{\Delta t}{\mu \Delta y} \left[ E_z^n(i,j+1) - E_z^n(i,j) \right]
$$

$$
H_y^{n+\frac{1}{2}}\left(i+\frac{1}{2},j\right) = H_y^{n-\frac{1}{2}}\left(i+\frac{1}{2},j\right) + \frac{\Delta t}{\mu \Delta x} \left[ E_z^n(i+1,j) - E_z^n(i,j) \right]
$$

**Update E from H:**

$$
E_z^{n+1}(i,j) = E_z^n(i,j) + \frac{\Delta t}{\epsilon} \left[ \frac{H_y^{n+\frac{1}{2}}\left(i+\frac{1}{2},j\right) - H_y^{n+\frac{1}{2}}\left(i-\frac{1}{2},j\right)}{\Delta x} - \frac{H_x^{n+\frac{1}{2}}\left(i,j+\frac{1}{2}\right) - H_x^{n+\frac{1}{2}}\left(i,j-\frac{1}{2}\right)}{\Delta y} \right]
$$

### 6. Courant-Friedrichs-Lewy (CFL) Stability Condition
For numerical stability in 2D:

$$
\Delta t \leq \frac{1}{c \sqrt{\frac{1}{\Delta x^2} + \frac{1}{\Delta y^2}}}
$$

With uniform grid spacing $\Delta x = \Delta y = \Delta$:

$$
\Delta t \leq \frac{\Delta}{c\sqrt{2}} \quad \text{where} \quad c = \frac{1}{\sqrt{\mu\epsilon}}
$$

### 7. Boundary Conditions

**Perfect Electric Conductor (PEC):**

$$
\mathbf{E}_{\text{tan}} = 0 \quad \Rightarrow \quad E_z = 0 \quad \text{on metal surface}
$$

**Absorbing Boundary Conditions (Simple ABC):**

$$
E_z^{\text{boundary}} = E_z^{\text{interior}} \cdot \alpha \quad \text{with} \quad \alpha < 1
$$

### 8. Material Implementation

**Dielectric Materials:**

$$
E_z^{n+1}(i,j) = E_z^n(i,j) + \frac{\Delta t}{\epsilon_0 \epsilon_r(i,j)} \cdot \nabla \times \mathbf{H}
$$

**Perfect Electric Conductor:**

$$
E_z(i,j) = 0 \quad \forall \quad (i,j) \in \text{metal region}
$$

### 9. Source Excitation
Gaussian pulse modulated sine wave:

$$
E_z^{\text{source}}(t) = \exp\left[-\left(\frac{t - t_0}{\tau}\right)^2\right] \cdot \sin(2\pi f_c t)
$$

where:
- $t_0$: pulse center time
- $\tau$: pulse width  
- $f_c$: center frequency

### 10. Energy Conservation Validation
Total electromagnetic energy in lossless media:

$$
W_{\text{total}} = \frac{1}{2} \sum_{i,j} \left[ \epsilon_0 \epsilon_r(i,j) E_z^2(i,j) + \mu_0 \left( H_x^2(i,j) + H_y^2(i,j) \right) \right]
$$

Should remain constant after source turns off: $\Delta W_{\text{total}} \approx 0$

---

## 🔑 Key Features Implemented

### **Core Algorithm**
- Pure Python implementation with explicit loops for clarity
- Yee's staggered grid with leapfrog time-stepping
- Central difference spatial discretization (2nd order accurate)

### **Physics Capabilities**
- Wave propagation in free space and materials
- Perfect Electric Conductor (PEC) boundaries
- Dielectric materials with user-defined $\epsilon_r$
- Simple absorbing boundary conditions
- Gaussian pulse source excitation

### **Validation & Analysis**
- Energy conservation monitoring
- Wave speed verification
- Field measurement probes
- Visual field distribution plots
- Quantitative error analysis

### **Code Quality**
- Modular structure for easy extension
- Detailed comments explaining physics
- Parameterized simulations
- Reproducible results

---

## 🎯 Applications Demonstrated

### **1. Basic Wave Propagation**
- Isotropic expansion from point source
- Wavefront visualization
- Speed verification: $v_{\text{measured}} \approx c$

### **2. Scattering from Metal Objects**
- Perfect reflection from PEC boundaries
- Shadow zone formation
- Standing wave patterns near reflectors
- Interference between incident and reflected waves

### **3. Dielectric Material Effects**
- Wave speed reduction: $v = c/\sqrt{\epsilon_r}$
- Wavelength compression inside dielectric
- Partial reflection at material boundaries
- Field continuity validation

### **4. Boundary Condition Testing**
- PEC vs absorbing boundary comparisons
- Reflection coefficient estimation
- Energy leakage analysis

---

## 📊 Results & Validation

### **Quantitative Validation**

**Wave Speed Verification:**
$$
v_{\text{measured}} = \frac{\text{Distance traveled}}{\text{Time steps} \times \Delta t} \approx \frac{1}{\sqrt{\mu_0\epsilon_0}}
$$

**Energy Conservation (Lossless Case):**
$$
\frac{|W_{\text{final}} - W_{\text{initial}}|}{W_{\text{initial}}} < 5\% \quad \text{(After source turns off)}
$$

**Numerical Stability:**
- CFL condition strictly enforced: $\Delta t = 0.5 \times \frac{\Delta}{c\sqrt{2}}$
- No exponential blow-up observed in 1000+ time steps
- Long-term simulation stability verified

### **Qualitative Observations**

**Wave Propagation:**
- Circular wavefronts from point source
- Uniform expansion in isotropic media
- Expected attenuation with distance

**Scattering Phenomena:**
- Clear shadow zones behind metal obstacles
- Constructive/destructive interference patterns
- Edge diffraction visible at metal corners

**Material Interactions:**
- Visible wavelength reduction in dielectrics
- Reflection at dielectric boundaries
- Field penetration into dielectric materials

---

## 🔬 Physical Observations

### **Wave-Metal Interaction**
1. **Complete Reflection**: Electric field forced to zero at metal surface
2. **Standing Waves**: Nodes at metal surface, antinodes at $\lambda/4$ intervals
3. **Shadow Zones**: Regions behind metal with significantly reduced field strength
4. **Edge Diffraction**: Wave bending around metal corners

### **Wave-Dielectric Interaction**  
1. **Speed Reduction**: Wavefront visibly slows upon entering dielectric
2. **Wavelength Compression**: $\lambda_{\text{dielectric}} = \lambda_0/\sqrt{\epsilon_r}$
3. **Partial Reflection**: Some energy reflects at dielectric interface
4. **Continuity**: Tangential E-field continuous across boundaries

### **Numerical Artifacts Identified**
1. **Numerical Dispersion**: Slight wavefront distortion at high frequencies
2. **Boundary Reflections**: Simple ABC causes ~20% reflection
3. **Staircase Approximation**: Rectangular grid approximates curved boundaries

### **Energy Flow Analysis**
1. **Source Region**: Energy increases during pulse excitation
2. **Propagation Phase**: Energy spreads uniformly through domain
3. **Steady State**: Energy stabilizes after reflections dissipate
4. **Conservation Check**: Total energy constant in lossless simulations

---
