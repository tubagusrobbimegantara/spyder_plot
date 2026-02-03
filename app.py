import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. KONFIGURASI HALAMAN & CSS KUSTOM ---
st.set_page_config(
    page_title="Aesthetic Radar Visualizer",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🕸️"
)

# Inject Custom CSS untuk tampilan yang lebih premium
st.markdown("""
    <style>
        /* Mengubah font global */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Styling Header */
        .main .block-container h1 {
            font-weight: 700;
            color: #FFFFFF;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .main .block-container h2, h3 {
            font-weight: 600;
            color: #E0E0E0;
        }

        /* Styling Container Utama agar seperti "Card" */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            background-color: #1E1E2E; /* Warna latar belakang card gelap */
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            border: 1px solid #303045;
        }

        /* Styling Sidebar */
        [data-testid="stSidebar"] {
            background-color: #13131F;
            border-right: 1px solid #303045;
        }

        /* Styling Tabel Dataframe */
        [data-testid="stDataFrame"] {
            border: 1px solid #303045;
            border-radius: 10px;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. JUDUL APLIKASI ---
col_header_1, col_header_2 = st.columns([4, 1])
with col_header_1:
    st.title("🕸️ Neo-Radar Analytics")
    st.markdown("Visualisasi perbandingan multi-variabel dengan estetika modern.")

# --- 3. SIDEBAR: UPLOAD & KONTROL ---
st.sidebar.header("🎛️ Kontrol Data")
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Unggah file Excel (.xlsx)", type=["xlsx"])

# Palet warna neon yang estetik
VIBRANT_PALETTE = ['#00F5D4', '#F15BB5', '#FEE440', '#9B5DE5', '#00BBF9', '#FF6B6B']

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        
        st.sidebar.subheader("🛠️ Konfigurasi")
        
        # Deteksi otomatis kolom
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        object_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Pilihan Kolom Label
        label_col = st.sidebar.selectbox(
            "1️⃣ Pilih kolom Entitas (Label Name):", 
            options=object_cols if object_cols else df.columns,
            index=0
        )
        
        # Pilihan Metrik (Otomatis pilih 5 pertama jika ada)
        default_metrics = numeric_cols[:5] if len(numeric_cols) >= 5 else numeric_cols
        selected_metrics = st.sidebar.multiselect(
            "2️⃣ Pilih Metrik (Kategori Sumbu):", 
            options=numeric_cols, 
            default=default_metrics
        )
        
        # Pilihan Entitas untuk dibandingkan
        if label_col and selected_metrics:
            entities = df[label_col].unique().tolist()
            selected_entities = st.sidebar.multiselect(
                "3️⃣ Pilih Entitas untuk dibandingkan:", 
                options=entities, 
                default=entities[:3] if len(entities) > 2 else entities
            )
        
        st.sidebar.markdown("---")
        st.sidebar.info(f"📊 Data dimuat: {df.shape[0]} baris, {df.shape[1]} kolom.")

        # --- 4. LOGIKA VISUALISASI ---
        if selected_metrics and selected_entities:
            with st.container(): # Container utama untuk hasil
                st.subheader("📈 Hasil Visualisasi")
                
                fig = go.Figure()

                # Cari nilai maksimum global untuk mengatur range sumbu agar konsisten
                global_max = df[selected_metrics].max().max()
                axis_range = [0, global_max * 1.1] # Tambah 10% padding

                for i, entity in enumerate(selected_entities):
                    # Filter data
                    filtered_data = df[df[label_col] == entity][selected_metrics].iloc[0]
                    values = filtered_data.values.tolist()
                    
                    color_idx = i % len(VIBRANT_PALETTE)
                    line_color = VIBRANT_PALETTE[color_idx]

                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=selected_metrics,
                        fill='toself',
                        name=f"<b>{entity}</b>", # Bold name di legenda
                        line=dict(color=line_color, width=3, shape='spline'), # Spline agar garis sedikit melengkung halus
                        marker=dict(
                            size=10, 
                            color=line_color,
                            line=dict(color='white', width=2) # Border putih pada titik agar pop-out
                        ),
                        opacity=0.8,
                        hoverinfo='text+r',
                        text=[f"{m}: {v:.2f}" for m, v in zip(selected_metrics, values)]
                    ))

                # --- KUSTOMISASI LAYOUT PLOTLY YANG ESTETIK ---
                fig.update_layout(
                    template="plotly_dark", # Menggunakan base template gelap
                    paper_bgcolor='rgba(0,0,0,0)', # Latar belakang transparan agar menyatu dengan container Streamlit
                    plot_bgcolor='rgba(0,0,0,0)',
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=axis_range,
                            showticklabels=True,
                            tickfont=dict(color='#AAAAAA', size=10),
                            gridcolor='#444455', # Warna grid radial yang halus
                            gridwidth=1,
                            layer='below traces'
                        ),
                        angularaxis=dict(
                            tickfont=dict(color='white', size=13, weight='bold'), # Font kategori lebih besar & tebal
                            gridcolor='#444455',
                            gridwidth=1.5,
                            layer='below traces'
                        ),
                        bgcolor='rgba(30, 30, 46, 0.5)' # Warna latar belakang area lingkaran dalam
                    ),
                    legend=dict(
                        orientation="h", # Legenda horizontal di bawah
                        yanchor="top", y=-0.15,
                        xanchor="center", x=0.5,
                        font=dict(size=13, color='white'),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    margin=dict(l=80, r=80, t=40, b=120), # Margin disesuaikan untuk legenda di bawah
                    height=650,
                    font=dict(family="Inter, sans-serif")
                )

                # Tampilkan Chart
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                
                # Tampilkan Data Table di dalam expander agar rapi
                with st.expander("🔎 Lihat Data Detail Terpilih"):
                    filtered_df_view = df[df[label_col].isin(selected_entities)][[label_col] + selected_metrics].reset_index(drop=True)
                    st.dataframe(filtered_df_view, use_container_width=True)

        else:
            st.container().warning("⚠️ Mohon pilih setidaknya satu metrik dan satu entitas di sidebar untuk memulai visualisasi.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
        st.markdown("Pastikan format file Excel Anda benar.")

else:
    # --- TAMPILAN AWAL (Landing Page State) ---
    with st.container():
        st.subheader("👋 Selamat Datang!")
        st.markdown("""
            Aplikasi ini mengubah data Excel menjadi grafik radar (spyder chart) yang interaktif dan modern.
            
            **Langkah Mudah:**
            1.  Buka sidebar 👈 di sebelah kiri.
            2.  Unggah file Excel (`.xlsx`) Anda.
            3.  Pilih kolom mana yang menjadi **Nama/Label** dan kolom mana yang menjadi **Nilai/Metrik**.
        """)
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            st.info("💡 **Tips:** Untuk hasil visual terbaik, gunakan data dengan skala nilai yang serupa antar kategorinya (misal: semua skala 1-10, atau semua dalam persen).")
        
        # Contoh tampilan kosong
        fig_empty = go.Figure()
        fig_empty.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(radialaxis=dict(visible=False), angularaxis=dict(visible=False)),
            height=300,
            annotations=[dict(text="Area Grafik Menunggu Data...", x=0.5, y=0.5, font_size=20, showarrow=False, font_color='gray')]
        )
        st.plotly_chart(fig_empty, use_container_width=True, config={'displayModeBar': False})
