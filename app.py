import streamlit as st
import pandas as pd
import random
import re
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
    
# ==============================================================================
# INITIALIZATION: DATA TICKETS DENGAN DATA JADWAL (RUTE, TANGGAL, JAM) REALISTIS
# ==============================================================================
if 'tickets' not in st.session_state:
    st.session_state.tickets = {
        "Pesawat": [
            {
                "id": "P01", 
                "kategori": "Ekonomi", 
                "nama": "Garuda Indonesia GA-204 (JKT - SUB)", 
                "asal": "JKT", "tujuan": "SUB",
                "harga": 1200000, 
                "stok": 50, 
                "fasilitas": "Bagasi 20kg, Makanan Hidangan Hangat, WiFi Terbatas",
                "image": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 08:00", "26-06-2026 14:00", "27-06-2026 19:30"]
            },
            {
                "id": "P02", 
                "kategori": "Ekonomi", 
                "nama": "Lion Air JT-512 (JKT - DPS)", 
                "asal": "JKT", "tujuan": "DPS",
                "harga": 850000, 
                "stok": 80, 
                "fasilitas": "Bagasi Kabin 7kg (Bagasi Bagasi berbayar)",
                "image": "https://images.unsplash.com/photo-1540962351504-03099e0a754b?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 06:00", "26-06-2026 11:15"]
            },
            {
                "id": "P03", 
                "kategori": "Ekonomi", 
                "nama": "Citilink QG-142 (JKT - JOG)", 
                "asal": "JKT", "tujuan": "JOG",
                "harga": 700000, 
                "stok": 60, 
                "fasilitas": "Free Snack Box, Bagasi Terdaftar 10kg",
                "image": "https://images.unsplash.com/photo-1483450388369-9ed95738483c?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 09:45", "28-06-2026 16:20"]
            },
            {
                "id": "P04", 
                "kategori": "Bisnis", 
                "nama": "Batik Air ID-6572 (JKT - MES)", 
                "asal": "JKT", "tujuan": "MES",
                "harga": 2500000, 
                "stok": 20, 
                "fasilitas": "Kursi Kulit Lebar, Bagasi 30kg, Makanan Premium",
                "image": "https://images.unsplash.com/photo-1517479149777-5f3b1511d5ad?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["26-06-2026 07:00", "27-06-2026 13:00"]
            },
            {
                "id": "P05", 
                "kategori": "Bisnis", 
                "nama": "Garuda Indonesia GA-312 (JKT - SUB)", 
                "asal": "JKT", "tujuan": "SUB",
                "harga": 3400000, 
                "stok": 15, 
                "fasilitas": "In-flight Entertainment 4K, WiFi Unlimited, Bagasi 40kg, Akses Lounge Bandara",
                "image": "https://images.unsplash.com/photo-1606761568499-6d2451b23c66?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 10:00", "27-06-2026 17:15"]
            },
        ],
        "Kereta Api": [
            {
                "id": "K01", 
                "kategori": "Ekonomi", 
                "nama": "Airlangga 236 (PSE - SBI)", 
                "asal": "PSE", "tujuan": "SBI",
                "harga": 104000, 
                "stok": 120, 
                "fasilitas": "AC Split, Power Outlet/Charger per bangku, Toilet Bersih",
                "image": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 11:10", "26-06-2026 11:10", "27-06-2026 11:10"]
            },
            {
                "id": "K02", 
                "kategori": "Ekonomi", 
                "nama": "Bengawan 246 (PSE - PWS)", 
                "asal": "PSE", "tujuan": "PWS",
                "harga": 74000, 
                "stok": 100, 
                "fasilitas": "AC, Charger, Formasi Kursi 3-2 berhadapan",
                "image": "https://images.unsplash.com/photo-1515165504669-423042d330d6?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 06:20", "26-06-2026 06:20"]
            },
            {
                "id": "K07", 
                "kategori": "Eksekutif", 
                "nama": "Argo Bromo Anggrek 2 (GMR - SBI)", 
                "asal": "GMR", "tujuan": "SBI",
                "harga": 650000, 
                "stok": 30, 
                "fasilitas": "Kursi Reclining & Rotating, Selimut & Bantal, Makan Gratis, WiFi",
                "image": "https://images.unsplash.com/photo-1532103054090-334e6e60b73c?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 08:15", "26-06-2026 20:30"]
            },
            {
                "id": "K08", 
                "kategori": "Eksekutif", 
                "nama": "Argo Lawu 8 (GMR - SLO)", 
                "asal": "GMR", "tujuan": "SLO",
                "harga": 580000, 
                "stok": 25, 
                "fasilitas": "Kursi Reclining, Port Audio, AC Sentral Dingin, Layanan Restorasi ke Meja",
                "image": "https://images.unsplash.com/photo-1519626144233-7ff521bf83cd?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 22:15", "27-06-2026 22:15"]
            },
        ],
        "Wisata": [
            {
                "id": "W01", 
                "kategori": "Lokal", 
                "nama": "Tiket Masuk Candi Borobudur", 
                "asal": "SEMUA", "tujuan": "BOROBUDUR",
                "harga": 50000, 
                "stok": 1000, 
                "fasilitas": "Akses Plataran Luar Candi, Pemandu Audio Digital (QR)",
                "image": "https://images.unsplash.com/photo-1584810359583-96fc3448beaa?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 07:00", "26-06-2026 07:00", "27-06-2026 07:00"]
            },
            {
                "id": "W02", 
                "kategori": "Lokal", 
                "nama": "Tiket Masuk Dufan Ancol", 
                "asal": "SEMUA", "tujuan": "DUFAN",
                "harga": 275000, 
                "stok": 500, 
                "fasilitas": "Akses Reguler ke Semua Wahana (Antrean Normal)",
                "image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 10:00", "26-06-2026 10:00", "27-06-2026 10:00"]
            },
            {
                "id": "W07", 
                "kategori": "VIP", 
                "nama": "VIP Fast Track Dufan Pass", 
                "asal": "SEMUA", "tujuan": "DUFAN",
                "harga": 650000, 
                "stok": 50, 
                "fasilitas": "Jalur Bebas Antrean (Fast Track) di 12 Wahana Utama, Akses Lounge Ber-AC",
                "image": "https://images.unsplash.com/photo-1561662091-aef40e041dcd?auto=format&fit=crop&q=80&w=600",
                "jadwal": ["25-06-2026 10:00", "26-06-2026 10:00"]
            },
        ]
    }

if 'history_transaksi' not in st.session_state: st.session_state.history_transaksi = []
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'applied_promo' not in st.session_state: st.session_state.applied_promo = None
if 'vouchers' not in st.session_state: st.session_state.vouchers = {"PROMOHEBAT": 50000, "ARCHELTIK": 100000}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'cart' not in st.session_state: st.session_state.cart = []
st.session_state.initialized = True

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
        self.selected_asal = None
        self.selected_tujuan = None
        self.selected_tanggal = None 
        self.selected_jam = None
        self.selected_kategori = None
        self.selected_tiket = None
        self.temp_nama = None       
        self.temp_nik = None        
        self.temp_kontak = None     
        self.response = "Halo! Saya ArcBot. Silakan pilih jenis tiket yang ingin Anda cari:\n- **Pesawat**\n- **Kereta Api**\n- **Wisata**"

    def dapatkan_deskripsi_kategori(self, jenis, kategori):
        deskripsi = {
            "Pesawat": {
                "Ekonomi": "Kelas Ekonomis dengan harga terjangkau, konfigurasi kursi standar.",
                "Bisnis": "Kelas Eksklusif dengan ruang kaki luas, prioritas bagasi, dan hidangan premium."
            },
            "Kereta Api": {
                "Ekonomi": "Kelas Kereta dengan efisiensi biaya tinggi, dilengkapi AC dan stopkontak.",
                "Eksekutif": "Kelas Kereta Premium dengan kursi reclining, kabin senyap, dan bantal."
            },
            "Wisata": {
                "Lokal": "Tiket akses masuk standar/reguler ke area destinasi utama.",
                "VIP": "Tiket akses premium dengan keuntungan jalur tanpa antrean (Fast Track)."
            }
        }
        return deskripsi.get(jenis, {}).get(kategori, "Kategori standar untuk kenyamanan perjalanan Anda.")

    def handle_global_queries(self, user_input):
        ui = user_input.lower()
        if "termurah" in ui:
            kategori_target = None
            if "pesawat" in ui: kategori_target = "Pesawat"
            elif "kereta" in ui: kategori_target = "Kereta Api"
            elif "wisata" in ui: kategori_target = "Wisata"
                
            if kategori_target:
                armada_list = st.session_state.tickets[kategori_target]
                murah = min(armada_list, key=lambda x: x['harga'])
                self.selected_jenis = kategori_target
                self.selected_kategori = murah['kategori']
                self.selected_tiket = murah
                self.state = "PILIH_JADWAL_TERMURAH"
                
                jadwal_str = ""
                for j in murah['jadwal']:
                    jadwal_str += f"- `{j}`\n"
                    
                return (
                    f"Tiket '{kategori_target}' termurah saat ini adalah:\n"
                    f"🎫 '{murah['nama']}' ({murah['kategori']})\n"
                    f"Tarif: Rp {murah['harga']:,}\n"
                    f"Fasilitas: {murah['fasilitas']}\n\n"
                    f"Jadwal Keberangkatan yang tersedia:\n{jadwal_str}\n"
                    f"Silakan ketik/salin salah satu Waktu di atas untuk langsung memesan:"
                )
        if "fasilitas" in ui:
            for k in st.session_state.tickets:
                for t in st.session_state.tickets[k]:
                    if t['nama'].lower() in ui or t['id'].lower() in ui:
                        return f"Fasilitas '{t['nama']}': {t['fasilitas']}"
        return None

    def step(self, user_input=None):
        if not user_input: return
        
        global_res = self.handle_global_queries(user_input)
        if global_res:
            self.response = global_res
            return

        ui_lower = user_input.strip().lower()

        # FSM LOGIC
        if self.state == "START":
            cocok = None
            if "pesawat" in ui_lower or "terbang" in ui_lower: cocok = "Pesawat"
            elif "kereta" in ui_lower or "api" in ui_lower: cocok = "Kereta Api"
            elif "wisata" in ui_lower or "liburan" in ui_lower: cocok = "Wisata"
            else:
                cocok = perbaiki_input(user_input, ["pesawat", "kereta api", "wisata"])
                if cocok:
                    cocok = "Pesawat" if cocok == "pesawat" else "Kereta Api" if cocok == "kereta api" else "Wisata"

            if cocok:
                self.selected_jenis = cocok
                
                # Perbaikan Utama: Cek jika ada kecocokan rute spesifik langsung dari database ticket
                rute_ditemukan = False
                for t in st.session_state.tickets[self.selected_jenis]:
                    if t['asal'].lower() in ui_lower and t['tujuan'].lower() in ui_lower:
                        self.selected_asal = t['asal']
                        self.selected_tujuan = t['tujuan']
                        rute_ditemukan = True
                        break

                if rute_ditemukan:
                    self.state = "PILIH_KATEGORI_RUTE"
                    armada_cocok = [t for t in st.session_state.tickets[self.selected_jenis] 
                                    if t['asal'] == self.selected_asal and t['tujuan'] == self.selected_tujuan]
                    kat_list = list(set([t['kategori'] for t in armada_cocok]))
                    kat_str = ", ".join([f"**{k}**" for k in kat_list])
                    self.response = f"Rute ditemukan! Menampilkan tiket '{self.selected_jenis}' dari **{self.selected_asal}** ke **{self.selected_tujuan}**.\n\nSilakan ketik kelas kategori yang tersedia: {kat_str}"
                else:
                    # Masuk ke alur pemilihan kategori umum
                    self.state = "ALUR_NORMAL_KATEGORI"
                    kategori_list = list(set([t['kategori'] for t in st.session_state.tickets[self.selected_jenis]]))
                    kat_str_dengan_desc = ""
                    for k in kategori_list:
                        desc_singkat = self.dapatkan_deskripsi_kategori(self.selected_jenis, k)
                        kat_str_dengan_desc += f"\n- **{k}**: {desc_singkat}"
                    self.response = f"Baik! Berikut kategori tiket '{self.selected_jenis}' yang tersedia:{kat_str_dengan_desc}\n\nSilakan ketik kategori pilihan Anda:"
            else:
                self.response = "Mohon maaf, pesan Anda tidak dipahami. Silakan pilih kategori: **Pesawat**, **Kereta Api**, atau **Wisata**."

        elif self.state == "PILIH_KATEGORI_RUTE":
            armada_cocok = [t for t in st.session_state.tickets[self.selected_jenis] 
                            if t['asal'] == self.selected_asal and t['tujuan'] == self.selected_tujuan]
            kategori_list = list(set([t['kategori'] for t in armada_cocok]))
            kat_lower = [k.lower() for k in kategori_list]
            cocok = perbaiki_input(user_input, kat_lower)
            
            if cocok:
                self.selected_kategori = kategori_list[kat_lower.index(cocok)]
                self.state = "PILIH_ITEM"
                items = [t for t in armada_cocok if t['kategori'] == self.selected_kategori]
                
                item_str = ""
                for t in items:
                    item_str += f"🎫 **[{t['id']}]** {t['nama']}\n"
                    item_str += f"  - Tarif: Rp {t['harga']:,}\n"
                    item_str += f"  - Fasilitas: {t['fasilitas']}\n\n"
                self.response = f"Berikut daftar tiket kelas '{self.selected_kategori}' untuk rute tersebut:\n\n{item_str}Ketik/Copy **Kode ID** tiket pilihan Anda untuk melihat jadwal resmi:"
            else:
                self.response = f"Pilihan salah. Silakan ketik kategori yang sesuai: {', '.join(kategori_list)}"

        elif self.state == "ALUR_NORMAL_KATEGORI":
            kategori_list = list(set([t['kategori'] for t in st.session_state.tickets[self.selected_jenis]]))
            kat_lower = [k.lower() for k in kategori_list]
            cocok = perbaiki_input(user_input, kat_lower)
            
            if cocok:
                self.selected_kategori = kategori_list[kat_lower.index(cocok)]
                self.state = "PILIH_ITEM"
                items = [t for t in st.session_state.tickets[self.selected_jenis] if t['kategori'] == self.selected_kategori]
                
                item_str = ""
                for t in items:
                    item_str += f"🎫 **[{t['id']}]** {t['nama']}\n"
                    item_str += f"  - Tarif: Rp {t['harga']:,}\n"
                    item_str += f"  - Fasilitas: {t['fasilitas']}\n\n"
                self.response = f"Berikut daftar Jadwal kelas '{self.selected_kategori}' yang tersedia:\n\n{item_str}Ketik/Copy **Kode ID** tiket pilihan Anda untuk melihat jadwal resmi:"
            else:
                self.response = f"Kategori kelas tersebut tidak tersedia. Silakan ketik salah satu kelas berikut: {', '.join(kategori_list)}"

        elif self.state == "PILIH_ITEM":
            items = [t for t in st.session_state.tickets[self.selected_jenis] if t['kategori'] == self.selected_kategori]
            id_list = [t['id'].lower() for t in items]
            
            if ui_lower in id_list:
                self.selected_tiket = items[id_list.index(ui_lower)]
                self.state = "PILIH_JADWAL"
                
                jadwal_str = ""
                for j in self.selected_tiket['jadwal']:
                    jadwal_str += f"- `{j}`\n"
                    
                self.response = (
                    f"Jdwal terpilih: **{self.selected_tiket['nama']}**\n"
                    f"Fasilitas: {self.selected_tiket['fasilitas']}\n\n"
                    f"Silakan pilih & ketik ulang Jadwal Keberangkatan di bawah ini secara presisi:\n\n"
                    f"{jadwal_str}"
                )
            else:
                self.response = "Kode ID salah. Mohon ketik kembali Kode ID yang tertera pada daftar di atas (Contoh: P01)."
        elif self.state == "PILIH_JADWAL" or self.state == "PILIH_JADWAL_TERMURAH":
            waktu_input = user_input.strip()
            if waktu_input in self.selected_tiket['jadwal']:
                self.selected_tanggal, self.selected_jam = waktu_input.split(" ")
                self.state = "INPUT_NAMA"
                self.response = f"Jadwal diatur pada tanggal **{self.selected_tanggal}** pukul **{self.selected_jam}**.\n\nMohon masukkan Nama Lengkap Anda (sesuai KTP/Paspor):"
            else:
                self.response = "⚠️ Waktu yang Anda masukkan tidak terdaftar. Silakan salin kembali waktu resmi yang valid sesuai opsi di atas:"

        elif self.state == "INPUT_NAMA": 
            if len(user_input.strip()) < 3:
                self.response = "Nama terlalu pendek. Mohon ketik kembali Nama Lengkap Anda:"
                return
            self.temp_nama = user_input.strip()
            self.state = "INPUT_NIK" 
            self.response = f"Nama penumpang '{self.temp_nama}' berhasil direkam. Selanjutnya, silakan masukkan Nomor NIK KTP / Paspor Anda:"

        elif self.state == "INPUT_NIK":
            if len(user_input.strip()) < 6:
                self.response = "Nomor identitas terlalu pendek. Silakan ketik NIK/Paspor Anda dengan benar:"
                return
            self.temp_nik = user_input.strip()
            self.state = "INPUT_KONTAK" 
            self.response = "Identitas tervalidasi. Terakhir, ketik Nomor Telepon atau WhatsApp Anda yang aktif:"

        elif self.state == "INPUT_KONTAK":
            self.temp_kontak = user_input.strip()
            self.state = "KONFIRMASI" 
            self.response = (
                f"📋 **RINGKASAN FORMULIR MANIFEST PERJALANAN**\n"
                f"- Nama Penumpang: {self.temp_nama}\n"
                f"- NIK / Paspor: {self.temp_nik}\n"
                f"- Kontak: {self.temp_kontak}\n"
                f"- Jadwal: {self.selected_tanggal} [{self.selected_jam} WIB]\n\n"
                f"📦 **DETAIL TIKET:**\n"
                f"[{self.selected_tiket['id']}] {self.selected_tiket['nama']} ({self.selected_kategori})\n"
                f"Tarif Settlement: **Rp {self.selected_tiket['harga']:,}**\n\n"
                f"Apakah data sudah sesuai? Ketik **Beli** untuk memesan atau **Batal** untuk mereset."
            )

        elif self.state == "KONFIRMASI":
            cocok = perbaiki_input(user_input, ["beli", "batal"])
            if cocok == "beli":
                if self.selected_tiket['stok'] > 0:
                    st.session_state.cart.append({
                        "id": self.selected_tiket['id'],
                        "nama": f"{self.selected_tiket['nama']} [{self.selected_tanggal} {self.selected_jam}]",
                        "user": f"{self.temp_nama} (NIK: {self.temp_nik})", 
                        "harga": self.selected_tiket['harga'],
                        "qty": 1 
                    })
                    self.response = f"✅ Sukses! Tiket perjalanan atas nama **{self.temp_nama}** telah berhasil masuk ke Keranjang Belanja. Apakah ada destinasi rute lain yang ingin Anda cari?"
                else:
                    self.response = "Maaf sekali, kuota kursi pada rute jadwal ini baru saja habis terisi penuh."
                self.reset_fsa_data()
            elif cocok == "batal":
                self.reset_fsa_data()
                self.response = "Proses registrasi dibatalkan. Kembali ke awal, apa yang bisa saya bantu? (**Pesawat** / **Kereta Api** / **Wisata**)"
            else:
                self.response = "Mohon konfirmasi secara jelas dengan mengetik kata **Beli** atau **Batal**."

    def reset_fsa_data(self):
        self.state = "START"
        self.selected_jenis = None
        self.selected_asal = None
        self.selected_tujuan = None
        self.selected_tanggal = None
        self.selected_jam = None
        self.selected_kategori = None
        self.selected_tiket = None
        self.temp_nama = None
        self.temp_nik = None
        self.temp_kontak = None

if 'arcbot' not in st.session_state:
    st.session_state.arcbot = ArcBotGenerativeFSA()
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
# 6. MAIN ENTERPRISE DESKTOP & NAVIGATION HEADER (MATCHING THE IMAGE DESIGN)
# ==============================================================================
else:
    user_info = st.session_state.users[st.session_state.current_user]
    
    # Menentukan list menu berdasarkan role
    if user_info["role"] == "admin":
        list_nav = ["Dashboard Analitik", "Manajemen Tiket", "Log Transaksi Pengguna", "Pengaturan Profil"]
    else:
        list_nav = ["Katalog Inventori Tiket", "Asisten Interaktif ArcBot", "Manajemen Keranjang Belanja", "Arsip Riwayat Pemesanan", "Pengaturan Profil"]
    
    # Inisialisasi session state untuk menyimpan menu aktif jika belum ada
    if "chosen_menu" not in st.session_state:
        st.session_state.chosen_menu = list_nav[0]

    # --- INLINE CSS HEADER MENU (PERSIS SEPERTI GAMBAR CONTOH) ---
    st.markdown("""
    <style>
    /* Styling Container Header Navigation */
    .header-nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFFFFF;
        padding: 15px 20px;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 30px;
    }
    .brand-logo-text {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
    }
    .brand-logo-text span {
        color: #EAB308; /* Warna kuning pada teks Tick */
    }
    /* Menghilangkan padding bawaan Streamlit column block untuk button */
    div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Implementasi Grid Header Navigation menggunakan st.columns
    # Membuat baris navigasi atas yang bersih dan rapi
    num_menus = len(list_nav)
    cols_header = st.columns([2] + [1.2] * num_menus + [1.5])
    
    # Kolom Pertama: Logo ArcTick
    with cols_header[0]:
        st.markdown("<div class='brand-logo-text'>Arc<span>Tick</span></div>", unsafe_allow_html=True)
    
    # Kolom Tengah: Menu Pilihan (Katalog, ArcBot, dll) dengan Polos / Underline Aktif
    for idx, menu_name in enumerate(list_nav):
        with cols_header[idx + 1]:
            # Memberikan penanda singkat (singkatan) agar pas di grid header desktop
            short_name = menu_name.replace("Katalog Inventori ", "").replace("Asisten Interaktif ", "").replace("Manajemen ", "").replace("Arsip ", "")
            
            # Deteksi apakah menu ini sedang aktif/dipilih
            is_active = (st.session_state.chosen_menu == menu_name)
            
            # Format visual tombol: Jika aktif diberi mark garis bawah, jika tidak tampil polos tekstual
            button_label = f"✨ {short_name}" if is_active else short_name
            
            # CSS kondisional disuntik via st.markdown tepat sebelum tombol dirender
            if is_active:
                st.markdown("<style>div.stButton > button { border-bottom: 3px solid #635BFF !important; color: #635BFF !important; font-weight: bold; background: none !important; border-top:none; border-left:none; border-right:none; border-radius:0px; }</style>", unsafe_allow_html=True)
            else:
                st.markdown("<style>div.stButton > button { border: none !important; color: #475569 !important; background: none !important; background-color: transparent !important; }</style>", unsafe_allow_html=True)
                
            if st.button(button_label, key=f"nav_{menu_name}", use_container_width=True):
                st.session_state.chosen_menu = menu_name
                st.rerun()
                
    # Kolom Terakhir: Logout (Dibuat mencolok dengan style background Biru Solid seperti tombol Register)
    with cols_header[-1]:
        st.markdown("""
        <style>
        /* Mengubah spesifik tombol terakhir (Logout) menjadi Biru Registrasi */
        div[data-testid="column"]:last-child div.stButton > button {
            background-color: #0066E2 !important;
            color: white !important;
            border-radius: 20px !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 8px 16px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("Sign Out", key="terminate_session_hub", use_container_width=True):
            st.session_state.current_user = None
            st.session_state.chosen_menu = None
            st.rerun()

    # Mengembalikan nilai menu aktif ke variabel lama agar sisa kode di bawahnya tidak error
    chosen_menu = st.session_state.chosen_menu

    # Sidebar opsional (Menampilkan info User internal / Core Node)
    with st.sidebar:
        st.markdown(f"### Node User: {user_info['name']}")
        st.markdown(f"Privilege: `{user_info['role'].upper()}`")
        st.markdown("---")


# ==============================================================================
    # 7. PILIHAN DASHBOARD USER WORKFLOW
    # ==============================================================================
    if chosen_menu == "Katalog Inventori Tiket":
        st.markdown("<span class='brand-title'>Hey There, Going Anywhere?</span>", unsafe_allow_html=True)
        st.markdown("<p class='brand-subtitle'>Pesan Tiket Dimanapun Kapanpun</p>", unsafe_allow_html=True)
        
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
                            # Container kartu luar menggunakan CSS .saas-card Anda
                            st.markdown('<div class="saas-card" style="padding-bottom:10px; margin-bottom:0px;">', unsafe_allow_html=True)
                            
                            # Menampilkan Gambar dari Internet (Menggunakan parameter Native agar 100% responsif)
                            if "image" in item_obj:
                                st.image(item_obj["image"], use_container_width=True)
                            
                            # Mengisi Konten Informasi Tiket di dalam Kartu Elemen setelah gambar
                            st.markdown(f"""
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                                    <span style="font-size:12px; font-weight:700; color:#635BFF; letter-spacing:1px;">ID: {item_obj['id']}</span>
                                    <span style="font-size:11px; background:#F1F5F9; color:#475569; padding:2px 8px; border-radius:12px;">{item_obj['fasilitas'].split(',')[0]}</span>
                                </div>
                                <h4 style="margin:8px 0; font-weight:700; color:#0A2540; line-height:1.4; min-height:45px;">{item_obj['nama']}</h4>
                                <h3 style="margin:0; color:#0A2540; font-weight:800;">Rp {item_obj['harga']:,}</h3>
                                <p style="font-size:13px; color:#627D98; margin-top:5px; margin-bottom:10px;">Ketersediaan Seat: <b>{item_obj['stok']}</b> unit</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Tombol Interaksi Aksi disematkan di luar wrapper raw HTML agar interaksinya tetap berjalan sempurna di Streamlit
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
            new_nama = st.text_input("Nama Jadwal Lengkap")
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