import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================================================================
# 1. KONFIGURASI HALAMAN & CSS CUSTOM (TEMA PUTIH-BIRU, RESPONSIF, ELEGAN)
# ==============================================================================
st.set_page_config(page_title="ArcTick - Multi-Ticketing System", page_icon="🎫", layout="wide")

st.markdown("""
<style>
    /* Global Base */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
        color: #1E293B;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Typography & Titles */
    .main-title { 
        font-size: clamp(28px, 4vw, 42px); 
        font-weight: 800; 
        color: #1E40AF; 
        text-align: center; 
        margin-bottom: 8px;
        letter-spacing: -0.05em;
    }
    .sub-title { 
        font-size: clamp(14px, 1.5vw, 18px); 
        color: #64748B; 
        text-align: center; 
        margin-bottom: 35px; 
    }
    
    /* Card layout components (Responsive Containers) */
    .ticket-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .ticket-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(30, 64, 175, 0.1);
        border-color: #BFDBFE;
    }
    
    /* Custom Bot Layout Containers */
    .bot-header {
        background-color: #1E40AF;
        color: #FFFFFF;
        padding: 15px 20px;
        border-radius: 12px 12px 0 0;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .bot-body {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-top: none;
        padding: 20px;
        border-radius: 0 0 12px 12px;
        margin-bottom: 20px;
    }

    /* Buttons override */
    .stButton>button {
        background-color: #2563EB !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        transition: background-color 0.2s !important;
    }
    .stButton>button:hover {
        background-color: #1D4ED8 !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
    }
    
    /* Form Inputs styling alignment */
    div[data-baseweb="input"] {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. INISIALISASI DATABASE SIMULASI (SESSION STATE)
# ==============================================================================
if 'initialized' not in st.session_state:
    st.session_state.users = {
        "admin": {"password": "admin123", "name": "Chief Admin", "role": "admin"},
        "user": {"password": "user123", "name": "Archel", "role": "user"}
    }
    
    st.session_state.tickets = {
        "Pesawat": [
            {"id": "P01", "kategori": "Ekonomi", "nama": "Garuda Indonesia GA-204 (JKT - SUB)", "harga": 1200000, "stok": 50},
            {"id": "P02", "kategori": "Ekonomi", "nama": "Lion Air JT-512 (JKT - DPS)", "harga": 850000, "stok": 80},
            {"id": "P03", "kategori": "Ekonomi", "nama": "Citilink QG-142 (JKT - JOG)", "harga": 700000, "stok": 60},
            {"id": "P04", "kategori": "Bisnis", "nama": "Batik Air ID-6572 (JKT - MES)", "harga": 2500000, "stok": 20},
            {"id": "P05", "kategori": "Bisnis", "nama": "Garuda Indonesia GA-312 (JKT - SUB)", "harga": 3400000, "stok": 15},
            {"id": "P06", "kategori": "Bisnis", "nama": "Singapore Airlines SQ-939 (JKT - SIN)", "harga": 5500000, "stok": 12},
            {"id": "P07", "kategori": "First Class", "nama": "Garuda Indonesia GA-100 (JKT - LHR)", "harga": 15000000, "stok": 4},
            {"id": "P08", "kategori": "First Class", "nama": "Emirates EK-357 (JKT - DXB)", "harga": 22000000, "stok": 6},
            {"id": "P09", "kategori": "First Class", "nama": "Qatar Airways QR-955 (JKT - DOH)", "harga": 19500000, "stok": 5},
        ],
        "Kereta Api": [
            {"id": "K01", "kategori": "Ekonomi", "nama": "Airlangga 236 (PSE - SBI)", "harga": 104000, "stok": 120},
            {"id": "K02", "kategori": "Ekonomi", "nama": "Bengawan 246 (PSE - PWS)", "harga": 74000, "stok": 100},
            {"id": "K03", "kategori": "Ekonomi", "nama": "Serayu 252 (GMR - PWT)", "harga": 67000, "stok": 90},
            {"id": "K04", "kategori": "Bisnis", "nama": "Senja Utama Yk 140 (GMR - YK)", "harga": 280000, "stok": 40},
            {"id": "K05", "kategori": "Bisnis", "nama": "Sawunggalih 154 (PSE - KTA)", "harga": 260000, "stok": 50},
            {"id": "K06", "kategori": "Bisnis", "nama": "Gajahwong 138 (PSE - LPN)", "harga": 290000, "stok": 45},
            {"id": "K07", "kategori": "Eksekutif", "nama": "Argo Bromo Anggrek 2 (GMR - SBI)", "harga": 650000, "stok": 30},
            {"id": "K08", "kategori": "Eksekutif", "nama": "Argo Lawu 8 (GMR - SLO)", "harga": 580000, "stok": 25},
            {"id": "K09", "kategori": "Eksekutif", "nama": "Taksaka 68 (GMR - YK)", "harga": 550000, "stok": 35},
        ],
        "Wisata": [
            {"id": "W01", "kategori": "Lokal", "nama": "Tiket Masuk Candi Borobudur", "harga": 50000, "stok": 1000},
            {"id": "W02", "kategori": "Lokal", "nama": "Tiket Masuk Dufan Ancol", "harga": 275000, "stok": 500},
            {"id": "W03", "kategori": "Lokal", "nama": "Tiket Ragunan Zoo Jakarta", "harga": 4000, "stok": 2000},
            {"id": "W04", "kategori": "Mancanegara", "nama": "Universal Studios Singapore", "harga": 950000, "stok": 200},
            {"id": "W05", "kategori": "Mancanegara", "nama": "Disneyland Tokyo", "harga": 1100000, "stok": 150},
            {"id": "W06", "kategori": "Mancanegara", "nama": "Louvre Museum Paris", "harga": 380000, "stok": 300},
            {"id": "W07", "kategori": "Premium / VIP", "nama": "VIP Fast Track Dufan Pass", "harga": 650000, "stok": 50},
            {"id": "W08", "kategori": "Premium / VIP", "nama": "Bali Safari Marine Park Rhino Package", "harga": 1750000, "stok": 20},
            {"id": "W09", "kategori": "Premium / VIP", "nama": "Lombok Private Island Cruise Tour", "harga": 3200000, "stok": 15},
        ]
    }
    st.session_state.history_transaksi = []
    st.session_state.current_user = None
    st.session_state.initialized = True

if 'cart' not in st.session_state:
    st.session_state.cart = []

# ==============================================================================
# 3. ENGINE TEORI BAHASA & OTOMATA (FSA + LEVENSHTEIN ANTI-TYPO)
# ==============================================================================
def levenshtein_distance(s1, s2):
    s1, s2 = s1.lower(), s2.lower()
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def perbaiki_input(user_input, daftar_pilihan, threshold=3):
    user_input = user_input.strip().lower()
    terbaik = None
    min_jarak = float('inf')
    for pilihan in daftar_pilihan:
        jarak = levenshtein_distance(user_input, pilihan)
        if jarak < min_jarak:
            min_jarak = jarak
            terbaik = pilihan
    if min_jarak <= threshold:
        return terbaik
    return None

class ArcBotFSA:
    def __init__(self):
        self.state = "START"
        self.selected_jenis = None
        self.selected_kategori = None
        self.selected_tiket = None
        self.response = "Halo! Selamat datang di **ArcTick**. Saya **ArcBot** 🤖.\n\nSilakan ketik tipe perjalanan atau liburan yang Anda inginkan:\n- **Pesawat**\n- **Kereta Api**\n- **Wisata**"

    def step(self, user_input=None):
        if not user_input:
            return

        if self.state == "START":
            pilihan_jenis = ["pesawat", "kereta api", "wisata"]
            cocok = perbaiki_input(user_input, pilihan_jenis)
            
            if cocok:
                self.selected_jenis = "Pesawat" if cocok == "pesawat" else "Kereta Api" if cocok == "kereta api" else "Wisata"
                self.state = "PILIH_KATEGORI"
                kategori_list = list(set([t['kategori'] for t in st.session_state.tickets[self.selected_jenis]]))
                kat_str = ", ".join([f"**{k}**" for k in kategori_list])
                self.response = f"Mencari armada **{self.selected_jenis}**? Pilihan kelas/kategori yang tersedia:\n{kat_str}\n\nSilakan ketik nama kategori pilihan Anda."
            else:
                self.response = "Maaf, ArcBot belum mengenali tipe tiket tersebut. Silakan ketik salah satu pilihan berikut: **Pesawat**, **Kereta Api**, atau **Wisata**."

        elif self.state == "PILIH_KATEGORI":
            kategori_list = list(set([t['kategori'] for t in st.session_state.tickets[self.selected_jenis]]))
            kategori_lowercase = [k.lower() for k in kategori_list]
            cocok = perbaiki_input(user_input, kategori_lowercase)
            
            if cocok:
                idx = kategori_lowercase.index(cocok)
                self.selected_kategori = kategori_list[idx]
                self.state = "PILIH_ITEM"
                items = [t for t in st.session_state.tickets[self.selected_jenis] if t['kategori'] == self.selected_kategori]
                item_str = "\n".join([f"- **{t['id']}**: {t['nama']} (Rp {t['harga']:,})" for t in items])
                self.response = f"Berikut daftar jadwal / opsi tiket **{self.selected_jenis}** [{self.selected_kategori}] yang siap dipesan:\n\n{item_str}\n\nSilakan masukkan **Kode ID Tiket** (Contoh: P01, K04, W02) untuk memilih item."
            else:
                kat_str = ", ".join([f"**{k}**" for k in kategori_list])
                self.response = f"Kategori tidak sesuai. Silakan ketik ulang kategori yang valid berikut ini: {kat_str}"

        elif self.state == "PILIH_ITEM":
            items = [t for t in st.session_state.tickets[self.selected_jenis] if t['kategori'] == self.selected_kategori]
            id_list = [t['id'].lower() for t in items]
            user_input_clean = user_input.strip().lower()
            
            if user_input_clean in id_list:
                idx = id_list.index(user_input_clean)
                self.selected_tiket = items[idx]
                self.state = "KONFIRMASI"
                self.response = f"Konfirmasi Pemilihan:\n**{self.selected_tiket['nama']}**\nHarga: **Rp {self.selected_tiket['harga']:,}**\n\nKetik **Beli** untuk menambahkan ke keranjang, atau ketik **Batal** untuk membatalkan."
            else:
                self.response = "Kode ID Tiket tidak terdaftar di daftar atas. Mohon periksa kembali kodenya dan ketik dengan benar."

        elif self.state == "KONFIRMASI":
            cocok = perbaiki_input(user_input, ["beli", "batal"])
            if cocok == "beli":
                if self.selected_tiket['stok'] > 0:
                    st.session_state.cart.append({
                        "id": self.selected_tiket['id'],
                        "nama": self.selected_tiket['nama'],
                        "harga": self.selected_tiket['harga'],
                        "qty": 1
                    })
                    self.response = f"🎉 Sukses! **{self.selected_tiket['nama']}** berhasil ditambahkan ke keranjang belanja Anda.\n\nIngin memesan lagi? Silakan ketik pilihan baru Anda: **Pesawat**, **Kereta Api**, atau **Wisata**."
                else:
                    self.response = "Waduh, stok alokasi tiket baru saja habis. Silakan ketik **Batal** untuk mencari rute atau alternatif lainnya."
                self.state = "START"
            elif cocok == "batal":
                self.state = "START"
                self.response = "Proses pemilihan dibatalkan oleh pengguna. Mari kita mulai lagi. Silakan ketik tipe tiket: **Pesawat**, **Kereta Api**, atau **Wisata**."
            else:
                self.response = "Mohon berikan jawaban yang pasti. Ketik **Beli** untuk setuju atau **Batal** untuk membatalkan item ini."

if 'arcbot' not in st.session_state:
    st.session_state.arcbot = ArcBotFSA()
    st.session_state.chat_history = [{"role": "assistant", "content": st.session_state.arcbot.response}]

# ==============================================================================
# 4. SISTEM INTERFACE & ROUTING HALAMAN
# ==============================================================================
if st.session_state.current_user is None:
    st.markdown("<div class='main-title'>🎫 ArcTick Hub</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Platform Reservasi Multi-Tiket Cerdas & Responsif</div>", unsafe_allow_html=True)
    
    col_auth_center = st.columns([1, 2, 1])
    with col_auth_center[1]:
        auth_tab = st.tabs(["🔒 Masuk Akun", "📝 Registrasi Baru"])
        
        with auth_tab[0]:
            login_user = st.text_input("Username", key="login_u")
            login_pass = st.text_input("Password", type="password", key="login_p")
            if st.button("Masuk Aplikasi"):
                if login_user in st.session_state.users and st.session_state.users[login_user]["password"] == login_pass:
                    st.session_state.current_user = login_user
                    st.success(f"Selamat datang kembali, {st.session_state.users[login_user]['name']}!")
                    st.rerun()
                else:
                    st.error("Identitas login tidak cocok!")
                    
        with auth_tab[1]:
            reg_user = st.text_input("Buat Username", key="reg_u")
            reg_name = st.text_input("Nama Lengkap Terdisplay", key="reg_n")
            reg_pass = st.text_input("Buat Password", type="password", key="reg_p")
            if st.button("Selesaikan Pendaftaran"):
                if reg_user in st.session_state.users:
                    st.error("Username ini sudah diklaim pengguna lain!")
                elif not reg_user or not reg_pass or not reg_name:
                    st.error("Mohon isi seluruh baris kolom registrasi!")
                else:
                    st.session_state.users[reg_user] = {"password": reg_pass, "name": reg_name, "role": "user"}
                    st.success("Akun terdaftar! Silakan beralih ke tab Masuk Akun.")

else:
    user_info = st.session_state.users[st.session_state.current_user]
    
    # Sidebar Responsive Navigation
    st.sidebar.markdown(f"<div style='padding: 10px 0;'><h4>👤 {user_info['name']}</h4><p style='color:#64748B; font-size:13px;'>Sesi: {user_info['role'].upper()}</p></div>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    if user_info["role"] == "admin":
        menu = st.sidebar.radio("Panel Navigasi", ["Dashboard Analitik", "Manajemen Tiket", "Log Transaksi Pengguna", "Pengaturan Profil"])
    else:
        menu = st.sidebar.radio("Panel Navigasi", ["Katalog Tiket", "Asisten ArcBot 🤖", "Keranjang Belanja", "Riwayat Pemesanan", "Pengaturan Profil"])
        
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Log Out / Keluar"):
        st.session_state.current_user = None
        st.rerun()

    # ==============================================================================
    # 5. HALAMAN PELANGGAN (USER INTERFACE)
    # ==============================================================================
    if menu == "Katalog Tiket":
        st.markdown("<div class='main-title'>Katalog Tiket</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Temukan tiket perjalanan terbaik dengan harga transparan</div>", unsafe_allow_html=True)
        
        jenis_tab = st.tabs(["✈️ Penerbangan", "🚊 Kereta Api", "🏞️ Destinasi Wisata"])
        
        for idx, jenis in enumerate(["Pesawat", "Kereta Api", "Wisata"]):
            with jenis_tab[idx]:
                kategori_list = list(set([t['kategori'] for t in st.session_state.tickets[jenis]]))
                for kat in kategori_list:
                    st.markdown(f"<h4 style='color:#1E40AF; margin-top:15px;'>Kelas / Zona: {kat}</h4>", unsafe_allow_html=True)
                    items = [t for t in st.session_state.tickets[jenis] if t['kategori'] == kat]
                    
                    # Responsiveness using dynamic grid mapping
                    cols = st.columns(3)
                    for i, item in enumerate(items):
                        with cols[i % 3]:
                            st.markdown(f"""
                            <div class="ticket-card">
                                <span style="background-color:#DBEAFE; color:#1E40AF; font-size:11px; padding:3px 8px; border-radius:5px; font-weight:bold;">{item['id']}</span>
                                <h5 style="margin: 10px 0 5px 0; font-weight:600;">{item['nama']}</h5>
                                <p style="color:#2563EB; font-weight:700; font-size:20px; margin:5px 0;">Rp {item['harga']:,}</p>
                                <p style="font-size:12px; color:#64748B; margin-bottom:15px;">Alokasi Sisa Kursi: <b>{item['stok']}</b></p>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button("Pesan Tiket Ini", key=f"btn_katalog_{item['id']}"):
                                if item['stok'] > 0:
                                    st.session_state.cart.append({"id": item['id'], "nama": item['nama'], "harga": item['harga'], "qty": 1})
                                    st.toast(f"Berhasil ditambahkan ke keranjang: {item['nama']}")
                                else:
                                    st.error("Mohon maaf, tiket rute ini telah penuh!")

    elif menu == "Asisten ArcBot 🤖":
        st.markdown("<div class='main-title'>Asisten Cerdas ArcBot</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Konsultasikan dan pesan tiket otomatis bebas dari kesalahan pengetikan</div>", unsafe_allow_html=True)
        
        col_chat, col_status = st.columns([2, 1])
        
        with col_status:
            # Tampilan Status Alur Obrolan yang Terbuka dan Bersih tanpa penulisan State Mesin Teknis internal
            st.markdown("""
            <div class='bot-header'>
                <span>📈 Alur Percakapan Terpandu</span>
            </div>
            """, unsafe_allow_html=True)
            with st.container():
                st.markdown(f"""
                <div class='bot-body'>
                    <p style='margin-bottom:8px;'><b>Kategori Sektor Aktif:</b><br><span style='color:#2563EB;'>{st.session_state.arcbot.selected_jenis or 'Menunggu pilihan...'}</span></p>
                    <p style='margin-bottom:0;'><b>Kelas Perjalanan Aktif:</b><br><span style='color:#2563EB;'>{st.session_state.arcbot.selected_kategori or 'Menunggu pilihan...'}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
            if st.button("Segarkan Ulang Percakapan"):
                st.session_state.arcbot = ArcBotFSA()
                st.session_state.chat_history = [{"role": "assistant", "content": st.session_state.arcbot.response}]
                st.rerun()
                
        with col_chat:
            chat_container = st.container(height=450)
            with chat_container:
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
                        
            if prompt := st.chat_input("Ketik instruksi pemesanan Anda di sini (misal: pswat, kreta)..."):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state.arcbot.step(prompt)
                st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.arcbot.response})
                st.rerun()

    elif menu == "Keranjang Belanja":
        st.markdown("<div class='main-title'>Keranjang Belanja</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Periksa kembali tiket pesanan Anda sebelum melakukan konfirmasi pembayaran</div>", unsafe_allow_html=True)
        
        if not st.session_state.cart:
            st.info("Keranjang Anda saat ini kosong. Pilih tiket rute terbaik di Katalog atau melalui ArcBot!")
        else:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.dataframe(df_cart, use_container_width=True, hide_index=True)
            
            total_bayar = sum([x['harga'] * x['qty'] for x in st.session_state.cart])
            st.markdown(f"<h3 style='text-align:right; color:#1E40AF;'>Total Pembayaran: Rp {total_bayar:,}</h3>", unsafe_allow_html=True)
            
            col_actions = st.columns([1, 1])
            with col_actions[0]:
                if st.button("Kosongkan Isi Keranjang"):
                    st.session_state.cart = []
                    st.rerun()
            with col_actions[1]:
                if st.button("Konfirmasi & Bayar Sekarang"):
                    for c_item in st.session_state.cart:
                        for j_key in st.session_state.tickets:
                            for t_item in st.session_state.tickets[j_key]:
                                if t_item['id'] == c_item['id']:
                                    t_item['stok'] -= 1
                                    
                    st.session_state.history_transaksi.append({
                        "Pelanggan": st.session_state.current_user,
                        "Waktu Transaksi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Rincian Tiket": ", ".join([f"{x['nama']} (x{x['qty']})" for x in st.session_state.cart]),
                        "Total Biaya": total_bayar
                    })
                    st.session_state.cart = []
                    st.success("🎉 Reservasi Berhasil! E-Tiket resmi Anda telah diterbitkan. Silakan cek menu Riwayat.")

    elif menu == "Riwayat Pemesanan":
        st.markdown("<div class='main-title'>Riwayat Pemesanan</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Daftar berkas invoice dokumen digital perjalanan Anda</div>", unsafe_allow_html=True)
        
        user_trx = [x for x in st.session_state.history_transaksi if x['Pelanggan'] == st.session_state.current_user]
        if not user_trx:
            st.info("Belum ditemukan riwayat pemesanan atas nama akun Anda.")
        else:
            st.dataframe(pd.DataFrame(user_trx), use_container_width=True, hide_index=True)

    # ==============================================================================
    # 6. PANEL KONTROL MANAJEMEN SISTEM (ADMIN INTERFACE)
    # ==============================================================================
    elif menu == "Dashboard Analitik" and user_info["role"] == "admin":
        st.markdown("<div class='main-title'>Dashboard Analitik</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Ringkasan grafik operasional server utama ArcTick</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        tot_user = len(st.session_state.users)
        tot_item = sum([len(st.session_state.tickets[k]) for k in st.session_state.tickets])
        tot_omset = sum([x['Total Biaya'] for x in st.session_state.history_transaksi])
        
        with c1:
            st.metric("Pengguna Terdaftar", f"{tot_user} Akun")
        with c2:
            st.metric("Varian Rute Sektor", f"{tot_item} Rute")
        with c3:
            st.metric("Omset Penjualan", f"Rp {tot_omset:,}")

    elif menu == "Manajemen Tiket" and user_info["role"] == "admin":
        st.markdown("<div class='main-title'>Manajemen Tiket</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Panel terpusat pengelola persediaan, modifikasi rute, dan katalog entitas tiket</div>", unsafe_allow_html=True)
        
        opsi_aksi = st.radio("Pilih Opsi Pengelolaan Data", ["Lihat Seluruh Tiket", "Tambahkan Tiket Baru", "Perbarui Rincian Tiket", "Hapus Tiket Eksisting"], horizontal=True)
        jenis_pilih = st.selectbox("Pilih Jenis Komoditas Perjalanan", ["Pesawat", "Kereta Api", "Wisata"])
        
        if opsi_aksi == "Lihat Seluruh Tiket":
            df_view = pd.DataFrame(st.session_state.tickets[jenis_pilih])
            st.dataframe(df_view, use_container_width=True, hide_index=True)
            
        elif opsi_aksi == "Tambahkan Tiket Baru":
            st.subheader(f"Input Formulir Baru - Sektor {jenis_pilih}")
            c_id = st.text_input("Kode Unik Tiket Baru (Contoh: P10 / K10 / W10)")
            c_kat = st.text_input("Nama Kategori / Kelas")
            c_nama = st.text_input("Nama Rute / Armada / Lokasi Wisata Lengkap")
            c_harga = st.number_input("Besaran Tarif Nilai Rupiah", min_value=0, step=10000)
            c_stok = st.number_input("Kuantitas Batas Maksimal Kuota Stok", min_value=0, step=1)
            
            if st.button("Simpan Data ke Database"):
                if c_id and c_kat and c_nama:
                    st.session_state.tickets[jenis_pilih].append({
                        "id": c_id, "kategori": c_kat, "nama": c_nama, "harga": c_harga, "stok": c_stok
                    })
                    st.success("Sukses menyimpan pembaruan entitas baru ke sistem utama.")
                else:
                    st.error("Gagal! Semua kolom wajib terisi.")
                
        elif opsi_aksi == "Perbarui Rincian Tiket":
            st.subheader(f"Formulir Penyesuaian Data - Sektor {jenis_pilih}")
            list_id = [t['id'] for t in st.session_state.tickets[jenis_pilih]]
            select_id = st.selectbox("Pilih Kode ID Tiket Target", list_id)
            
            item_ref = next(t for t in st.session_state.tickets[jenis_pilih] if t['id'] == select_id)
            u_kat = st.text_input("Sesuaikan Kategori Kelas", value=item_ref['kategori'])
            u_nama = st.text_input("Sesuaikan Nama Armada / Lokasi Wisata", value=item_ref['nama'])
            u_harga = st.number_input("Sesuaikan Harga Jual Terbaru", min_value=0, value=item_ref['harga'], step=10000)
            u_stok = st.number_input("Sesuaikan Total Alokasi Ketersediaan Kursi", min_value=0, value=item_ref['stok'], step=1)
            
            if st.button("Terapkan Perubahan Rincian"):
                item_ref['kategori'] = u_kat
                item_ref['nama'] = u_nama
                item_ref['harga'] = u_harga
                item_ref['stok'] = u_stok
                st.success(f"Pembaruan data rute ID {select_id} sukses disimpan!")

        elif opsi_aksi == "Hapus Tiket Eksisting":
            st.subheader(f"Penghapusan Data dari Sistem Inventori - Sektor {jenis_pilih}")
            list_id = [t['id'] for t in st.session_state.tickets[jenis_pilih]]
            select_id = st.selectbox("Pilih ID Tiket yang akan dieliminasi permanen", list_id)
            
            if st.button("Eksekusi Hapus Permanen"):
                st.session_state.tickets[jenis_pilih] = [t for t in st.session_state.tickets[jenis_pilih] if t['id'] != select_id]
                st.warning(f"Data berkas tiket dengan ID {select_id} resmi dihilangkan dari katalog.")

    elif menu == "Log Transaksi Pengguna" and user_info["role"] == "admin":
        st.markdown("<div class='main-title'>Log Transaksi Global</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Audit riwayat pembayaran transaksi yang dilakukan seluruh pengguna aplikasi</div>", unsafe_allow_html=True)
        
        if not st.session_state.history_transaksi:
            st.info("Arsip transaksi kosong. Belum ada aktivitas transaksi masuk dari pelanggan.")
        else:
            st.dataframe(pd.DataFrame(st.session_state.history_transaksi), use_container_width=True, hide_index=True)

    # ==============================================================================
    # 7. MANAJEMEN PENGATURAN PROFIL GLOBAL (USER & ADMIN)
    # ==============================================================================
    elif menu == "Pengaturan Profil":
        st.markdown("<div class='main-title'>Pengaturan Profil</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Kelola preferensi dan rahasia kredensial akun personal Anda</div>", unsafe_allow_html=True)
        
        curr_username = st.session_state.current_user
        
        col_prof_center = st.columns([1, 2, 1])
        with col_prof_center[1]:
            new_name = st.text_input("Ubah Nama Tampilan Akun", value=st.session_state.users[curr_username]['name'])
            new_pass = st.text_input("Ubah Password Baru Anda", value=st.session_state.users[curr_username]['password'], type="password")
            
            if st.button("Simpan Perubahan Akun"):
                if new_name and new_pass:
                    st.session_state.users[curr_username]['name'] = new_name
                    st.session_state.users[curr_username]['password'] = new_pass
                    st.success("Profil akun Anda berhasil dimodifikasi dan telah diperbarui secara langsung!")
                else:
                    st.error("Pengisian kolom nama dan password tidak boleh dikosongkan.")