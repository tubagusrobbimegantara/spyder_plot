import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfigurasi Halaman
st.set_page_config(page_title="Excel Radar Visualizer", layout="wide")

st.title("📈 Excel-to-Spyder Chart")
st.markdown("Unggah file Excel kamu, pilih entitasnya, dan lihat hasilnya secara instan.")

# --- SIDEBAR: UPLOAD & SETTINGS ---
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Pilih file Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Membaca data
    df = pd.read_excel(uploaded_file)
    
    st.sidebar.subheader("Pengaturan Chart")
    
    # 1. Pilih kolom yang berisi Nama/Label (misal: Nama Produk, Nama Atlet)
    label_col = st.sidebar.selectbox("Pilih kolom label (Entitas):", df.columns)
    
    # 2. Pilih kolom-kolom angka yang akan dijadikan metrik
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    selected_metrics = st.sidebar.multiselect("Pilih metrik (Kategori):", numeric_cols, default=numeric_cols[:5])
    
    # 3. Pilih entitas spesifik yang ingin dibandingkan
    entities = df[label_col].unique()
    selected_entities = st.sidebar.multiselect("Pilih entitas untuk dibandingkan:", entities, default=entities[:2] if len(entities) > 1 else entities)

    if selected_metrics and selected_entities:
        # --- PROSES DATA ---
        fig = go.Figure()
        
        # Palet warna estetik
        colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']

        for i, entity in enumerate(selected_entities):
            # Ambil baris data untuk entitas yang dipilih
            filtered_df = df[df[label_col] == entity]
            values = filtered_df[selected_metrics].values.flatten().tolist()
            
            # Tambahkan ke grafik
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=selected_metrics,
                fill='toself',
                name=str(entity),
                line=dict(color=colors[i % len(colors)]),
                opacity=0.7
            ))

        # --- TAMPILAN CHART ---
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, gridcolor="#E5E5E5"),
                angularaxis=dict(gridcolor="#E5E5E5")
            ),
            showlegend=True,
            template='plotly_white',
            height=600,
            margin=dict(l=100, r=100, t=50, b=50)
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Detail Data")
            st.dataframe(df[df[label_col].isin(selected_entities)][[label_col] + selected_metrics])

    else:
        st.warning("Silakan pilih minimal satu metrik dan satu entitas di sidebar.")

else:
    # Tampilan saat belum ada file
    st.info("👋 Silakan unggah file Excel di sidebar untuk memulai.")
    st.markdown("""
    **Format Excel yang disarankan:**
    | Nama Produk | Speed | Reliability | Comfort |
    |-------------|-------|-------------|---------|
    | Toyota      | 8     | 9           | 7       |
    | Honda       | 7     | 8           | 9       |
    """)
