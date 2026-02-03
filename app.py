import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Custom Radar Analytics", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Pro-Level Radar Chart")
st.write("Sesuaikan tampilan grafik secara interaktif melalui panel di sebelah kiri.")

# --- SIDEBAR: KONTROL INTERAKTIF ---
st.sidebar.header("📂 Data & Visual")
uploaded_file = st.sidebar.file_uploader("Unggah Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # 1. Kontrol Font & Visual
    st.sidebar.subheader("🎨 Estetika")
    font_size_label = st.sidebar.slider("Ukuran Font Kategori", 10, 24, 14)
    font_size_value = st.sidebar.slider("Ukuran Angka Nilai", 8, 20, 12)
    line_width = st.sidebar.slider("Ketebalan Garis", 1, 5, 3)
    marker_size = st.sidebar.slider("Ukuran Titik", 4, 12, 8)
    fill_opacity = st.sidebar.slider("Transparansi Warna", 0.0, 1.0, 0.2)
    
    # 2. Pilihan Kolom
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    object_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    label_col = st.sidebar.selectbox("Pilih Kolom Entitas:", object_cols if object_cols else df.columns)
    selected_metrics = st.sidebar.multiselect("Pilih Metrik:", numeric_cols, default=numeric_cols[:5])
    
    entities = df[label_col].unique().tolist()
    selected_entities = st.sidebar.multiselect("Pilih Data:", entities, default=entities[:3])

    if selected_metrics and selected_entities:
        fig = go.Figure()
        
        # Palet warna estetik (mirip gambar referensi)
        COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

        for i, entity in enumerate(selected_entities):
            filtered_df = df[df[label_col] == entity]
            r_values = filtered_df[selected_metrics].values.flatten().tolist()
            
            # Mendapatkan warna saat ini
            current_color = COLORS[i % len(COLORS)]

            fig.add_trace(go.Scatterpolar(
                r=r_values,
                theta=selected_metrics,
                fill='toself',
                name=entity,
                mode='lines+markers+text',
                text=r_values,
                textposition="top center",
                textfont=dict(size=font_size_value, color=current_color, family="Arial Black"),
                line=dict(color=current_color, width=line_width),
                marker=dict(size=marker_size),
                # Konversi hex ke rgba untuk transparansi
                fillcolor=f"rgba{tuple(list(int(current_color[j:j+2], 16) for j in (1, 3, 5)) + [fill_opacity])}"
            ))

        # --- LAYOUT SANGAT BERSIH ---
        fig.update_layout(
            template="plotly_white",
            polar=dict(
                bgcolor="white",
                radialaxis=dict(
                    visible=True,
                    range=[0, df[selected_metrics].max().max() * 1.1],
                    gridcolor="#f0f0f0",
                    tickfont=dict(size=10, color="gray"),
                ),
                angularaxis=dict(
                    gridcolor="#f0f0f0",
                    tickfont=dict(size=font_size_label, color="#333", weight="bold")
                )
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom", y=-0.2,
                xanchor="center", x=0.5,
                font=dict(size=font_size_label)
            ),
            margin=dict(l=80, r=80, t=50, b=80),
            height=700
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pilih metrik dan entitas di sidebar.")
else:
    st.warning("Silakan unggah file Excel untuk memulai.")
