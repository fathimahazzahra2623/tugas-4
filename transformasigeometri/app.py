import streamlit as st
import numpy as np


# --- Judul dan Pengantar ---
st.title("🧪 Virtual Lab Transformasi Geometri")
st.markdown("Interaktif mempelajari **Rotasi**, **Translasi**, **Refleksi**, dan **Dilatasi**.")

# --- Bagian 1: Input Titik Awal ---
st.sidebar.header("1. Input Titik Awal")
x_awal = st.sidebar.number_input("Koordinat X Awal (P)", value=2.0, step=0.5)
y_awal = st.sidebar.number_input("Koordinat Y Awal (P)", value=3.0, step=0.5)
titik_awal = np.array([x_awal, y_awal])

# --- Bagian 2: Pilihan Transformasi ---
st.sidebar.header("2. Pilih & Atur Transformasi")
transformasi_pilih = st.sidebar.selectbox(
    "Pilih Jenis Transformasi",
    ["Translasi (Pergeseran)", "Refleksi (Pencerminan)", "Rotasi (Perputaran)", "Dilatasi (Perkalian)"]
)

# Inisialisasi titik hasil sama dengan titik awal
titik_hasil = titik_awal

# --- Bagian 3: Logika Transformasi Berdasarkan Pilihan ---

if transformasi_pilih == "Translasi (Pergeseran)":
    st.subheader("Transformasi: Translasi (Pergeseran)")
    tx = st.slider("Vektor Translasi X (Tx)", -5.0, 5.0, 1.0, step=0.5)
    ty = st.slider("Vektor Translasi Y (Ty)", -5.0, 5.0, 1.0, step=0.5)
    
    vektor_translasi = np.array([tx, ty])
    # Rumus: P' = P + T
    titik_hasil = titik_awal + vektor_translasi
    st.info(f"Titik Hasil P' = ({titik_awal[0]} + {tx}, {titik_awal[1]} + {ty})")

elif transformasi_pilih == "Refleksi (Pencerminan)":
    st.subheader("Transformasi: Refleksi (Pencerminan)")
    sumbu_refleksi = st.selectbox(
        "Pilih Sumbu Pencerminan",
        ["Sumbu X (y=0)", "Sumbu Y (x=0)", "Garis y=x", "Garis y=-x"]
    )
    
    # Matriks Refleksi
    if sumbu_refleksi == "Sumbu X (y=0)":
        matriks_refleksi = np.array([[1, 0], [0, -1]])
        st.info("Pencerminan terhadap Sumbu X: (x, y) -> (x, -y)")
    elif sumbu_refleksi == "Sumbu Y (x=0)":
        matriks_refleksi = np.array([[-1, 0], [0, 1]])
        st.info("Pencerminan terhadap Sumbu Y: (x, y) -> (-x, y)")
    elif sumbu_refleksi == "Garis y=x":
        matriks_refleksi = np.array([[0, 1], [1, 0]])
        st.info("Pencerminan terhadap Garis y=x: (x, y) -> (y, x)")
    elif sumbu_refleksi == "Garis y=-x":
        matriks_refleksi = np.array([[0, -1], [-1, 0]])
        st.info("Pencerminan terhadap Garis y=-x: (x, y) -> (-y, -x)")
        
    # Rumus: P' = M * P (menggunakan perkalian matriks)
    titik_hasil = matriks_refleksi @ titik_awal

elif transformasi_pilih == "Rotasi (Perputaran)":
    st.subheader("Transformasi: Rotasi (Perputaran)")
    # Rotasi berpusat di (0,0)
    sudut_derajat = st.slider("Sudut Rotasi (Derajat, berlawanan jarum jam)", -360, 360, 90)
    
    # Konversi ke radian
    theta = np.deg2rad(sudut_derajat)
    
    # Matriks Rotasi
    matriks_rotasi = np.array([
        [np.cos(theta), -np.sin(theta)], 
        [np.sin(theta), np.cos(theta)]
    ])
    
    # Rumus: P' = R * P
    titik_hasil = matriks_rotasi @ titik_awal
    
    st.info(f"Rotasi sebesar {sudut_derajat}° berlawanan arah jarum jam terhadap titik pusat (0,0).")

elif transformasi_pilih == "Dilatasi (Perkalian)":
    st.subheader("Transformasi: Dilatasi (Perkalian)")
    k = st.slider("Faktor Skala (k)", -3.0, 3.0, 2.0, step=0.1)
    
    # Matriks Dilatasi
    matriks_dilatasi = np.array([[k, 0], [0, k]])
    
    # Rumus: P' = D * P
    titik_hasil = matriks_dilatasi @ titik_awal
    
    st.info(f"Dilatasi dengan faktor skala k={k} berpusat di titik pusat (0,0).")
    
# --- Bagian 4: Visualisasi & Hasil ---
st.header("Hasil Visual & Koordinat")

# Menampilkan hasil koordinat
st.metric(
    label=f"Koordinat Titik Awal P", 
    value=f"({titik_awal[0]:.2f}, {titik_awal[1]:.2f})"
)
st.metric(
    label=f"Koordinat Titik Hasil P'", 
    value=f"({titik_hasil[0]:.2f}, {titik_hasil[1]:.2f})"
)

# Membuat Plot
fig, ax = plt.subplots()

# Plot titik awal (biru)
ax.plot(titik_awal[0], titik_awal[1], 'o', color='blue', label='P Awal')
ax.text(titik_awal[0] + 0.1, titik_awal[1] + 0.1, 'P', color='blue')

# Plot titik hasil (merah)
ax.plot(titik_hasil[0], titik_hasil[1], 'x', color='red', label='P\' Hasil')
ax.text(titik_hasil[0] + 0.1, titik_hasil[1] + 0.1, "P'", color='red')

# Pengaturan Plot
ax.axhline(0, color='gray', linewidth=0.5) # Garis Sumbu X
ax.axvline(0, color='gray', linewidth=0.5) # Garis Sumbu Y
ax.set_xlabel("Sumbu X")
ax.set_ylabel("Sumbu Y")
ax.set_title(f"Visualisasi {transformasi_pilih}")
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_aspect('equal', adjustable='box')

# Menentukan batas plot agar kedua titik terlihat
min_x = min(titik_awal[0], titik_hasil[0], 0) - 2
max_x = max(titik_awal[0], titik_hasil[0], 0) + 2
min_y = min(titik_awal[1], titik_hasil[1], 0) - 2
max_y = max(titik_awal[1], titik_hasil[1], 0) + 2

ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)

st.pyplot(fig)
