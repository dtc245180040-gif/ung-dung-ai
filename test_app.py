import pytest
import os
import sqlite3
from unittest.mock import patch
from app import app, init_db, get_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    test_db = 'database/test_canteen.db'
    
    import app as app_module
    original_get_db = app_module.get_db
    original_client = app_module.client
    
    def get_test_db():
        conn = sqlite3.connect(test_db)
        conn.row_factory = sqlite3.Row
        return conn

    app_module.get_db = get_test_db
    app_module.DATABASE = test_db
    
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except:
            pass
        
    app_module.init_db()
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
            sess['role'] = 'admin'
        yield client
        
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except:
            pass
    
    app_module.get_db = original_get_db
    app_module.DATABASE = "database/canteen.db"
    app_module.client = original_client


# ============================================================================
# NHÓM 1: KIỂM THỬ ĐÚNG (HAPPY PATH / POSITIVE TESTS) - TIÊU CHÍ 3.1
# ============================================================================

def test_login_success(client):
    """TC_POS_01: Đăng nhập thành công với tài khoản hợp lệ."""
    rv = client.post('/', data=dict(
        username='admin',
        password='123456'
    ), follow_redirects=False)
    # Redirect sang dashboard khi đúng
    assert rv.status_code == 302
    assert '/dashboard' in rv.headers.get('Location', '')

def test_add_food_success(client):
    """TC_POS_02: Thêm món ăn mới với dữ liệu hợp lệ."""
    rv = client.post('/foods/add', data=dict(
        name='Bún chả Hà Nội',
        category='Món nước',
        price='40000',
        quantity='25'
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert b"B\xc3\xban ch\xe1\xba\xa3 H\xc3\xa0 N\xe1\xbb\x99i" in rv.data or "Bún chả Hà Nội" in rv.text

def test_add_ingredient_success(client):
    """TC_POS_03: Thêm nguyên liệu hợp lệ vào kho."""
    rv = client.post('/ingredients/add', data=dict(
        name='Hành lá',
        unit='kg',
        quantity='5',
        min_quantity='2'
    ), follow_redirects=True)
    assert rv.status_code == 200

def test_add_supplier_success(client):
    """TC_POS_04: Thêm nhà cung cấp hợp lệ."""
    rv = client.post('/suppliers/add', data=dict(
        name='Công ty Nông sản Sạch',
        phone='0987654321',
        address='Hà Nội'
    ), follow_redirects=True)
    assert rv.status_code == 200

def test_sales_and_stock_deduction(client):
    """TC_POS_05: Bán hàng thành công và tự động trừ số lượng tồn kho."""
    import app as app_module
    conn = app_module.get_db()
    food = conn.execute("SELECT * FROM foods WHERE id = 1").fetchone()
    initial_qty = food['quantity']
    conn.close()

    sale_qty = 2
    rv = client.post('/sales/add', data=dict(
        food_id=1,
        quantity=sale_qty
    ), follow_redirects=True)
    assert rv.status_code == 200

    conn = app_module.get_db()
    updated_food = conn.execute("SELECT * FROM foods WHERE id = 1").fetchone()
    conn.close()
    assert updated_food['quantity'] == initial_qty - sale_qty

def test_add_feedback_success(client):
    """TC_POS_06: Gửi phản hồi khách hàng hợp lệ (5 sao)."""
    rv = client.post('/feedback/add', data=dict(
        food_id=1,
        customer_name='Nguyễn Văn A',
        rating=5,
        comment='Món ăn rất ngon, phục vụ nhanh!'
    ), follow_redirects=True)
    assert rv.status_code == 200

def test_dashboard_and_reports_access(client):
    """TC_POS_07: Truy cập Dashboard và trang Thống kê Báo cáo thành công."""
    rv_dash = client.get('/dashboard')
    assert rv_dash.status_code == 200
    rv_rep = client.get('/reports')
    assert rv_rep.status_code == 200


# ============================================================================
# NHÓM 2: KIỂM THỬ SAI (NEGATIVE TESTS) - TIÊU CHÍ 3.1
# ============================================================================

def test_login_wrong_password(client):
    """TC_NEG_01: Đăng nhập sai mật khẩu bị từ chối."""
    rv = client.post('/', data=dict(
        username='admin',
        password='wrongpassword'
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert "Tài khoản hoặc mật khẩu không đúng" in rv.text or b"T\xc3\xa0i kho\xe1\xba\xa3n" in rv.data

def test_add_food_missing_required_fields(client):
    """TC_NEG_02: Thêm món ăn bỏ trống trường bắt buộc trả về lỗi 400."""
    rv = client.post('/foods/add', data=dict(
        name='',
        category='Cơm',
        price='30000',
        quantity='10'
    ))
    assert rv.status_code == 400

def test_add_food_negative_values(client):
    """TC_NEG_03: Thêm món ăn có giá tiền hoặc số lượng âm trả về 400."""
    rv = client.post('/foods/add', data=dict(
        name='Món lỗi',
        category='Cơm',
        price='-10000',
        quantity='5'
    ))
    assert rv.status_code == 400

def test_sales_exceed_available_quantity(client):
    """TC_NEG_04: Bán hàng vượt quá số lượng tồn kho trả về 400."""
    rv = client.post('/sales/add', data=dict(
        food_id=1,
        quantity=99999
    ))
    assert rv.status_code == 400
    assert "vượt quá" in rv.text or b"v\xc6\xb0\xe1\xbb\xa3t" in rv.data

def test_sales_zero_or_negative_quantity(client):
    """TC_NEG_05: Bán hàng với số lượng <= 0 trả về 400."""
    rv = client.post('/sales/add', data=dict(
        food_id=1,
        quantity=0
    ))
    assert rv.status_code == 400

def test_feedback_invalid_rating(client):
    """TC_NEG_06: Gửi phản hồi với số sao ngoài khoảng 1-5 trả về 400."""
    rv = client.post('/feedback/add', data=dict(
        food_id=1,
        customer_name='Học sinh',
        rating=6,
        comment='Quá tốt'
    ))
    assert rv.status_code == 400

def test_staff_role_forbidden_on_admin_actions(client):
    """TC_NEG_07: Tài khoản nhân viên (staff) bị chặn (403) khi thực hiện hành động admin."""
    with client.session_transaction() as sess:
        sess['role'] = 'staff'
        sess['username'] = 'nhanvien'
    
    # Staff cố tình xóa món ăn
    rv = client.post('/foods/delete/1')
    assert rv.status_code == 403

    # Staff cố tình thêm món ăn
    rv = client.post('/foods/add', data=dict(
        name='Món staff thêm', category='Cơm', price='30000', quantity='5'
    ))
    assert rv.status_code == 403


# ============================================================================
# NHÓM 3: KIỂM THỬ BIÊN (BOUNDARY TESTS) - TIÊU CHÍ 3.1
# ============================================================================

def test_sales_exact_stock_boundary(client):
    """TC_BND_01: Bán vừa đúng toàn bộ số lượng tồn kho (tồn kho về đúng 0)."""
    import app as app_module
    conn = app_module.get_db()
    food = conn.execute("SELECT * FROM foods WHERE id = 2").fetchone()
    stock = food['quantity']
    conn.close()

    rv = client.post('/sales/add', data=dict(
        food_id=2,
        quantity=stock
    ), follow_redirects=True)
    assert rv.status_code == 200

    conn = app_module.get_db()
    updated_food = conn.execute("SELECT * FROM foods WHERE id = 2").fetchone()
    conn.close()
    assert updated_food['quantity'] == 0

def test_feedback_rating_boundaries(client):
    """TC_BND_02: Đánh giá tại chính xác biên dưới (1 sao) và biên trên (5 sao)."""
    # Biên dưới: 1 sao
    rv1 = client.post('/feedback/add', data=dict(
        food_id=1, customer_name='Khách 1', rating=1, comment='Biên dưới'
    ), follow_redirects=True)
    assert rv1.status_code == 200

    # Biên trên: 5 sao
    rv5 = client.post('/feedback/add', data=dict(
        food_id=1, customer_name='Khách 2', rating=5, comment='Biên trên'
    ), follow_redirects=True)
    assert rv5.status_code == 200

def test_food_search_empty_keyword(client):
    """TC_BND_03: Tìm kiếm với chuỗi rỗng trả về toàn bộ danh sách."""
    rv = client.get('/foods?keyword=')
    assert rv.status_code == 200


# ============================================================================
# NHÓM 4: KIỂM THỬ TÍCH HỢP AI & XỬ LÝ LỖI / FALLBACK - TIÊU CHÍ 2.4 & 3.3
# ============================================================================

def test_ai_endpoints_fallback_when_api_fails(client):
    """TC_AI_01: Khi API AI lỗi hoặc mất kết nối, hệ thống kích hoạt Fallback Rule-Based an toàn."""
    import app as app_module
    # Thêm feedback mẫu để đảm bảo có dữ liệu gửi cho AI phân tích
    client.post('/feedback/add', data=dict(
        food_id=1, customer_name='Test Fallback', rating=4, comment='Ngon nhưng cần cải thiện'
    ))
    
    # Giả lập call_gemini trả về lỗi timeout/mất mạng
    with patch.object(app_module, 'call_gemini', return_value=(None, "Lỗi kết nối giả lập")):
        rv_rec = client.get('/ai-recommend')
        assert rv_rec.status_code == 200
        assert "đề xuất cơ bản" in rv_rec.text or "Không thể kết nối" in rv_rec.text

        rv_fb = client.get('/ai-feedback')
        assert rv_fb.status_code == 200
        assert "thống kê phản hồi cơ bản" in rv_fb.text or "Không thể kết nối" in rv_fb.text

        rv_rep = client.get('/ai-report')
        assert rv_rep.status_code == 200
        assert "Không thể kết nối" in rv_rep.text or "doanh thu" in rv_rep.text

def test_ai_chat_api(client):
    """TC_AI_02: Kiểm tra endpoint Chatbot AI /api/chat với input hợp lệ và rỗng."""
    import app as app_module
    # Input rỗng
    rv_empty = client.post('/api/chat', json={"message": "   "})
    assert rv_empty.status_code == 400

    # Input hợp lệ với mock response nhanh
    with patch.object(app_module, 'call_gemini', return_value=("Chào bạn, tôi là trợ lý Căng tin!", None)):
        rv_chat = client.post('/api/chat', json={"message": "Hôm nay có bao nhiêu món?"})
        assert rv_chat.status_code == 200
        data = rv_chat.get_json()
        assert "trợ lý Căng tin" in data["response"]

def test_ai_chat_page_access(client):
    """TC_AI_03: Truy cập trang Trợ lý AI Căng tin (/ai-chat) thành công."""
    rv = client.get('/ai-chat')
    assert rv.status_code == 200
    assert "Trợ lý AI" in rv.text

