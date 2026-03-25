import streamlit as st

# Cấu hình giao diện
st.set_page_config(page_title="Agile Planning Poker", layout="centered")

st.title("🃏 Agile Planning Poker")
st.write("Dành cho Team 20 người - PM Điều khiển")

# Giả lập database đơn giản bằng Session State (Trong thực tế nên dùng database/socket)
if 'points' not in st.session_state:
    st.session_state.points = {}
if 'reveal' not in st.session_state:
    st.session_state.reveal = False

# Sidebar cho PM (Host)
with st.sidebar:
    st.header("Admin Control")
    password = st.text_input("Mật khẩu Admin", type="password")
    if password == "admin123": # Bạn có thể đổi pass này
        if st.button("Lật bài (Reveal)"):
            st.session_state.reveal = True
        if st.button("Làm mới (Reset)"):
            st.session_state.points = {}
            st.session_state.reveal = False
            st.rerun()
        st.success("Bạn đang là Host!")

# Giao diện cho Thành viên
name = st.text_input("Nhập tên của bạn:", placeholder="Ví dụ: Dev BE - Tuấn")

if name:
    st.subheader(f"Chào {name}, mời bạn chọn Story Point:")
    cols = st.columns(7)
    fibonacci = [1, 2, 3, 5, 8, 13, 21]
    
    for i, p in enumerate(fibonacci):
        if cols[i].button(str(p)):
            st.session_state.points[name] = p
            st.toast(f"Bạn đã chọn {p} points!")

st.divider()

# Hiển thị kết quả
st.subheader("Kết quả đánh giá")
if not st.session_state.points:
    st.info("Đang chờ mọi người vote...")
else:
    # Danh sách những người đã vote
    voted_names = list(st.session_state.points.keys())
    
    if not st.session_state.reveal:
        st.warning(f"Đã có {len(voted_names)} người vote. Đang ẩn kết quả...")
        for n in voted_names:
            st.write(f"✅ {n} đã xong.")
    else:
        # Hiện kết quả chi tiết
        for n, p in st.session_state.points.items():
            st.write(f"👤 **{n}**: {p} Points")
        
        # Tính trung bình
        avg = sum(st.session_state.points.values()) / len(st.session_state.points)
        st.success(f"Điểm trung bình: **{avg:.1f}**")