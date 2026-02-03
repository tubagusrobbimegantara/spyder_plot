import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Radar Chart Mapper", layout="wide")

st.title("📊 Radar Chart Analysis")
st.markdown("Visualisasi perbandingan entitas berdasarkan data Excel.")

# 2. Sidebar untuk Upload
st.sidebar.header("Data Input")
uploaded_file = st.sidebar.file_uploader("Unggah file Excel (.xlsx)", type=["xlsx"])

# Warna yang mirip dengan contoh gambar (Blue, Orange, Green)
COLOR_PALETTE = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Deteksi kolom otomatis
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    object_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    st.sidebar.subheader("Konfigurasi")
    label_col = st.sidebar.selectbox("Pilih Kolom Entitas:", object_cols if object_cols else df.columns)
    selected_metrics = st.sidebar.multiselect("Pilih Metrik:", numeric_cols, default=numeric_cols[:5])
    
    entities = df[label_col].unique().tolist()
    selected_entities = st.sidebar.multiselect("Pilih Data untuk Ditampilkan:", entities, default=entities[:3])

    if selected_metrics and selected_entities:
        fig = go.Figure()

        for i, entity in enumerate(selected_entities):
            filtered_df = df[df[label_col] == entity]
            # Plotly butuh nilai pertama diulang di akhir untuk menutup garis lingkaran
            r_values = filtered_df[selected_metrics].values.flatten().tolist()
            theta_values = selected_metrics
            
            # Tambahkan trace
            fig.add_trace(go.Scatterpolar(
                r=r_values,
                theta=theta_values,
                fill='toself',
                name=entity,
                mode='lines+markers+text', # Memunculkan garis, titik, dan teks angka
                text=r_values,             # Menampilkan angka nilai
                textposition="top center", # Posisi angka
                textfont=dict(size=12, color=COLOR_PALETTE[i % len(COLOR_PALETTE)], family="Arial Black"),
                line=dict(color=COLOR_PALETTE[i % len(COLOR_PALETTE)], width=3),
                marker=dict(size=8),
                fillcolor=f"rgba{tuple(list(int(COLOR_PALETTE[i % len(COLOR_PALETTE)][j:j+2], 16) for j in (1, 3, 5)) + [0.2])}" # Transparansi area
            ))

        # 3. Layout Estetik (Minimalis Putih)
        fig.update_layout(
            template="plotly_white",
            polar=dict(
                bgcolor="white",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100], # Mengikuti contoh gambar (persentil 0-100)
                    gridcolor="#ECECEC",
                    linecolor="#ECECEC",
                    tickfont=dict(size=10, color="gray")
                ),
                angularaxis=dict(
                    gridcolor="#ECECEC",
                    linecolor="#ECECEC",
                    tickfont=dict(size=12, color="#333", weight="bold")
                )
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=14)
            ),
            margin=dict(l=100, r=100, t=80, b=100),
            height=700
        )

        # Tampilkan di Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        # Opsi Tabel Data
        with st.expander("Lihat Detail Tabel"):
            st.dataframe(df[df[label_col].isin(selected_entities)], use_container_width=True)
    else:
        st.info("Silakan tentukan metrik dan entitas di sidebar.")
else:
    # State Awal
    st.info("Silakan unggah file Excel di sidebar untuk memulai.")
    st.image("https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/bus.jpg", caption="Contoh format data: Baris untuk entitas, Kolom untuk skor.", width=400)
