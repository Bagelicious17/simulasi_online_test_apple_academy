import streamlit as st
import time
import random
from questions import QUESTIONS

st.set_page_config(page_title="Apple Dev Academy Prep", page_icon="🍎", layout="wide")

# ── Question categories for logic section labels ──
LOGIC_CATEGORIES = {
    "CATEGORY A": "📊 Number Series",
    "CATEGORY B": "🔤 Letter Series",
    "CATEGORY C": "🏷️ Verbal Classification",
    "CATEGORY D": "🧩 Essential Part",
    "CATEGORY E": "🔗 Verbal Analogies",
    "CATEGORY F": "🧠 Deductive Logic",
    "CATEGORY G": "🌐 Artificial Language",
    "CATEGORY H": "📋 Matching Definitions",
    "CATEGORY I": "♟️ Complex Logic Puzzles",
}

@st.cache_data
def get_random_questions(all_questions):
    selected_questions = {}
    quota = {
        "Section 1: Logic": 25,
        "Section 2: Programming (Swift Focus)": 20,
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
st.caption("Entrance test simulation with Logic, Swift Programming, OOP, and Design/UX questions")
st.markdown("---")

# ── Timer & Sidebar ──
duration = 60 * 45  # 45 minutes
elapsed = time.time() - st.session_state.start_time
remaining = max(0, int(duration - elapsed))
mins_left = remaining // 60
secs_left = remaining % 60

st.sidebar.header("⏱️ Time Remaining")
if remaining > 300:
    st.sidebar.subheader(f"🟢 {mins_left} min {secs_left} sec")
elif remaining > 60:
    st.sidebar.warning(f"🟡 {mins_left} min {secs_left} sec")
else:
    st.sidebar.error(f"🔴 {mins_left} min {secs_left} sec")

# Progress bar for time
time_progress = min(1.0, elapsed / duration)
st.sidebar.progress(time_progress, text=f"{int(time_progress*100)}% time used")

# ── Progress indicator ──
total_questions = sum(len(v) for v in st.session_state.selected_questions.values())
answered_count = sum(1 for v in st.session_state.answers.values() if v is not None)

st.sidebar.markdown("---")
st.sidebar.header("📝 Answer Progress")
st.sidebar.metric("Answered", f"{answered_count} / {total_questions}")
answer_progress = answered_count / total_questions if total_questions > 0 else 0
st.sidebar.progress(answer_progress, text=f"{int(answer_progress*100)}% questions answered")

# Per-section progress
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Per Section")
for section, q_list in st.session_state.selected_questions.items():
    section_answered = sum(
        1 for i in range(len(q_list)) 
        if st.session_state.answers.get(f"{section}_{i}") is not None
    )
    short_name = section.split(":")[1].strip() if ":" in section else section
    st.sidebar.caption(f"**{short_name}**: {section_answered}/{len(q_list)}")

# Reset button
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Start New Test", use_container_width=True, type="primary"):
    reset_test()
    st.rerun()

# ── Auto-refresh timer (every 30 seconds) ──
if not st.session_state.submitted and remaining > 0:
    time.sleep(0.1)  # Small delay to not block
    
if remaining <= 0 and not st.session_state.submitted:
    st.error("⏰ Time's Up! Please press the Submit Answers button.")

# ── Question Form ──
if not st.session_state.submitted:
    with st.form("exam_form"):
        for section, q_list in st.session_state.selected_questions.items():
            st.header(section)
            
            # Show total available questions info
            total_available = len(QUESTIONS.get(section, []))
            if total_available > len(q_list):
                st.info(f"📚 Showing {len(q_list)} of {total_available} available questions (randomly selected)")
            
            for i, q_item in enumerate(q_list):
                q_key = f"{section}_{i}"
                
                st.write(f"**{i+1}. {q_item['q']}**")
                
                user_choice = st.radio(
                    "Choose your answer:", 
                    q_item['options'], 
                    key=q_key,
                    index=None
                )
                st.session_state.answers[q_key] = user_choice
                st.divider()

        submitted = st.form_submit_button("✅ Submit Answers", use_container_width=True, type="primary")
    
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
    
    st.header("📊 Your Test Results")
    st.markdown("---")
    
    # Overall metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("🏆 Final Score", f"{score_final:.1f}%")
    col2.metric("✅ Correct", f"{correct_count} / {total_questions}")
    elapsed_mins = int(elapsed // 60)
    elapsed_secs = int(elapsed % 60)
    col3.metric("⏱️ Time Spent", f"{elapsed_mins}m {elapsed_secs}s")
    
    if score_final >= 75:
        st.balloons()
        st.success("🎉 Outstanding! You have a great chance of getting in!")
    elif score_final >= 50:
        st.warning("📈 Not bad! Room for improvement — review the wrong answers below.")
    else:
        st.error("💪 Keep practicing! Focus on the sections where you scored lowest.")
    
    # Per-section breakdown
    st.markdown("---")
    st.subheader("📊 Section Breakdown")
    
    breakdown_cols = st.columns(len(section_results))
    for idx, (section, (s_correct, s_total)) in enumerate(section_results.items()):
        s_pct = (s_correct / s_total * 100) if s_total > 0 else 0
        short_name = section.split(":")[1].strip() if ":" in section else section
        with breakdown_cols[idx]:
            st.metric(short_name, f"{s_correct}/{s_total}")
            st.progress(s_pct / 100)
            if s_pct >= 75:
                st.caption("🟢 Great!")
            elif s_pct >= 50:
                st.caption("🟡 Decent")
            else:
                st.caption("🔴 Needs practice")
    
    # Detailed wrong answers with explanations
    st.markdown("---")
    st.subheader("📝 Wrong Answer Review")
    
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
                with st.expander(f"❌ Q{i+1}: {q_item['q'][:80]}..."):
                    if user_answer is None:
                        st.write("📌 **Your answer:** _Not answered_")
                    else:
                        st.write(f"📌 **Your answer:** :red[{user_answer}]")
                    st.write(f"✅ **Correct answer:** :green[{q_item['answer']}]")
                    
                    # Show explanation if available
                    explanation = q_item.get('explanation')
                    if explanation:
                        st.info(f"💡 **Explanation:** {explanation}")
    
    if not has_wrong:
        st.success("🏆 Perfect! All answers are correct!")
    
    # Reset button at bottom
    st.markdown("---")
    col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
    with col_reset2:
        if st.button("🔄 Start New Test", key="reset_bottom", use_container_width=True, type="primary"):
            reset_test()
            st.rerun()