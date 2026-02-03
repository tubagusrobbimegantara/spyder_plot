import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Konfigurasi Halaman (Default Putih)
st.set_page_config(page_title="Radar Chart Minimalis", layout="wide")

st.title("📊 Data Visualizer")
st.markdown("Unggah file Excel untuk melihat perbandingan kategori.")

# --- SIDEBAR: INPUT ---
st.sidebar.header("Pengaturan")
uploaded_file = st.sidebar.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])

# Warna yang solid dan profesional
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Deteksi kolom
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    object_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    label_col = st.sidebar.selectbox("Pilih Kolom Label:", object_cols if object_cols else df.columns)
    selected_metrics = st.sidebar.multiselect("Pilih Metrik:", numeric_cols, default=numeric_cols[:5])
    
    entities = df[label_col].unique().tolist()
    selected_entities = st.sidebar.multiselect("Pilih Data yang Dibandingkan:", entities, default=entities[:2])

    if selected_metrics and selected_entities:
        fig = go.Figure()

        for i, entity in enumerate(selected_entities):
            filtered_df = df[df[label_col] == entity]
            values = filtered_df[selected_metrics].values.flatten().tolist()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=selected_metrics,
                fill='toself',
                name=entity,
                line=dict(color=COLORS[i % len(COLORS)], width=2),
                marker=dict(size=6)
            ))

        # Layout Bersih & Background Putih
        fig.update_layout(
            template="plotly_white",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    gridcolor="#e0e0e0",
                    linecolor="#e0e0e0",
                    range=[0, df[selected_metrics].max().max() * 1.1]
                ),
                angularaxis=dict(
                    gridcolor="#e0e0e0",
                    linecolor="#e0e0e0"
                )
            ),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(l=50, r=50, t=50, b=50),
            height=600
        )

        # Tampilkan
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabel Data Sederhana
        with st.expander("Lihat Tabel Data"):
            st.write(df[df[label_col].isin(selected_entities)])
    else:
        st.info("Pilih metrik dan entitas di sidebar.")
else:
    st.warning("Silakan unggah file Excel di sidebar untuk memunculkan grafik.")
