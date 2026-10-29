import sqlite3
import os

from functools import wraps

from flask import Flask, render_template, request, redirect, session, jsonify

from dotenv import load_dotenv
from google import genai
from prompts.recommend_prompt import (
    SYSTEM_PROMPT as RECOMMEND_SYSTEM_PROMPT,
    USER_PROMPT as RECOMMEND_USER_PROMPT
)

from prompts.feedback_prompt import (
    SYSTEM_PROMPT as FEEDBACK_SYSTEM_PROMPT,
    USER_PROMPT as FEEDBACK_USER_PROMPT
)

from prompts.report_prompt import (
    SYSTEM_PROMPT as REPORT_SYSTEM_PROMPT,
    USER_PROMPT as REPORT_USER_PROMPT
)

from prompts.chat_prompt import SYSTEM_PROMPT as CHAT_SYSTEM_PROMPT

import time

load_dotenv(override=True)

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except Exception:
        pass

# Lấy API Key từ biến môi trường (.env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        safe_print(f"[Gemini] Không thể khởi tạo genai.Client: {e}")

# Danh sách model ưu tiên: thử model hoạt động tốt nhất trước, nếu lỗi thì fallback
GEMINI_MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]

# Cache kết quả AI để tránh lặp lại request, tránh quá tải quota và giúp trang web mở tức thì
_AI_CACHE = {}

def get_cached_ai(key, ttl=900):
    """Lấy kết quả AI từ cache nếu còn hạn (mặc định 15 phút), bỏ qua khi testing."""
    if app.config.get("TESTING"):
        return None
    if key in _AI_CACHE:
        val, ts = _AI_CACHE[key]
        if time.time() - ts < ttl:
            return val
    return None

def set_cached_ai(key, val):
    """Lưu kết quả AI vào cache."""
    _AI_CACHE[key] = (val, time.time())

def generate_fallback_recommend(foods, ingredients, sales):
    top_dishes = [s["food_name"] for s in sales[:3]] if sales else ["Cơm gà", "Phở bò"]
    low_stock = [i["name"] for i in ingredients if i["quantity"] <= i["min_quantity"]]
    
    text = "### 📋 Đề xuất Thực đơn Thông minh (Dự phòng tự động từ CSDL)\n\n"
    text += f"1. **Món ăn nên ưu tiên phục vụ:** {', '.join(top_dishes)} (Đây là các món có lượt mua cao và nhu cầu ổn định nhất trong ngày).\n\n"
    if low_stock:
        text += f"2. **Cảnh báo nguyên liệu cần nhập gấp:** Các nguyên liệu {', '.join(low_stock)} hiện đã chạm hoặc thấp hơn định mức an toàn. Cần bổ sung trước ca phục vụ tiếp theo.\n\n"
    else:
        text += "2. **Tình trạng kho nguyên liệu:** Toàn bộ nguyên liệu đều đang ở mức an toàn, sẵn sàng phục vụ thực đơn đầy đủ.\n\n"
    text += "3. **Khuyến nghị kinh doanh:** Tiếp tục duy trì thực đơn bán chạy, có thể kết hợp đồ uống (trà sữa, nước ngọt) vào combo để tối ưu doanh thu trung bình trên mỗi đơn hàng.\n\n"
    text += "*(Hệ thống đang sử dụng đề xuất cơ bản dựa trên dữ liệu bán hàng và tồn kho)*"
    return text

def generate_fallback_feedback(feedbacks, positive, neutral, negative):
    total = len(feedbacks)
    text = "### 🧠 Phân tích Đánh giá Khách hàng (Dự phòng tự động từ CSDL)\n\n"
    text += f"- **Tổng số lượt đánh giá:** {total} lượt (Tích cực: {positive}, Trung lập: {neutral}, Cần cải thiện: {negative}).\n\n"
    if positive >= negative:
        text += "- **Đánh giá chung:** Đa số học sinh và giáo viên đánh giá tích cực về chất lượng món ăn và thái độ phục vụ.\n\n"
    else:
        text += "- **Đánh giá chung:** Có một số phản hồi chưa hài lòng, quản lý nên kiểm tra lại chất lượng món ăn và thời gian phục vụ.\n\n"
    text += "- **Hành động đề xuất:** Tiếp tục duy trì chất lượng các món được khen, đồng thời khảo sát thêm ý kiến khách hàng vào giờ cao điểm.\n\n"
    text += "*(Hệ thống vẫn hiển thị thống kê phản hồi cơ bản)*"
    return text

def generate_fallback_report(total_revenue, total_quantity, total_orders, best_selling):
    top_names = [b["food_name"] for b in best_selling[:3]] if best_selling else ["Cơm gà", "Phở bò"]
    text = "### 📊 Báo cáo Doanh thu & Chiến lược Kinh doanh (Dự phòng tự động từ CSDL)\n\n"
    text += f"- **Tổng doanh thu:** {total_revenue:,.0f} VNĐ qua {total_orders} giao dịch bán hàng ({total_quantity} suất món ăn đã phục vụ).\n\n"
    text += f"- **Mặt hàng chủ lực:** {', '.join(top_names)} đóng góp tỷ trọng doanh thu cao nhất cho căng tin.\n\n"
    text += "- **3 Giải pháp gia tăng doanh thu:**\n"
    text += "  1. **Tạo combo trưa tiện lợi:** Ghép món ăn chính + đồ uống với mức giá ưu đãi nhẹ để tăng giá trị đơn hàng.\n"
    text += "  2. **Tối ưu hóa giờ cao điểm:** Chuẩn bị sẵn các phần ăn mang đi trong khung giờ 11h30 - 12h30 để tăng tốc độ phục vụ.\n"
    text += "  3. **Kiểm soát chi phí nguyên liệu:** Nhập hàng theo định mức tiêu thụ thực tế để tránh lãng phí.\n\n"
    text += "*(Hệ thống đang hiển thị phân tích doanh thu cơ bản từ CSDL)*"
    return text

from concurrent.futures import ThreadPoolExecutor, TimeoutError

_ai_executor = ThreadPoolExecutor(max_workers=4)

def _call_gemini_internal(contents, system_instruction=None, max_retries=1):
    if not client:
        return None, "Chưa cấu hình GEMINI_API_KEY."
    
    from google.genai import types
    
    last_error = ""
    for model_name in GEMINI_MODELS:
        for attempt in range(max_retries):
            try:
                config = None
                if system_instruction:
                    config = types.GenerateContentConfig(
                        system_instruction=system_instruction
                    )
                
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config
                )
                if response and response.text:
                    return response.text, None  # Thành công
            except Exception as e:
                error_str = str(e)
                last_error = error_str
                safe_print(f"[Gemini] Model={model_name}, Attempt={attempt+1}/{max_retries}, Error: {error_str[:120]}")
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    break
                elif "503" in error_str or "UNAVAILABLE" in error_str or "overloaded" in error_str:
                    time.sleep(0.5)
                    continue
                else:
                    break
    
    return None, f"Không thể kết nối Gemini AI lúc này: {last_error}"

def call_gemini(contents, system_instruction=None, max_retries=1, timeout=8):
    """Gọi Gemini API với timeout tối đa (mặc định 8s), tự động fallback khi chậm hoặc quá tải."""
    if not client:
        return None, "Chưa cấu hình GEMINI_API_KEY."
    try:
        future = _ai_executor.submit(_call_gemini_internal, contents, system_instruction, max_retries)
        return future.result(timeout=timeout)
    except TimeoutError:
        safe_print(f"[Gemini] Request timed out sau {timeout}s.")
        return None, "Gemini API phản hồi quá chậm (timeout)."
    except Exception as e:
        return None, str(e)

def warm_up_cache():
    """Khởi tạo trước cache phân tích CSDL để trang web mở tức thì không bị treo."""
    try:
        conn = get_db()
        foods = conn.execute("SELECT id, name, price, quantity, status FROM foods").fetchall()
        ingredients = conn.execute("SELECT name, quantity, unit, min_quantity FROM ingredients").fetchall()
        sales = conn.execute("""
            SELECT foods.name AS food_name, SUM(sales.quantity) AS total_quantity
            FROM sales JOIN foods ON sales.food_id = foods.id
            GROUP BY sales.food_id ORDER BY total_quantity DESC LIMIT 5
        """).fetchall()
        feedbacks = conn.execute("""
            SELECT feedback.rating, feedback.comment, foods.name AS food_name
            FROM feedback LEFT JOIN foods ON feedback.food_id = foods.id
        """).fetchall()
        sales_summary = conn.execute("SELECT COUNT(*), COALESCE(SUM(quantity), 0), COALESCE(SUM(total), 0) FROM sales").fetchone()
        conn.close()

        set_cached_ai("recommend", generate_fallback_recommend(foods, ingredients, sales))
        set_cached_ai("feedback", generate_fallback_feedback(feedbacks, 1, 0, 0))
        set_cached_ai("report", generate_fallback_report(sales_summary[2], sales_summary[1], sales_summary[0], sales))
    except Exception as e:
        pass


app = Flask(__name__)
app.secret_key = "smart-canteen-secret-key"
DATABASE = "database/canteen.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/")

        if session.get("role") != "admin":
            return "Bạn không có quyền thực hiện chức năng này!", 403

        return f(*args, **kwargs)

    return decorated_function
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Đang bán'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            quantity REAL DEFAULT 0,
            min_quantity REAL DEFAULT 0
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            address TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id INTEGER,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            sale_date TEXT NOT NULL,
            FOREIGN KEY (food_id) REFERENCES foods(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id INTEGER,
            customer_name TEXT,
            rating INTEGER,
            comment TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (food_id) REFERENCES foods(id)
        )
    """)

    # Bảng tài khoản người dùng
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Dữ liệu món ăn mẫu
    count = conn.execute(
        "SELECT COUNT(*) FROM foods"
    ).fetchone()[0]

    if count == 0:
        conn.executemany("""
            INSERT INTO foods
            (name, category, price, quantity, status)
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("Cơm gà", "Cơm", 30000, 50, "Đang bán"),
            ("Phở bò", "Món nước", 35000, 40, "Đang bán"),
            ("Mì xào", "Mì", 25000, 35, "Đang bán"),
            ("Trà sữa", "Đồ uống", 20000, 60, "Đang bán"),
            ("Bánh mì", "Đồ ăn nhanh", 15000, 45, "Đang bán")
        ])

    # Dữ liệu nguyên liệu mẫu
    ingredient_count = conn.execute(
        "SELECT COUNT(*) FROM ingredients"
    ).fetchone()[0]

    if ingredient_count == 0:
        conn.executemany("""
            INSERT INTO ingredients
            (name, unit, quantity, min_quantity)
            VALUES (?, ?, ?, ?)
        """, [
            ("Thịt gà", "kg", 4, 10),
            ("Thịt bò", "kg", 12, 8),
            ("Rau xanh", "kg", 3, 8),
            ("Trứng", "quả", 25, 30),
            ("Gạo", "kg", 50, 20)
        ])

    # Tài khoản mẫu
    user_count = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    if user_count == 0:
        conn.executemany("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, [
            ("admin", "123456", "admin"),
            ("nhanvien", "123456", "staff")
        ])

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            return render_template(
                "login.html",
                error="Vui lòng nhập tài khoản và mật khẩu!"
            )

        conn = get_db()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE username = ? AND password = ?
        """, (
            username,
            password
        )).fetchone()

        conn.close()

        if user is None:
            return render_template(
                "login.html",
                error="Tài khoản hoặc mật khẩu không đúng!"
            )

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]

        return redirect("/dashboard")

    return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()

    food_count = conn.execute(
        "SELECT COUNT(*) FROM foods"
    ).fetchone()[0]

    ingredient_count = conn.execute(
        "SELECT COUNT(*) FROM ingredients"
    ).fetchone()[0]

    supplier_count = conn.execute(
        "SELECT COUNT(*) FROM suppliers"
    ).fetchone()[0]

    sale_count = conn.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    revenue = conn.execute(
        "SELECT COALESCE(SUM(total), 0) FROM sales"
    ).fetchone()[0]

    low_ingredients = conn.execute("""
        SELECT *
        FROM ingredients
        WHERE quantity <= min_quantity
        ORDER BY quantity ASC
    """).fetchall()

    best_selling = conn.execute("""
        SELECT
            foods.name,
            SUM(sales.quantity) AS total_sold
        FROM sales
        JOIN foods ON sales.food_id = foods.id
        GROUP BY sales.food_id
        ORDER BY total_sold DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        food_count=food_count,
        ingredient_count=ingredient_count,
        supplier_count=supplier_count,
        sale_count=sale_count,
        revenue=revenue,
        low_ingredients=low_ingredients,
        best_selling=best_selling
    )


@app.route("/foods")
@login_required
def foods():
    keyword = request.args.get("keyword", "").strip()

    conn = get_db()

    if keyword:
        foods = conn.execute("""
            SELECT * FROM foods
            WHERE name LIKE ? OR category LIKE ?
            ORDER BY id DESC
        """, (f"%{keyword}%", f"%{keyword}%")).fetchall()
    else:
        foods = conn.execute("""
            SELECT * FROM foods
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    return render_template(
    "foods.html",
    foods=foods,
    keyword=keyword,
    role=session.get("role")
)


@app.route("/foods/add", methods=["GET", "POST"])
@admin_required
def add_food():

    if request.method == "GET":
        return render_template("food_add.html")

    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    price = request.form.get("price", "").strip()
    quantity = request.form.get("quantity", "0").strip()

    if not name or not category or not price:
        return "Vui lòng nhập đầy đủ thông tin!", 400

    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        return "Giá hoặc số lượng không hợp lệ!", 400

    if price < 0 or quantity < 0:
        return "Giá và số lượng không được âm!", 400

    conn = get_db()

    conn.execute("""
        INSERT INTO foods
        (name, category, price, quantity, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        category,
        price,
        quantity,
        "Đang bán"
    ))

    conn.commit()
    conn.close()

    return redirect("/foods")


@app.route("/foods/delete/<int:food_id>", methods=["POST"])
@admin_required
def delete_food(food_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM foods WHERE id = ?",
        (food_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/foods")
@app.route("/foods/edit/<int:food_id>", methods=["GET", "POST"])
@admin_required
def edit_food(food_id):
    conn = get_db()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        price = request.form.get("price", "").strip()
        quantity = request.form.get("quantity", "0").strip()
        status = request.form.get("status", "Đang bán").strip()

        if not name or not category or not price:
            conn.close()
            return "Vui lòng nhập đầy đủ thông tin!", 400

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            conn.close()
            return "Giá hoặc số lượng không hợp lệ!", 400

        if price < 0 or quantity < 0:
            conn.close()
            return "Giá và số lượng không được âm!", 400

        conn.execute("""
            UPDATE foods
            SET name = ?,
                category = ?,
                price = ?,
                quantity = ?,
                status = ?
            WHERE id = ?
        """, (
            name,
            category,
            price,
            quantity,
            status,
            food_id
        ))

        conn.commit()
        conn.close()

        return redirect("/foods")

    food = conn.execute(
        "SELECT * FROM foods WHERE id = ?",
        (food_id,)
    ).fetchone()

    conn.close()

    if food is None:
        return "Không tìm thấy món ăn!", 404

    return render_template("edit_food.html", food=food)    


@app.route("/ingredients")
@login_required
def ingredients():
    keyword = request.args.get("keyword", "").strip()

    conn = get_db()

    if keyword:
        ingredients = conn.execute("""
            SELECT * FROM ingredients
            WHERE name LIKE ? OR unit LIKE ?
            ORDER BY id DESC
        """, (f"%{keyword}%", f"%{keyword}%")).fetchall()
    else:
        ingredients = conn.execute("""
            SELECT * FROM ingredients
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    return render_template(
        "ingredients.html",
        ingredients=ingredients,
        keyword=keyword,
        role=session.get("role")
    )
@app.route("/ingredients/add", methods=["POST"])
@admin_required
def add_ingredient():
    name = request.form.get("name", "").strip()
    unit = request.form.get("unit", "").strip()
    quantity = request.form.get("quantity", "0").strip()
    min_quantity = request.form.get("min_quantity", "0").strip()

    if not name or not unit:
        return "Vui lòng nhập đầy đủ thông tin!", 400

    try:
        quantity = float(quantity)
        min_quantity = float(min_quantity)
    except ValueError:
        return "Số lượng không hợp lệ!", 400

    if quantity < 0 or min_quantity < 0:
        return "Số lượng không được âm!", 400

    conn = get_db()

    conn.execute("""
        INSERT INTO ingredients
        (name, unit, quantity, min_quantity)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        unit,
        quantity,
        min_quantity
    ))

    conn.commit()
    conn.close()

    return redirect("/ingredients")   
@app.route("/ingredients/delete/<int:ingredient_id>", methods=["POST"])
@admin_required
def delete_ingredient(ingredient_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM ingredients WHERE id = ?",
        (ingredient_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/ingredients")
@app.route("/ingredients/edit/<int:ingredient_id>", methods=["GET", "POST"])
@admin_required
def edit_ingredient(ingredient_id):
    conn = get_db()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        unit = request.form.get("unit", "").strip()
        quantity = request.form.get("quantity", "0").strip()
        min_quantity = request.form.get("min_quantity", "0").strip()

        if not name or not unit:
            conn.close()
            return "Vui lòng nhập đầy đủ thông tin!", 400

        try:
            quantity = float(quantity)
            min_quantity = float(min_quantity)
        except ValueError:
            conn.close()
            return "Số lượng không hợp lệ!", 400

        if quantity < 0 or min_quantity < 0:
            conn.close()
            return "Số lượng không được âm!", 400

        conn.execute("""
            UPDATE ingredients
            SET name = ?,
                unit = ?,
                quantity = ?,
                min_quantity = ?
            WHERE id = ?
        """, (
            name,
            unit,
            quantity,
            min_quantity,
            ingredient_id
        ))

        conn.commit()
        conn.close()

        return redirect("/ingredients")

    ingredient = conn.execute(
        "SELECT * FROM ingredients WHERE id = ?",
        (ingredient_id,)
    ).fetchone()

    conn.close()

    if ingredient is None:
        return "Không tìm thấy nguyên liệu!", 404

    return render_template(
        "edit_ingredient.html",
        ingredient=ingredient
    ) 


@app.route("/suppliers")
@login_required
def suppliers():
    keyword = request.args.get("keyword", "").strip()

    conn = get_db()

    if keyword:
        suppliers = conn.execute("""
            SELECT * FROM suppliers
            WHERE name LIKE ?
               OR phone LIKE ?
               OR address LIKE ?
            ORDER BY id DESC
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )).fetchall()
    else:
        suppliers = conn.execute("""
            SELECT * FROM suppliers
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    return render_template(
        "suppliers.html",
        suppliers=suppliers,
        keyword=keyword,
        role=session.get("role")
    )


@app.route("/suppliers/add", methods=["POST"])
@admin_required
def add_supplier():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()

    if not name:
        return "Vui lòng nhập tên nhà cung cấp!", 400

    conn = get_db()

    conn.execute("""
        INSERT INTO suppliers (name, phone, address)
        VALUES (?, ?, ?)
    """, (
        name,
        phone,
        address
    ))

    conn.commit()
    conn.close()

    return redirect("/suppliers")
@app.route("/suppliers/delete/<int:supplier_id>", methods=["POST"])
@admin_required
def delete_supplier(supplier_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM suppliers WHERE id = ?",
        (supplier_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/suppliers")
@app.route("/suppliers/edit/<int:supplier_id>", methods=["GET", "POST"])
@admin_required
def edit_supplier(supplier_id):
    conn = get_db()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not name:
            conn.close()
            return "Vui lòng nhập tên nhà cung cấp!", 400

        conn.execute("""
            UPDATE suppliers
            SET name = ?,
                phone = ?,
                address = ?
            WHERE id = ?
        """, (
            name,
            phone,
            address,
            supplier_id
        ))

        conn.commit()
        conn.close()

        return redirect("/suppliers")

    supplier = conn.execute(
        "SELECT * FROM suppliers WHERE id = ?",
        (supplier_id,)
    ).fetchone()

    conn.close()

    if supplier is None:
        return "Không tìm thấy nhà cung cấp!", 404

    return render_template(
        "edit_supplier.html",
        supplier=supplier
    )


@app.route("/sales")
@login_required
def sales():
    keyword = request.args.get("keyword", "").strip()

    conn = get_db()

    if keyword:
        sales = conn.execute("""
            SELECT 
                sales.id,
                foods.name AS food_name,
                sales.quantity,
                sales.total,
                sales.sale_date
            FROM sales
            LEFT JOIN foods ON sales.food_id = foods.id
            WHERE foods.name LIKE ?
            ORDER BY sales.id DESC
        """, (f"%{keyword}%",)).fetchall()
    else:
        sales = conn.execute("""
            SELECT 
                sales.id,
                foods.name AS food_name,
                sales.quantity,
                sales.total,
                sales.sale_date
            FROM sales
            LEFT JOIN foods ON sales.food_id = foods.id
            ORDER BY sales.id DESC
        """).fetchall()

    foods = conn.execute("""
        SELECT * FROM foods
        WHERE status = 'Đang bán'
        ORDER BY name
    """).fetchall()

    conn.close()

    return render_template(
        "sales.html",
        sales=sales,
        foods=foods,
        keyword=keyword
    )
@app.route("/sales/add", methods=["POST"])
@login_required
def add_sale():
    food_id = request.form.get("food_id", "").strip()
    quantity = request.form.get("quantity", "").strip()

    if not food_id or not quantity:
        return "Vui lòng nhập đầy đủ thông tin!", 400

    try:
        food_id = int(food_id)
        quantity = int(quantity)
    except ValueError:
        return "Dữ liệu không hợp lệ!", 400

    if quantity <= 0:
        return "Số lượng phải lớn hơn 0!", 400

    conn = get_db()

    food = conn.execute(
        "SELECT * FROM foods WHERE id = ?",
        (food_id,)
    ).fetchone()

    if food is None:
        conn.close()
        return "Không tìm thấy món ăn!", 404

    if quantity > food["quantity"]:
        conn.close()
        return "Số lượng bán vượt quá số lượng món ăn hiện có!", 400

    total = food["price"] * quantity

    conn.execute("""
        INSERT INTO sales
        (food_id, quantity, total, sale_date)
        VALUES (?, ?, ?, datetime('now', 'localtime'))
    """, (
        food_id,
        quantity,
        total
    ))

    conn.execute("""
        UPDATE foods
        SET quantity = quantity - ?
        WHERE id = ?
    """, (
        quantity,
        food_id
    ))

    conn.commit()
    conn.close()

    return redirect("/sales")
@app.route("/sales/delete/<int:sale_id>", methods=["POST"])
@admin_required
def delete_sale(sale_id):
    conn = get_db()

    sale = conn.execute(
        "SELECT * FROM sales WHERE id = ?",
        (sale_id,)
    ).fetchone()

    if sale is None:
        conn.close()
        return "Không tìm thấy giao dịch!", 404

    conn.execute(
        "UPDATE foods SET quantity = quantity + ? WHERE id = ?",
        (sale["quantity"], sale["food_id"])
    )

    conn.execute(
        "DELETE FROM sales WHERE id = ?",
        (sale_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/sales")


@app.route("/feedback")
@login_required
def feedback():
    conn = get_db()

    feedbacks = conn.execute("""
        SELECT
            feedback.id,
            foods.name AS food_name,
            feedback.customer_name,
            feedback.rating,
            feedback.comment,
            feedback.created_at
        FROM feedback
        LEFT JOIN foods ON feedback.food_id = foods.id
        ORDER BY feedback.id DESC
    """).fetchall()

    foods = conn.execute("""
        SELECT * FROM foods
        ORDER BY name
    """).fetchall()

    conn.close()

    return render_template(
        "feedback.html",
        feedbacks=feedbacks,
        foods=foods
    )
@app.route("/feedback/add", methods=["POST"])
@login_required
def add_feedback():
    food_id = request.form.get("food_id", "").strip()
    customer_name = request.form.get("customer_name", "").strip()
    rating = request.form.get("rating", "").strip()
    comment = request.form.get("comment", "").strip()

    if not food_id or not rating or not comment:
        return "Vui lòng nhập đầy đủ thông tin!", 400

    try:
        food_id = int(food_id)
        rating = int(rating)
    except ValueError:
        return "Dữ liệu không hợp lệ!", 400

    if rating < 1 or rating > 5:
        return "Đánh giá phải từ 1 đến 5 sao!", 400

    conn = get_db()

    food = conn.execute(
        "SELECT id FROM foods WHERE id = ?",
        (food_id,)
    ).fetchone()

    if food is None:
        conn.close()
        return "Không tìm thấy món ăn!", 404

    conn.execute("""
        INSERT INTO feedback
        (food_id, customer_name, rating, comment, created_at)
        VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
    """, (
        food_id,
        customer_name,
        rating,
        comment
    ))

    conn.commit()
    conn.close()

    return redirect("/feedback")
@app.route("/feedback/delete/<int:feedback_id>", methods=["POST"])
@admin_required
def delete_feedback(feedback_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM feedback WHERE id = ?",
        (feedback_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/feedback")


@app.route("/reports")
@login_required
def reports():
    conn = get_db()

    total_revenue = conn.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM sales
    """).fetchone()[0]

    total_sales = conn.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM sales
    """).fetchone()[0]

    transaction_count = conn.execute("""
        SELECT COUNT(*)
        FROM sales
    """).fetchone()[0]

    average_order = conn.execute("""
        SELECT COALESCE(AVG(total), 0)
        FROM sales
    """).fetchone()[0]

    best_selling = conn.execute("""
        SELECT
            foods.name,
            SUM(sales.quantity) AS total_sold,
            SUM(sales.total) AS revenue
        FROM sales
        JOIN foods ON sales.food_id = foods.id
        GROUP BY sales.food_id
        ORDER BY total_sold DESC
        LIMIT 10
    """).fetchall()

    daily_revenue = conn.execute("""
        SELECT
            DATE(sale_date) AS sale_day,
            SUM(total) AS revenue
        FROM sales
        GROUP BY DATE(sale_date)
        ORDER BY sale_day DESC
        LIMIT 7
    """).fetchall()

    low_ingredients = conn.execute("""
        SELECT *
        FROM ingredients
        WHERE quantity <= min_quantity
        ORDER BY quantity ASC
    """).fetchall()

    conn.close()

    return render_template(
        "reports.html",
        total_revenue=total_revenue,
        total_sales=total_sales,
        transaction_count=transaction_count,
        average_order=average_order,
        best_selling=best_selling,
        daily_revenue=daily_revenue,
        low_ingredients=low_ingredients
    )
@app.route("/ai-recommend")
@login_required
def ai_recommend():

    conn = get_db()

    # Lấy danh sách món ăn
    foods = conn.execute("""
        SELECT id, name, price, quantity, status
        FROM foods
        ORDER BY id DESC
    """).fetchall()

    # Lấy nguyên liệu
    ingredients = conn.execute("""
        SELECT name, quantity, unit, min_quantity
        FROM ingredients
        ORDER BY quantity ASC
    """).fetchall()

    # Thống kê món bán chạy
    sales = conn.execute("""
        SELECT
            foods.name AS food_name,
            SUM(sales.quantity) AS total_quantity
        FROM sales
        JOIN foods ON sales.food_id = foods.id
        GROUP BY sales.food_id
        ORDER BY total_quantity DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    # ==============================
    # TẠO DANH SÁCH ĐỀ XUẤT CƠ BẢN
    # ==============================

    recommendations = []

    for food in foods:

        food_name = food["name"]

        sold = 0

        for sale in sales:
            if sale["food_name"] == food_name:
                sold = sale["total_quantity"]
                break

        if sold >= 5:
            reason = "Món bán chạy, nên ưu tiên đưa vào thực đơn."

        elif sold >= 1:
            reason = "Món có doanh số ổn định, có thể tiếp tục duy trì."

        else:
            reason = "Món chưa có nhiều dữ liệu bán hàng, có thể dùng để đa dạng thực đơn."

        recommendations.append({
            "name": food_name,
            "price": food["price"],
            "sold": sold,
            "reason": reason
        })

    # ==============================
    # GỌI GEMINI AI HOẶC SỬ DỤNG CACHE / FALLBACK
    # ==============================

    ai_text = get_cached_ai("recommend")

    if not ai_text:
        if client:
            food_data = []
            for food in foods:
                food_data.append({
                    "name": food["name"],
                    "price": food["price"],
                    "quantity": food["quantity"],
                    "status": food["status"]
                })

            ingredient_data = []
            for ingredient in ingredients:
                ingredient_data.append({
                    "name": ingredient["name"],
                    "quantity": ingredient["quantity"],
                    "unit": ingredient["unit"],
                    "min_quantity": ingredient["min_quantity"]
                })

            sales_data = []
            for sale in sales:
                sales_data.append({
                    "food_name": sale["food_name"],
                    "total_quantity": sale["total_quantity"]
                })

            prompt = RECOMMEND_SYSTEM_PROMPT + "\n\n" + RECOMMEND_USER_PROMPT.format(
                food_data=food_data,
                ingredient_data=ingredient_data,
                sales_data=sales_data
            )

            result, error = call_gemini(prompt)
            if result:
                ai_text = result
                set_cached_ai("recommend", ai_text)
            else:
                ai_text = generate_fallback_recommend(foods, ingredients, sales)
        else:
            ai_text = generate_fallback_recommend(foods, ingredients, sales)

    return render_template(
        "ai_recommend.html",
        recommendations=recommendations,
        ingredients=ingredients,
        ai_text=ai_text
    )
@app.route("/ai-feedback")
@login_required
def ai_feedback():

    conn = get_db()

    feedbacks = conn.execute("""
        SELECT
            feedback.rating,
            feedback.comment,
            feedback.created_at,
            foods.name AS food_name
        FROM feedback
        LEFT JOIN foods
            ON feedback.food_id = foods.id
        ORDER BY feedback.id DESC
    """).fetchall()

    conn.close()

    # ==============================
    # THỐNG KÊ PHẢN HỒI
    # ==============================

    total = len(feedbacks)

    positive = 0
    neutral = 0
    negative = 0

    for feedback in feedbacks:

        rating = feedback["rating"]

        if rating >= 4:
            positive += 1

        elif rating == 3:
            neutral += 1

        else:
            negative += 1

    if total > 0:
        average_rating = sum(
            feedback["rating"] for feedback in feedbacks
        ) / total
    else:
        average_rating = 0

    # ==============================
    # TỔNG HỢP CƠ BẢN
    # ==============================

    if positive > negative:

        summary = (
            "Khách hàng nhìn chung đánh giá tích cực "
            "về các món ăn."
        )

    elif negative > positive:

        summary = (
            "Có nhiều phản hồi chưa tích cực, "
            "nên kiểm tra lại chất lượng món ăn."
        )

    else:

        summary = (
            "Phản hồi của khách hàng khá cân bằng, "
            "cần tiếp tục theo dõi."
        )

    # ==============================
    # GEMINI AI HOẶC SỬ DỤNG CACHE / FALLBACK
    # ==============================

    ai_text = get_cached_ai("feedback")

    if not ai_text:
        if client and feedbacks:
            feedback_data = []
            for feedback in feedbacks:
                feedback_data.append({
                    "food_name": feedback["food_name"],
                    "rating": feedback["rating"],
                    "comment": feedback["comment"]
                })

            prompt = FEEDBACK_SYSTEM_PROMPT + "\n\n" + FEEDBACK_USER_PROMPT.format(
                feedback_data=feedback_data
            )

            result, error = call_gemini(prompt)
            if result:
                ai_text = result
                set_cached_ai("feedback", ai_text)
            else:
                ai_text = generate_fallback_feedback(feedbacks, positive, neutral, negative)
        elif not feedbacks:
            ai_text = "Chưa có phản hồi của khách hàng để phân tích."
        else:
            ai_text = generate_fallback_feedback(feedbacks, positive, neutral, negative)

    return render_template(
        "ai_feedback.html",
        feedbacks=feedbacks,
        total=total,
        positive=positive,
        neutral=neutral,
        negative=negative,
        average_rating=average_rating,
        summary=summary,
        ai_text=ai_text
    )
@app.route("/ai-report")
@login_required
def ai_report():

    conn = get_db()

    # ==============================
    # THỐNG KÊ DOANH THU
    # ==============================

    total_revenue = conn.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM sales
    """).fetchone()[0]

    total_quantity = conn.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM sales
    """).fetchone()[0]

    total_orders = conn.execute("""
        SELECT COUNT(*)
        FROM sales
    """).fetchone()[0]

    # ==============================
    # MÓN BÁN CHẠY
    # ==============================

    best_selling = conn.execute("""
        SELECT
            foods.name AS food_name,
            SUM(sales.quantity) AS total_quantity,
            SUM(sales.total) AS revenue
        FROM sales
        JOIN foods
            ON sales.food_id = foods.id
        GROUP BY sales.food_id
        ORDER BY total_quantity DESC
        LIMIT 5
    """).fetchall()

    # ==============================
    # DOANH THU THEO NGÀY
    # ==============================

    daily_revenue = conn.execute("""
        SELECT
            DATE(sale_date) AS sale_day,
            SUM(total) AS revenue,
            SUM(quantity) AS quantity
        FROM sales
        GROUP BY DATE(sale_date)
        ORDER BY sale_day DESC
        LIMIT 7
    """).fetchall()

    conn.close()

    # ==============================
    # GEMINI AI HOẶC SỬ DỤNG CACHE / FALLBACK
    # ==============================

    ai_text = get_cached_ai("report")

    if not ai_text:
        if client:
            best_selling_data = []
            for item in best_selling:
                best_selling_data.append({
                    "food_name": item["food_name"],
                    "quantity": item["total_quantity"],
                    "revenue": item["revenue"]
                })

            daily_data = []
            for item in daily_revenue:
                daily_data.append({
                    "date": item["sale_day"],
                    "revenue": item["revenue"],
                    "quantity": item["quantity"]
                })

            prompt = REPORT_SYSTEM_PROMPT + "\n\n" + REPORT_USER_PROMPT.format(
                total_revenue=total_revenue,
                total_quantity=total_quantity,
                total_orders=total_orders,
                best_selling=best_selling_data,
                daily_revenue=daily_data
            )

            result, error = call_gemini(prompt)
            if result:
                ai_text = result
                set_cached_ai("report", ai_text)
            else:
                ai_text = generate_fallback_report(total_revenue, total_quantity, total_orders, best_selling)
        else:
            ai_text = generate_fallback_report(total_revenue, total_quantity, total_orders, best_selling)

    return render_template(
        "ai_report.html",
        total_revenue=total_revenue,
        total_quantity=total_quantity,
        total_orders=total_orders,
        best_selling=best_selling, 
        ai_text=ai_text
    )

@app.route("/ai-chat")
@login_required
def ai_chat():
    """Trang tương tác trực tiếp với Trợ lý AI Căng tin (Google Gemini AI)."""
    conn = get_db()
    food_count = conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0]
    ingredient_count = conn.execute("SELECT COUNT(*) FROM ingredients").fetchone()[0]
    revenue = conn.execute("SELECT COALESCE(SUM(total), 0) FROM sales").fetchone()[0]
    conn.close()
    return render_template(
        "ai_chat.html",
        food_count=food_count,
        ingredient_count=ingredient_count,
        revenue=revenue
    )

@app.route("/api/chat", methods=["POST"])
@login_required
def api_chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"response": "Lỗi: Vui lòng nhập tin nhắn."}), 400
    
    user_message = data["message"].strip()
    if not user_message:
         return jsonify({"response": "Lỗi: Tin nhắn không được rỗng."}), 400

    conn = get_db()
    
    food_count = conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0]
    ingredient_count = conn.execute("SELECT COUNT(*) FROM ingredients").fetchone()[0]
    revenue = conn.execute("SELECT COALESCE(SUM(total), 0) FROM sales").fetchone()[0]
    sale_count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    
    # Lấy danh sách món ăn
    foods = conn.execute("SELECT name, price, quantity FROM foods").fetchall()
    food_list_str = ", ".join([f"{f['name']} ({f['price']:,.0f}đ)" for f in foods]) if foods else "Chưa có món ăn."

    # Lấy nguyên liệu sắp hết kho
    low_stock = conn.execute("SELECT name, quantity, unit, min_quantity FROM ingredients WHERE quantity <= min_quantity").fetchall()
    low_stock_str = ", ".join([f"{i['name']} ({i['quantity']} {i['unit']}/{i['min_quantity']} {i['unit']})" for i in low_stock]) if low_stock else "Tất cả nguyên liệu đều đủ định mức an toàn."

    # Top món bán chạy
    top_sales = conn.execute("""
        SELECT foods.name, SUM(sales.quantity) as sold
        FROM sales
        JOIN foods ON sales.food_id = foods.id
        GROUP BY sales.food_id
        ORDER BY sold DESC LIMIT 5
    """).fetchall()
    top_sales_str = ", ".join([f"{s['name']} ({s['sold']} suất)" for s in top_sales]) if top_sales else "Chưa có giao dịch bán hàng."

    conn.close()

    system_instruction = CHAT_SYSTEM_PROMPT.format(
        food_count=food_count,
        ingredient_count=ingredient_count,
        revenue="{:,.0f}".format(revenue),
        sale_count=sale_count,
        food_list=food_list_str,
        low_stock=low_stock_str,
        top_sales=top_sales_str
    )
    
    result, error = call_gemini(user_message, system_instruction=system_instruction)
    if result:
        return jsonify({"response": result})
    else:
        return jsonify({"response": f"Xin lỗi, {error}"})


if __name__ == "__main__":
    init_db()
    warm_up_cache()
    app.run(debug=True, threaded=True)