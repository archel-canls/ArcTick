import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ==============================================================================
# 1. PREMIUM BRANDING & ADVANCED CSS (RESPONSIVE WHITE-BLUE THEME)
# ==============================================================================
st.set_page_config(page_title="ArcTick | Enterprise Ticketing Management", page_icon="🎫", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Reset & Base Typography */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #0A2540 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Clean Header Blueprint */
    header[data-testid="stHeader"] {
        background-color: #0A2540 !important;
        border-bottom: 2px solid #635BFF;
    }
    
    /* Navigation Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* Corporate Typography Design */
    .brand-title {
        font-size: 34px;
        font-weight: 800;
        color: #0A2540;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }
    .brand-subtitle {
        font-size: 15px;
        color: #627D98;
        margin-bottom: 30px;
    }
    
    /* Cards Layout Architecture */
    .saas-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.02), 0px 12px 32px rgba(0, 0, 0, 0.03);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .saas-card:hover {
        border-color: #635BFF;
        transform: translateY(-2px);
        box-shadow: 0px 4px 8px rgba(99, 91, 255, 0.04), 0px 16px 40px rgba(99, 91, 255, 0.08);
    }
    
    /* Custom Modern Dynamic Chat Bubbles */
    .bubble-assistant {
        background-color: #F1F5F9;
        color: #0A2540;
        padding: 14px 18px;
        border-radius: 4px 16px 16px 16px;
        margin-bottom: 12px;
        line-height: 1.5;
        border-left: 3px solid #635BFF;
    }
    .bubble-user {
        background-color: #635BFF;
        color: #FFFFFF;
        padding: 14px 18px;
        border-radius: 16px 16px 4px 16px;
        margin-bottom: 12px;
        line-height: 1.5;
        text-align: right;
    }
    
    /* Standardized Buttons to Match SaaS Framework */
    .stButton>button {
        background-color: #635BFF !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 22px !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #4B44E0 !important;
        transform: translateY(-1px);
    }
    
    /* Responsive Navigation Wrapper */
    .menu-container {
        background: #F1F5F9;
        padding: 6px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SEED DATA & STATE ENGINE INITIALIZATION
# ==============================================================================
if 'initialized' not in st.session_state:
    st.session_state.users = {
        "admin": {"password": "admin123", "name": "System Administrator", "role": "admin"},
        "user": {"password": "user123", "name": "Archel", "role": "user"}
    }
    
    st.session_state.tickets = {
        "Pesawat": [
            {"id": "P01", "kategori": "Ekonomi", "nama": "Garuda Indonesia GA-204 (JKT - SUB)", "harga": 1200000, "stok": 50},
            {"id": "P02", "kategori": "Ekonomi", "nama": "Lion Air JT-512 (JKT - DPS)", "harga": 850000, "stok": 80},
            {"id": "P03", "kategori": "Ekonomi", "nama": "Citilink QG-142 (JKT - JOG)", "harga": 700000, "stok": 60},
            {"id": "P04", "kategori": "Bisnis", "nama": "Batik Air ID-6572 (JKT - MES)", "harga": 2500000, "stok": 20},
            {"id": "P05", "kategori": "Bisnis", "nama": "Garuda Indonesia GA-312 (JKT - SUB)", "harga": 3400000, "stok": 15},
        ],
        "Kereta Api": [
            {"id": "K01", "kategori": "Ekonomi", "nama": "Airlangga 236 (PSE - SBI)", "harga": 104000, "stok": 120},
            {"id": "K02", "kategori": "Ekonomi", "nama": "Bengawan 246 (PSE - PWS)", "harga": 74000, "stok": 100},
            {"id": "K07", "kategori": "Eksekutif", "nama": "Argo Bromo Anggrek 2 (GMR - SBI)", "harga": 650000, "stok": 30},
            {"id": "K08", "kategori": "Eksekutif", "nama": "Argo Lawu 8 (GMR - SLO)", "harga": 580000, "stok": 25},
        ],
        "Wisata": [
            {"id": "W01", "kategori": "Lokal", "nama": "Tiket Masuk Candi Borobudur", "harga": 50000, "stok": 1000},
            {"id": "W02", "kategori": "Lokal", "nama": "Tiket Masuk Dufan Ancol", "harga": 275000, "stok": 500},
            {"id": "W07", "kategori": "VIP", "nama": "VIP Fast Track Dufan Pass", "harga": 650000, "stok": 50},
        ]
    }
    st.session_state.history_transaksi = []
    st.session_state.current_user = None
    st.session_state.applied_promo = None
    st.session_state.vouchers = {"PROMOHEBAT": 50000, "ARCHELTIK": 100000}
    st.session_state.initialized = True

if 'cart' not in st.session_state:
    st.session_state.cart = []

# ==============================================================================
# 3. ADVANCED NLP SIMULATION ENGINE (VARIED RESPONSES LIKE GEMINI)
# ==============================================================================
def levenshtein_distance(s1, s2):
    s1, s2 = s1.lower(), s2.lower()
    if len(s1) < len(s2): return levenshtein_distance(s2, s1)
    if len(s2) == 0: return len(s1)
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
    if min_jarak <= threshold: return terbaik
    return None

class ArcBotGenerativeFSA:
    def __init__(self):
        self.state = "START"
        self.selected_jenis = None
        self.selected_kategori = None
        self.selected_tiket = None
        self.response = "Halo! Saya ArcBot. Silakan sebutkan jenis tiket yang ingin Anda cari saat ini: **Pesawat**, **Kereta Api**, atau **Wisata**."

    def step(self, user_input=None):
        if not user_input: return
        
        # Kumpulan respons variatif gaya LLM / Gemini agar tidak monoton
        rancu_responses = [
            "Saya kurang menangkap maksud Anda. Bisa sebutkan kategori spesifik seperti Pesawat, Kereta Api, atau Wisata?",
            "Hmm, instruksi tersebut agak kurang jelas bagi saya. Apakah Anda sedang mencari tiket Pesawat, Kereta Api, atau destinasi Wisata?",
            "Maaf, saya belum memahami kalimat itu. Coba ketik pilihan layanan yang tersedia: Pesawat, Kereta Api, atau Wisata agar saya bisa membantu.",
            "Bisa dipermudah pertanyaannya? Saya dikonfigurasi untuk membantu pemesanan tiket Pesawat, Kereta Api, dan Wisata."
        ]
        
        if self.state == "START":
            pilihan_jenis = ["pesawat", "kereta api", "wisata"]
            cocok = perbaiki_input(user_input, pilihan_jenis)
            
            if cocok:
                self.selected_jenis = "Pesawat" if cocok == "pesawat" else "Kereta Api" if cocok == "kereta api" else "Wisata"
                self.state = "PILIH_KATEGORI"
                kategori_list = list(set([t['kategori'] for t in st.session_state.tickets[self.selected_jenis]]))
                kat_str = ", ".join([f"**{k}**" for k in kategori_list])
                
                success_responses = [
                    f"Baik, pencarian diarahkan ke armada **{self.selected_jenis}**. Untuk mempermudah, kelas/kategori apa yang Anda inginkan? Tersedia kelas: {kat_str}.",
                    f"Siap! Mari kita lihat opsi untuk **{self.selected_jenis}**. Kategori yang bisa Anda pilih saat ini adalah: {kat_str}. Mana rute yang Anda minati?",
                    f"Membuka portal reservasi **{self.selected_jenis}**. Silakan tentukan tingkatan kelas berikut: {kat_str}."
                ]
                self.response = random.choice(success_responses)
            else:
                self.response = random.choice(rancu_responses)

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
                
                kat_success = [
                    f"Menampilkan seluruh opsi aktif pada kategori **{self.selected_kategori}**:\n\n{item_str}\n\nMasukkan salah satu **Kode ID** di atas untuk langsung mengunci pilihan.",
                    f"Berikut opsi manifes jadwal untuk kelas **{self.selected_kategori}**:\n\n{item_str}\n\nTuliskan **Kode Tiket** yang ingin Anda ambil.",
                ]
                self.response = random.choice(kat_success)
            else:
                kat_str = ", ".join([f"**{k}**" for k in kategori_list])
                self.response = f"Pilihan kelas tidak sesuai. Harap masukkan opsi yang valid berikut ini: {kat_str}"

        elif self.state == "PILIH_ITEM":
            items = [t for t in st.session_state.tickets[self.selected_jenis] if t['kategori'] == self.selected_kategori]
            id_list = [t['id'].lower() for t in items]
            user_input_clean = user_input.strip().lower()
            
            if user_input_clean in id_list:
                idx = id_list.index(user_input_clean)
                self.selected_tiket = items[idx]
                self.state = "KONFIRMASI"
                self.response = f"Berikut ringkasan pesanan Anda:\n\n**{self.selected_tiket['nama']}**\nTarif: *Rp {self.selected_tiket['harga']:,}*\n\nKetik **Beli** jika rincian sudah sesuai, atau ketik **Batal** untuk mereset."
            else:
                self.response = "Kode ID Tiket yang Anda ketik tidak ditemukan dalam daftar terlampir. Coba periksa kembali kombinasinya."

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
                    self.response = f"🎉 Berhasil! **{self.selected_tiket['nama']}** telah ditambahkan ke keranjang belanja.\n\nAda rencana perjalanan lain? Sila ketik **Pesawat**, **Kereta Api**, atau **Wisata** kembali."
                else:
                    self.response = "Mohon maaf, kuota alokasi kursi untuk tiket ini mendadak habis. Silakan ketik **Batal** untuk mereset pencarian."
                self.state = "START"
            elif cocok == "batal":
                self.state = "START"
                self.response = "Proses registrasi tiket dibatalkan. Mari kita mulai pencarian dari awal kembali. Ketik **Pesawat**, **Kereta Api**, atau **Wisata**."
            else:
                self.response = "Instruksi tidak sah. Harap ketik **Beli** untuk validasi masuk keranjang atau **Batal** untuk membuang entitas."

if 'arcbot' not in st.session_state:
    st.session_state.arcbot = ArcBotGenerativeFSA()
    st.session_state.chat_history = [{"role": "assistant", "content": st.session_state.arcbot.response}]

# ==============================================================================
# 4. RESPONSIVE BURGER MENU DETECTOR (SMARTPHONE WRAPPER)
# ==============================================================================
is_mobile = st.columns([1, 4, 1])[1] # Mock responsivitas kolom tengah

# ==============================================================================
# 5. AUTHENTICATION HUB (CLEAN CORPORATE LOOK - NO AI ICONS)
# ==============================================================================
if st.session_state.current_user is None:
    st.markdown("<div style='text-align:center; padding: 40px 0 10px 0;'><span class='brand-title'>ArcTick Terminal</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><p class='brand-subtitle'>Integrated Logistics & Ticket Management Network System</p></div>", unsafe_allow_html=True)
    
    col_layout = st.columns([1.2, 1, 1.2])
    with col_layout[1]:
        # Gambar Interaktif dari Unsplash Link CDN menggantikan icon buatan AI standar
        st.image("https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80&w=600", use_container_width=True)
        
        tab_portal = st.tabs(["Sign In Platform", "Create Enterprise Account"])
        with tab_portal[0]:
            u_entry = st.text_input("User Core Identification", placeholder="Username")
            p_entry = st.text_input("Security Core Key", type="password", placeholder="Password")
            if st.button("Authorize Access", use_container_width=True):
                if u_entry in st.session_state.users and st.session_state.users[u_entry]["password"] == p_entry:
                    st.session_state.current_user = u_entry
                    st.rerun()
                else:
                    st.error("Authentication Failure: Invalid Key Access.")
        with tab_portal[1]:
            reg_u = st.text_input("Register New ID", placeholder="Ex: archel99")
            reg_n = st.text_input("Legal Full Name", placeholder="Ex: Archel Hardani")
            reg_p = st.text_input("Configure Secure Password", type="password", placeholder="Minimal 6 Character")
            if st.button("Deploy Account Data", use_container_width=True):
                if reg_u in st.session_state.users:
                    st.error("Identity Duplicate: ID already recorded.")
                elif not reg_u or not reg_p:
                    st.error("Submission Halted: Required fields cannot empty.")
                else:
                    st.session_state.users[reg_u] = {"password": reg_p, "name": reg_n, "role": "user"}
                    st.success("Provisioning Successful! Switch to Sign In portal.")

# ==============================================================================
# 6. MAIN ENTERPRISE DESKTOP & BURGER MOBILE ENGINE
# ==============================================================================
else:
    user_info = st.session_state.users[st.session_state.current_user]
    
    # Pendeteksian Menu Hamburger / Dropdown Responsif di Smartphone
    st.markdown("<div class='menu-container'>", unsafe_allow_html=True)
    if user_info["role"] == "admin":
        list_nav = ["Dashboard Analitik", "Manajemen Tiket", "Log Transaksi Pengguna", "Pengaturan Profil"]
    else:
        list_nav = ["Katalog Inventori Tiket", "Asisten Interaktif ArcBot", "Manajemen Keranjang Belanja", "Arsip Riwayat Pemesanan", "Pengaturan Profil"]
        
    # Element Dropdown Burger Menu (Dipasang di area atas agar responsif saat dibuka di Android/iOS)
    chosen_menu = st.selectbox("☰ Navigation Menu (Responsive Hub)", list_nav)
    st.markdown("</div>", unsafe_allow_html=True)

    # Sidebar Data Metadata Tetap Berjalan di Monitor Besar
    with st.sidebar:
        st.markdown(f"### Core Node: {user_info['name']}")
        st.markdown(f"Access Priority Level: `{user_info['role'].upper()}`")
        st.markdown("---")
        if st.button("Terminate Session", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()

    # ==============================================================================
    # 7. PILIHAN DASHBOARD USER WORKFLOW
    # ==============================================================================
    if chosen_menu == "Katalog Inventori Tiket":
        st.markdown("<span class='brand-title'>Katalog Alokasi Tiket</span>", unsafe_allow_html=True)
        st.markdown("<p class='brand-subtitle'>Manajemen pemesanan tiket terintegrasi real-time database server</p>", unsafe_allow_html=True)
        
        tab_sektor = st.tabs(["Sektor Hub Udara", "Sektor Jalur Darat", "Paket Destinasi Wisata"])
        mapping_sektor = ["Pesawat", "Kereta Api", "Wisata"]
        
        for idx, sek in enumerate(mapping_sektor):
            with tab_sektor[idx]:
                uniko = list(set([t['kategori'] for t in st.session_state.tickets[sek]]))
                for kat_item in uniko:
                    st.markdown(f"<div style='color:#635BFF; font-weight:700; border-bottom:1px solid #F1F5F9; padding-bottom:4px; margin-top:20px;'>KELAS - {kat_item.upper()}</div>", unsafe_allow_html=True)
                    items_db = [t for t in st.session_state.tickets[sek] if t['kategori'] == kat_item]
                    
                    grid_cols = st.columns(2)
                    for loop_i, item_obj in enumerate(items_db):
                        with grid_cols[loop_i % 2]:
                            st.markdown(f"""
                            <div class="saas-card">
                                <div style="display:flex; justify-content:between; align-items:center;">
                                    <span style="font-size:12px; font-weight:700; color:#635BFF; letter-spacing:1px;">ID: {item_obj['id']}</span>
                                </div>
                                <h4 style="margin:8px 0; font-weight:700; color:#0A2540;">{item_obj['nama']}</h4>
                                <h3 style="margin:0; color:#0A2540; font-weight:800;">Rp {item_obj['harga']:,}</h3>
                                <p style="font-size:13px; color:#627D98; margin-top:5px; margin-bottom:15px;">Ketersediaan Seat: <b>{item_obj['stok']}</b> unit</p>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button("Alokasikan ke Keranjang", key=f"kat_{item_obj['id']}", use_container_width=True):
                                if item_obj['stok'] > 0:
                                    st.session_state.cart.append({"id": item_obj['id'], "nama": item_obj['nama'], "harga": item_obj['harga'], "qty": 1})
                                    st.toast(f"Berhasil ditambahkan: {item_obj['nama']}")
                                else:
                                    st.error("Stok barang habis.")

    elif chosen_menu == "Asisten Interaktif ArcBot":
        st.markdown("<span class='brand-title'>Core AI ArcBot Gateway</span>", unsafe_allow_html=True)
        st.markdown("<p class='brand-subtitle'>Percakapan natural berbasis FSA Generatif dengan toleransi kesalahan ketik</p>", unsafe_allow_html=True)
        
        chat_layout_left, chat_layout_right = st.columns([2.5, 1])
        
        with chat_layout_right:
            st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
            st.markdown("<h5>Context State Tracker</h5>", unsafe_allow_html=True)
            st.write(f"**Sektor Dituju:** {st.session_state.arcbot.selected_jenis or 'None'}")
            st.write(f"**Kategori Dipilih:** {st.session_state.arcbot.selected_kategori or 'None'}")
            if st.button("Wipe Chat Memory", use_container_width=True):
                st.session_state.arcbot = ArcBotGenerativeFSA()
                st.session_state.chat_history = [{"role": "assistant", "content": st.session_state.arcbot.response}]
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        with chat_layout_left:
            for chit in st.session_state.chat_history:
                if chit["role"] == "assistant":
                    st.markdown(f"<div class='bubble-assistant'>{chit['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='bubble-user'>{chit['content']}</div>", unsafe_allow_html=True)
                    
            if inp_chat := st.chat_input("Ketik pesan balasan Anda ke ArcBot..."):
                st.session_state.chat_history.append({"role": "user", "content": inp_chat})
                st.session_state.arcbot.step(inp_chat)
                st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.arcbot.response})
                st.rerun()

    elif chosen_menu == "Manajemen Keranjang Belanja":
        st.markdown("<span class='brand-title'>Billing System & Checkout</span>", unsafe_allow_html=True)
        st.markdown("<p class='brand-subtitle'>Kelola rekapitulasi data pembelian dan masukkan kode voucher diskon</p>", unsafe_allow_html=True)
        
        if not st.session_state.cart:
            st.info("Sistem mendeteksi keranjang belanja Anda masih kosong.")
        else:
            df_rekap = pd.DataFrame(st.session_state.cart)
            st.dataframe(df_rekap, use_container_width=True, hide_index=True)
            
            subtotal = sum([x['harga'] * x['qty'] for x in st.session_state.cart])
            
            # Fitur Baru: Sistem Kode Voucher Promo Terintegrasi
            col_v1, col_v2 = st.columns([2, 1])
            with col_v1:
                v_code = st.text_input("Mempunyai Voucher Diskon? Masukkan di sini:", placeholder="Contoh: PROMOHEBAT")
            with col_v2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Terapkan Diskon", use_container_width=True):
                    if v_code in st.session_state.vouchers:
                        st.session_state.applied_promo = st.session_state.vouchers[v_code]
                        st.success(f"Potongan Harga Rp {st.session_state.vouchers[v_code]:,} berhasil diterapkan!")
                    else:
                        st.error("Kode voucher tidak valid.")
                        
            diskon = st.session_state.applied_promo if st.session_state.applied_promo else 0
            total_akhir = max(0, subtotal - diskon)
            
            st.markdown(f"<h4>Subtotal: Rp {subtotal:,}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color:red;'>Potongan Voucher: - Rp {diskon:,}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='color:#635BFF;'>Total Akhir Tagihan: Rp {total_akhir:,}</h2>", unsafe_allow_html=True)
            
            # Fitur Baru: Dropdown Pemilihan Metode Pembayaran Resmi
            pay_method = st.selectbox("Pilih Metode Settlement Pembayaran:", ["Mandiri Virtual Account", "BCA Virtual Account", "QRIS LinkAja/Dana", "Credit Card Secured"])
            
            c_action1, c_action2 = st.columns(2)
            with c_action1:
                if st.button("Kosongkan Semua Item", use_container_width=True):
                    st.session_state.cart = []
                    st.session_state.applied_promo = None
                    st.rerun()
            with c_action2:
                if st.button("Konfirmasi Pembayaran Finansial", use_container_width=True):
                    for item_c in st.session_state.cart:
                        for k_key in st.session_state.tickets:
                            for item_t in st.session_state.tickets[k_key]:
                                if item_t['id'] == item_c['id']:
                                    item_t['stok'] -= 1
                                    
                    st.session_state.history_transaksi.append({
                        "id_transaksi": f"TX-{random.randint(10000, 99999)}",
                        "customer": st.session_state.current_user,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "rincian": ", ".join([f"{x['nama']} (x{x['qty']})" for x in st.session_state.cart]),
                        "metode": pay_method,
                        "nominal": total_akhir
                    })
                    st.session_state.cart = []
                    st.session_state.applied_promo = None
                    st.success("Transaksi Diterima! Faktur Pemesanan Elektronik Anda telah diterbitkan.")

    elif chosen_menu == "Arsip Riwayat Pemesanan":
        st.markdown("<span class='brand-title'>Arsip Pemesanan Resmi</span>", unsafe_allow_html=True)
        st.markdown("<p class='brand-subtitle'>Lembar riwayat pencatatan dokumen perjalanan dan status cetak manifes</p>", unsafe_allow_html=True)
        
        filter_trx = [x for x in st.session_state.history_transaksi if x['customer'] == st.session_state.current_user]
        if not filter_trx:
            st.info("Sistem belum menemukan adanya transaksi keluar atas nama user Anda.")
        else:
            for trx in filter_trx:
                with st.container():
                    st.markdown(f"""
                    <div class='saas-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <b style='color:#635BFF;'>{trx['id_transaksi']}</b>
                            <span style='color:#627D98; font-size:12px;'>{trx['timestamp']}</span>
                        </div>
                        <p style='margin:10px 0;'>Detail Item: {trx['rincian']}</p>
                        <p style='margin:0; font-size:13px;'>Metode: {trx['metode']} | <b>Total: Rp {trx['nominal']:,}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                    # Fitur Baru: Tombol Cetak Nota Mockup Elektronik
                    if st.button("Cetak Digital Dokumen PDF", key=f"print_{trx['id_transaksi']}"):
                        st.toast(f"Mengekspor berkas {trx['id_transaksi']}... Unduhan Berhasil!")

    # ==============================================================================
    # 8. PANEL KONTROL ADMIN WORKFLOW (MANAJEMEN TIKET TANPA SEBUTAN CRUD)
    # ==============================================================================
    elif chosen_menu == "Dashboard Analitik" and user_info["role"] == "admin":
        st.markdown("<span class='brand-title'>Corporate Data Analytics</span>", unsafe_allow_html=True)
        
        ca, cb, cc = st.columns(3)
        with ca: st.metric("Total User Terdaftar", f"{len(st.session_state.users)} Akun")
        with cb: st.metric("Total Jenis Rute Komoditas", f"{sum([len(st.session_state.tickets[k]) for k in st.session_state.tickets])} Rute")
        with cc: st.metric("Gross Revenue (Pendapatan)", f"Rp {sum([x['nominal'] for x in st.session_state.history_transaksi]):,}")

    elif chosen_menu == "Manajemen Tiket" and user_info["role"] == "admin":
        st.markdown("<span class='brand-title'>Modul Manajemen Konfigurasi Tiket</span>", unsafe_allow_html=True)
        st.markdown("<p class='brand-subtitle'>Panel kontrol mutasi restrukturisasi data, stok gudang, dan penyesuaian kelas tarif</p>", unsafe_allow_html=True)
        
        action_selector = st.radio("Pilih Tipe Aksi Operasional:", ["Lihat Database", "Entri Data Baru", "Modifikasi Parameter Data", "Eliminasi Tiket"], horizontal=True)
        sektor_target = st.selectbox("Pilih Sektor Industri:", ["Pesawat", "Kereta Api", "Wisata"])
        
        if action_selector == "Lihat Database":
            st.dataframe(pd.DataFrame(st.session_state.tickets[sektor_target]), use_container_width=True, hide_index=True)
            
        elif action_selector == "Entri Data Baru":
            new_id = st.text_input("Kode ID Unik Baru")
            new_kat = st.text_input("Kategori Kelas")
            new_nama = st.text_input("Nama Jadwal/Armada Lengkap")
            new_harga = st.number_input("Besaran Tarif Unit (Rupiah)", min_value=0, step=50000)
            new_stok = st.number_input("Batas Maksimal Kuota Kursi", min_value=0, step=5)
            
            if st.button("Simpan Entri Baru"):
                st.session_state.tickets[sektor_target].append({
                    "id": new_id, "kategori": new_kat, "nama": new_nama, "harga": new_harga, "stok": new_stok
                })
                st.success("Informasi tiket baru telah berhasil diunggah ke database awan.")
                
        elif action_selector == "Modifikasi Parameter Data":
            arr_id = [x['id'] for x in st.session_state.tickets[sektor_target]]
            id_chosen = st.selectbox("Pilih Kode ID Target yang Diubah", arr_id)
            
            ref_pointer = next(x for x in st.session_state.tickets[sektor_target] if x['id'] == id_chosen)
            edit_kat = st.text_input("Sesuaikan Kategori", value=ref_pointer['kategori'])
            edit_nama = st.text_input("Sesuaikan Nama Objek", value=ref_pointer['nama'])
            edit_harga = st.number_input("Sesuaikan Nilai Tarif Jual", min_value=0, value=ref_pointer['harga'])
            edit_stok = st.number_input("Sesuaikan Batas Stok Sisa", min_value=0, value=ref_pointer['stok'])
            
            if st.button("Terapkan Konfigurasi Baru"):
                ref_pointer['kategori'] = edit_kat
                ref_pointer['nama'] = edit_nama
                ref_pointer['harga'] = edit_harga
                ref_pointer['stok'] = edit_stok
                st.success("Sinkronisasi Pembaruan Data Sukses Dilakukan.")

        elif action_selector == "Eliminasi Tiket":
            arr_id = [x['id'] for x in st.session_state.tickets[sektor_target]]
            id_chosen = st.selectbox("Pilih ID Tiket yang Akan Dihapus", arr_id)
            if st.button("Hapus Secara Permanen"):
                st.session_state.tickets[sektor_target] = [x for x in st.session_state.tickets[sektor_target] if x['id'] != id_chosen]
                st.warning("Data terpilih telah dibersihkan secara permanen dari server.")

    elif chosen_menu == "Log Transaksi Pengguna" and user_info["role"] == "admin":
        st.markdown("<span class='brand-title'>Audit Log Sistem Finansial</span>", unsafe_allow_html=True)
        if not st.session_state.history_transaksi:
            st.info("Belum ada mutasi log transaksi terdeteksi masuk.")
        else:
            st.dataframe(pd.DataFrame(st.session_state.history_transaksi), use_container_width=True, hide_index=True)

    # ==============================================================================
    # 9. PENGATURAN PROFIL INTEGRATED HUB
    # ==============================================================================
    elif chosen_menu == "Pengaturan Profil":
        st.markdown("<span class='brand-title'>Account Settings Portal</span>", unsafe_allow_html=True)
        
        curr_u = st.session_state.current_user
        edit_display_name = st.text_input("Ubah Nama Resmi Akun", value=st.session_state.users[curr_u]['name'])
        edit_display_pass = st.text_input("Ubah Kunci Pengaman Baru", value=st.session_state.users[curr_u]['password'], type="password")
        
        if st.button("Perbarui Data Autentikasi"):
            if edit_display_name and edit_display_pass:
                st.session_state.users[curr_u]['name'] = edit_display_name
                st.session_state.users[curr_u]['password'] = edit_display_pass
                st.success("Modifikasi data kredensial profil Anda berhasil diproses.")