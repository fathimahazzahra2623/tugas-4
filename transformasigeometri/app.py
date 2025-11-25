import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Judul dan Pengantar ---
st.title("🧪 Virtual Lab Transformasi Geometri")
st.markdown("Interaktif mempelajari **Rotasi**, **Translasi**, **Refleksi**, dan **Dilatasi**.")

# --- Bagian 1: Input Titik Awal (Sidebar) ---
st.sidebar.header("1. Input Titik Awal")
try:
    # Memastikan input diterima sebagai float
    x_awal = st.sidebar.number_input("Koordinat X Awal (P)", value=2.0, step=0.5)
    y_awal = st.sidebar.number_input("Koordinat Y Awal (P)", value=3.0, step=0.5)
    
    # Titik awal sebagai vektor numpy
    titik_awal = np.array([x_awal, y_awal])
except ValueError:
    st.error("Masukkan angka yang valid untuk koordinat.")
    st.stop()

# --- Bagian 2: Pilihan Transformasi (Sidebar) ---
st.sidebar.header("2. Pilih & Atur Transformasi")
transformasi_pilih = st.sidebar.selectbox(
    "Pilih Jenis Transformasi",
    ["Translasi (Pergeseran)", "Refleksi (Pencerminan)", "Rotasi (Perputaran)", "Dilatasi (Perkalian)"]
)

# Inisialisasi titik hasil
titik_hasil = np.copy(titik_awal) # Gunakan np.copy agar tidak merubah nilai awal

# --- Bagian 3: Logika Transformasi (Main Content) ---

st.header(f"Transformasi: {transformasi_pilih}")
deskripsi_rumus = ""

if transformasi_pilih == "Translasi (Pergeseran)":
    tx = st.slider("Vektor Translasi X (Tx)", -5.0, 5.0, 1.0, step=0.5)
    ty = st.slider("Vektor Translasi Y (Ty)", -5.0, 5.0, 1.0, step=0.5)
    
    vektor_translasi = np.array([tx, ty])
    # Rumus: P' = P + T
    titik_hasil = titik_awal + vektor_translasi
    deskripsi_rumus = f"Rumus: $P'(x', y') = P(x, y) + T(T_x, T_y) = ({titik_awal[0]} + {tx}, {titik_awal[1]} + {ty})$"

elif transformasi_pilih == "Refleksi (Pencerminan)":
    sumbu_refleksi = st.selectbox(
        "Pilih Sumbu Pencerminan",
        ["Sumbu X (y=0)", "Sumbu Y (x=0)", "Garis y=x", "Garis y=-x"]
    )
    
    # Matriks Refleksi
    if sumbu_refleksi == "Sumbu X (y=0)":
        matriks_refleksi = np.array([[1, 0], [0, -1]])
        deskripsi_rumus = "Rumus: $(x, y) \\rightarrow (x, -y)$. Matriks: $$\\begin{pmatrix} 1 & 0 \\\\ 0 & -1 \\end{pmatrix}$$"
    elif sumbu_refleksi == "Sumbu Y (x=0)":
        matriks_refleksi = np.array([[-1, 0], [0, 1]])
        deskripsi_rumus = "Rumus: $(x, y) \\rightarrow (-x, y)$. Matriks: $$\\begin{pmatrix} -1 & 0 \\\\ 0 & 1 \\end{pmatrix}$$"
    elif sumbu_refleksi == "Garis y=x":
        matriks_refleksi = np.array([[0, 1], [1, 0]])
        deskripsi_rumus = "Rumus: $(x, y) \\rightarrow (y, x)$. Matriks: $$\\begin{pmatrix} 0 & 1 \\\\ 1 & 0 \\end{pmatrix}$$"
    elif sumbu_refleksi == "Garis y=-x":
        matriks_refleksi = np.array([[0, -1], [-1, 0]])
        deskripsi_rumus = "Rumus: $(x, y) \\rightarrow (-y, -x)$. Matriks: $$\\begin{pmatrix} 0 & -1 \\\\ -1 & 0 \\end{pmatrix}$$"
        
    # Rumus: P' = M * P (menggunakan perkalian matriks)
    titik_hasil = matriks_refleksi @ titik_awal

elif transformasi_pilih == "Rotasi (Perputaran)":
    # Rotasi berpusat di (0,0)
    sudut_derajat = st.slider("Sudut Rotasi (Derajat, berlawanan jarum jam)", -360, 360, 90)
    
    # Konversi ke radian
    theta = np.deg2rad(sudut_derajat)
    
    # Matriks Rotasi
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    matriks_rotasi = np.array([
        [cos_t, -sin_t], 
        [sin_t, cos_t]
    ])
    
    # Rumus: P' = R * P
    titik_hasil = matriks_rotasi @ titik_awal
    
    deskripsi_rumus = f"Rotasi sebesar ${sudut_derajat}^\\circ$ berlawanan arah jarum jam. Matriks Rotasi $R(\\theta)$: $$\\begin{pmatrix} \\cos \\theta & -\\sin \\theta \\\\ \\sin \\theta & \\cos \\theta \\end{pmatrix}$$"

elif transformasi_pilih == "Dilatasi (Perkalian)":
    k = st.slider("Faktor Skala (k)", -3.0, 3.0, 2.0, step=0.1)
    
    # Matriks Dilatasi
    matriks_dilatasi = np.array([[k, 0], [0, k]])
    
    # Rumus: P' = D * P
    titik_hasil = matriks_dilatasi @ titik_awal
    
    deskripsi_rumus = f"Dilatasi dengan faktor skala $k={k}$ berpusat di $(0,0)$. Rumus: $(x, y) \\rightarrow (kx, ky)$."

# Menampilkan Rumus
st.markdown(deskripsi_rumus)
    
# --- Bagian 4: Visualisasi & Hasil ---
st.subheader("Hasil Koordinat")

# Menampilkan hasil koordinat
col_awal, col_hasil = st.columns(2)

col_awal.metric(
    label=f"Titik Awal P", 
    value=f"({titik_awal[0]:.2f}, {titik_awal[1]:.2f})"
)
col_hasil.metric(
    label=f"Titik Hasil P'", 
    value=f"({titik_hasil[0]:.2f}, {titik_hasil[1]:.2f})"
)

st.subheader("Visualisasi")

# Membuat Plot
fig, ax = plt.subplots(figsize=(6, 6))

# Plot titik awal (biru)
ax.plot(titik_awal[0], titik_awal[1], 'o', color='blue', markersize=8, label='P Awal')
ax.text(titik_awal[0] + 0.15, titik_awal[1] + 0.15, 'P', color='blue', fontsize=12)

# Plot titik hasil (merah)
ax.plot(titik_hasil[0], titik_hasil[1], 'x', color='red', markersize=8, mew=2, label='P\' Hasil')
ax.text(titik_hasil[0] + 0.15, titik_hasil[1] + 0.15, "P'", color='red', fontsize=12)

# Menarik garis dari asal ke hasil (untuk visualisasi translasi/rotasi/dilatasi)
if transformasi_pilih in ["Translasi (Pergeseran)", "Rotasi (Perputaran)", "Dilatasi (Perkalian)"]:
    ax.plot([titik_awal[0], titik_hasil[0]], [titik_awal[1], titik_hasil[1]], 'k--', alpha=0.5)

# Pengaturan Plot
ax.axhline(0, color='gray', linewidth=0.8, zorder=0) # Garis Sumbu X
ax.axvline(0, color='gray', linewidth=0.8, zorder=0) # Garis Sumbu Y
ax.set_xlabel("Sumbu X")
ax.set_ylabel("Sumbu Y")
ax.set_title(f"Visualisasi {transformasi_pilih}")
ax.grid(True, linestyle=':', alpha=0.7)
ax.set_aspect('equal', adjustable='box') # Penting agar plot tidak terdistorsi

# Menentukan batas plot agar kedua titik terlihat
semua_koordinat = np.concatenate(([titik_awal], [titik_hasil]), axis=0)
padding = 2.0
min_c = np.min(semua_koordinat) - padding
max_c = np.max(semua_koordinat) + padding
limit = max(abs(min_c), abs(max_c))

ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

st.pyplot(fig)
