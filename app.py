import streamlit as st
import time
import random
from questions import QUESTIONS

st.set_page_config(page_title="Apple Dev Academy Prep", page_icon="🍎", layout="wide")

# ── Question categories for logic section labels ──
LOGIC_CATEGORIES = {
    "CATEGORY A": "📊 Pola Angka (Number Series)",
    "CATEGORY B": "🔤 Pola Huruf (Letter Series)",
    "CATEGORY C": "🏷️ Klasifikasi Kata (Verbal Classification)",
    "CATEGORY D": "🧩 Bagian Esensial (Essential Part)",
    "CATEGORY E": "🔗 Analogi (Verbal Analogies)",
    "CATEGORY F": "🧠 Logika Deduktif (Deductive Logic)",
    "CATEGORY G": "🌐 Bahasa Buatan (Artificial Language)",
    "CATEGORY H": "📋 Definisi & Penilaian (Matching Definitions)",
    "CATEGORY I": "♟️ Puzzle Logika (Complex Logic)",
}

@st.cache_data
def get_random_questions(all_questions):
    selected_questions = {}
    quota = {
        "Section 1: Logic": 25,
        "Section 2: Programming (Swift Focus)": 15,
        "Section 3: OOP": 10,
        "Section 4: Bonus (Design/UX)": 2
    }
    
    for section, limit in quota.items():
        if section in all_questions:
            sample_size = min(len(all_questions[section]), limit)
            selected_questions[section] = random.sample(all_questions[section], sample_size)
            
    return selected_questions

# ── Session state initialization ──
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = get_random_questions(QUESTIONS)
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# ── Reset handler ──
def reset_test():
    get_random_questions.clear()
    st.session_state.selected_questions = get_random_questions(QUESTIONS)
    st.session_state.answers = {}
    st.session_state.start_time = time.time()
    st.session_state.submitted = False

# ── Header ──
st.title("🍎 Apple Developer Academy — Simulation Test")
st.caption("Simulasi tes masuk Apple Developer Academy dengan soal logika, Swift, OOP, dan Design/UX")
st.markdown("---")

# ── Timer & Sidebar ──
duration = 60 * 45  # 45 minutes
elapsed = time.time() - st.session_state.start_time
remaining = max(0, int(duration - elapsed))
mins_left = remaining // 60
secs_left = remaining % 60

st.sidebar.header("⏱️ Waktu Tersisa")
if remaining > 300:
    st.sidebar.subheader(f"🟢 {mins_left} menit {secs_left} detik")
elif remaining > 60:
    st.sidebar.warning(f"🟡 {mins_left} menit {secs_left} detik")
else:
    st.sidebar.error(f"🔴 {mins_left} menit {secs_left} detik")

# Progress bar for time
time_progress = min(1.0, elapsed / duration)
st.sidebar.progress(time_progress, text=f"{int(time_progress*100)}% waktu terpakai")

# ── Progress indicator ──
total_questions = sum(len(v) for v in st.session_state.selected_questions.values())
answered_count = sum(1 for v in st.session_state.answers.values() if v is not None)

st.sidebar.markdown("---")
st.sidebar.header("📝 Progress Jawaban")
st.sidebar.metric("Terjawab", f"{answered_count} / {total_questions}")
answer_progress = answered_count / total_questions if total_questions > 0 else 0
st.sidebar.progress(answer_progress, text=f"{int(answer_progress*100)}% soal dijawab")

# Per-section progress
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Per Bagian")
for section, q_list in st.session_state.selected_questions.items():
    section_answered = sum(
        1 for i in range(len(q_list)) 
        if st.session_state.answers.get(f"{section}_{i}") is not None
    )
    short_name = section.split(":")[1].strip() if ":" in section else section
    st.sidebar.caption(f"**{short_name}**: {section_answered}/{len(q_list)}")

# Reset button
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Mulai Tes Baru", use_container_width=True, type="primary"):
    reset_test()
    st.rerun()

# ── Auto-refresh timer (every 30 seconds) ──
if not st.session_state.submitted and remaining > 0:
    time.sleep(0.1)  # Small delay to not block
    # Use st.empty for auto-refresh hint
    
if remaining <= 0 and not st.session_state.submitted:
    st.error("⏰ Waktu Habis! Silakan tekan tombol Submit Jawaban.")

# ── Question Form ──
if not st.session_state.submitted:
    with st.form("exam_form"):
        for section, q_list in st.session_state.selected_questions.items():
            st.header(section)
            
            # Show total available questions info for logic section
            if section == "Section 1: Logic":
                total_available = len(QUESTIONS.get(section, []))
                st.info(f"📚 Menampilkan {len(q_list)} dari {total_available} soal logika yang tersedia (dipilih acak)")
            
            prev_category = None
            for i, q_item in enumerate(q_list):
                q_key = f"{section}_{i}"
                
                # Show category label for logic questions
                if section == "Section 1: Logic":
                    q_text = q_item.get('q', '')
                    # Detect category from question content
                    for cat_key, cat_label in LOGIC_CATEGORIES.items():
                        # We'll just show the question number and text
                        pass
                
                st.write(f"**{i+1}. {q_item['q']}**")
                
                user_choice = st.radio(
                    "Pilih jawaban:", 
                    q_item['options'], 
                    key=q_key,
                    index=None
                )
                st.session_state.answers[q_key] = user_choice
                st.divider()

        submitted = st.form_submit_button("✅ Submit Jawaban", use_container_width=True, type="primary")
    
    if submitted:
        st.session_state.submitted = True
        st.rerun()

# ── Results Display ──
if st.session_state.submitted:
    correct_count = 0
    total_questions = sum(len(v) for v in st.session_state.selected_questions.values())
    section_results = {}
    
    for section, q_list in st.session_state.selected_questions.items():
        section_correct = 0
        section_total = len(q_list)
        for i, q_item in enumerate(q_list):
            q_key = f"{section}_{i}"
            user_answer = st.session_state.answers.get(q_key)
            if user_answer == q_item['answer']:
                correct_count += 1
                section_correct += 1
        section_results[section] = (section_correct, section_total)

    score_final = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    st.header("📊 Hasil Tes Anda")
    st.markdown("---")
    
    # Overall metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("🏆 Skor Akhir", f"{score_final:.1f}%")
    col2.metric("✅ Benar", f"{correct_count} / {total_questions}")
    elapsed_mins = int(elapsed // 60)
    elapsed_secs = int(elapsed % 60)
    col3.metric("⏱️ Waktu Terpakai", f"{elapsed_mins}m {elapsed_secs}s")
    
    if score_final >= 75:
        st.balloons()
        st.success("🎉 Luar biasa! Peluang kamu lolos sangat besar.")
    elif score_final >= 50:
        st.warning("📈 Lumayan! Masih bisa ditingkatkan. Perhatikan bagian yang salah.")
    else:
        st.error("💪 Terus latihan ya! Fokus pada bagian yang masih lemah.")
    
    # Per-section breakdown
    st.markdown("---")
    st.subheader("📊 Breakdown Per Bagian")
    
    breakdown_cols = st.columns(len(section_results))
    for idx, (section, (s_correct, s_total)) in enumerate(section_results.items()):
        s_pct = (s_correct / s_total * 100) if s_total > 0 else 0
        short_name = section.split(":")[1].strip() if ":" in section else section
        with breakdown_cols[idx]:
            st.metric(short_name, f"{s_correct}/{s_total}")
            st.progress(s_pct / 100)
            if s_pct >= 75:
                st.caption("🟢 Bagus!")
            elif s_pct >= 50:
                st.caption("🟡 Cukup")
            else:
                st.caption("🔴 Perlu latihan")
    
    # Detailed wrong answers with explanations
    st.markdown("---")
    st.subheader("📝 Pembahasan Jawaban Salah")
    
    has_wrong = False
    for section, q_list in st.session_state.selected_questions.items():
        wrong_in_section = []
        for i, q_item in enumerate(q_list):
            q_key = f"{section}_{i}"
            user_answer = st.session_state.answers.get(q_key)
            if user_answer != q_item['answer']:
                wrong_in_section.append((i, q_item, user_answer))
        
        if wrong_in_section:
            has_wrong = True
            st.markdown(f"### {section}")
            for i, q_item, user_answer in wrong_in_section:
                with st.expander(f"❌ Soal {i+1}: {q_item['q'][:80]}..."):
                    if user_answer is None:
                        st.write("📌 **Jawaban kamu:** _Tidak dijawab_")
                    else:
                        st.write(f"📌 **Jawaban kamu:** :red[{user_answer}]")
                    st.write(f"✅ **Jawaban benar:** :green[{q_item['answer']}]")
                    
                    # Show explanation if available
                    explanation = q_item.get('explanation')
                    if explanation:
                        st.info(f"💡 **Penjelasan:** {explanation}")
    
    if not has_wrong:
        st.success("🏆 Sempurna! Semua jawaban benar!")
    
    # Reset button at bottom
    st.markdown("---")
    col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
    with col_reset2:
        if st.button("🔄 Mulai Tes Baru", key="reset_bottom", use_container_width=True, type="primary"):
            reset_test()
            st.rerun()