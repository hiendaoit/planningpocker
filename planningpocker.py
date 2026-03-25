import streamlit as st
from streamlit_server_state import server_state, server_state_lock

st.set_page_config(page_title="Agile Planning Poker Realtime", layout="centered")

st.title("🃏 Agile Planning Poker")

# Khởi tạo kho lưu trữ chung cho tất cả mọi người (Server-wide)
with server_state_lock["poker_data"]:
    if "points" not in server_state:
        server_state.points = {}
    if "reveal" not in server_state:
        server_state.reveal = False

# --- SIDEBAR DÀNH CHO PM (HOST) ---
with st.sidebar:
    st.header("Admin Control")
    password = st.text_input("Mật khẩu Admin", type="password")
    if password == "admin123":
        st.success("Bạn đang là Host!")
        if st.button("Lật bài (Reveal)"):
            with server_state_lock["poker_data"]:
                server_state.reveal = True
        
        if st.button("Làm mới (Reset)"):
            with server_state_lock["poker_data"]:
                server_state.points = {}
                server_state.reveal = False
            st.rerun()

# --- GIAO DIỆN NGƯỜI CHƠI ---
name = st.text_input("Nhập tên của bạn:")

if name:
    st.subheader(f"Chào {name}, mời bạn chọn Story Point:")
    cols = st.columns(7)
    fibonacci = [1, 2, 3, 5, 8, 13, 21]
    
    for i, p in enumerate(fibonacci):
        if cols[i].button(str(p), key=f"btn_{p}"):
            with server_state_lock["poker_data"]:
                # Cập nhật điểm vào kho chung
                current_points = server_state.points.copy()
                current_points[name] = p
                server_state.points = current_points
            st.toast(f"Bạn đã chọn {p} points!")

st.divider()

# --- HIỂN THỊ KẾT QUẢ REALTIME ---
st.subheader("Kết quả đánh giá")

if not server_state.points:
    st.info("Đang chờ mọi người vote...")
else:
    all_votes = server_state.points
    voted_names = list(all_votes.keys())
    
    if not server_state.reveal:
        st.warning(f"Đã có {len(voted_names)} người vote. Đang ẩn kết quả...")
        # Hiển thị danh sách những người đã xong nhưng không hiện điểm
        for n in voted_names:
            st.write(f"✅ **{n}** đã xong.")
    else:
        st.success("🎉 CẢ TEAM CÙNG LẬT BÀI:")
        for n, p in all_votes.items():
            st.write(f"👤 **{n}**: {p} Points")
        
        # Tính trung bình để PM dễ chốt số
        avg = sum(all_votes.values()) / len(all_votes)
        st.metric("Điểm trung bình", f"{avg:.1f}")
