import streamlit as st
from streamlit_server_state import server_state, server_state_lock

# Cấu hình giao diện
st.set_page_config(page_title="Agile Planning Poker Realtime", layout="centered")

st.title("🃏 Agile Planning Poker")
st.write("Dành cho Team 20 người - Dữ liệu Realtime")

# Khởi tạo kho dữ liệu chung trên Server (Thay cho session_state)
with server_state_lock["poker_data"]:
    if "points" not in server_state:
        server_state.points = {}
    if "reveal" not in server_state:
        server_state.reveal = False

# --- SIDEBAR CHO PM (HOST) ---
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

# --- GIAO DIỆN CHO THÀNH VIÊN ---
name = st.text_input("Nhập tên của bạn:", placeholder="Ví dụ: Dev BE - Tuấn")

if name:
    st.subheader(f"Chào {name}, mời bạn chọn Story Point:")
    cols = st.columns(7)
    fibonacci = [1, 2, 3, 5, 8, 13, 21]
    
    for i, p in enumerate(fibonacci):
        # Dùng key để tránh trùng lặp button
        if cols[i].button(str(p), key=f"btn_{p}"):
            with server_state_lock["poker_data"]:
                # Streamlit-server-state yêu cầu gán lại object để nhận diện thay đổi
                current_points = server_state.points.copy()
                current_points[name] = p
                server_state.points = current_points
            st.toast(f"Bạn đã chọn {p} points!")

st.divider()

# --- HIỂN THỊ KẾT QUẢ ---
st.subheader("Kết quả đánh giá")

# Lấy dữ liệu từ kho chung
all_votes = server_state.points
is_reveal = server_state.reveal

if not all_votes:
    st.info("Đang chờ mọi người vote...")
else:
    voted_names = list(all_votes.keys())
    
    if not is_reveal:
        st.warning(f"🔔 Đã có {len(voted_names)} người vote. Đang ẩn kết quả...")
        # Hiển thị danh sách người đã vote để PM biết ai chưa làm
        c1, c2 = st.columns(2)
        for idx, n in enumerate(voted_names):
            if idx % 2 == 0:
                c1.write(f"✅ **{n}**")
            else:
                c2.write(f"✅ **{n}**")
    else:
        st.success("🎉 KẾT QUẢ CHI TIẾT:")
        # Hiển thị kết quả cụ thể
        for n, p in all_votes.items():
            st.write(f"👤 **{n}**: {p} Points")
        
        # Tính trung bình
        avg = sum(all_votes.values()) / len(all_votes)
        st.metric("Điểm trung bình", f"{avg:.1f}")
        st.balloons()
