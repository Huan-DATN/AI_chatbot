from typing_extensions import TypedDict
from typing_extensions import Annotated
from typing import List


class Message(TypedDict):
    role: str  # "user" hoặc "bot"
    content: str


class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str
    chat_history: List[Message]
    session_id: str  # Add session_id to track the conversation


class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


examples = [
    {
        "question": "Cho tôi danh sách tất cả các sản phẩm.",
        "query": 'SELECT * FROM "Product" WHERE "isActive" = true AND "deletedAt" IS NULL;',
    },
    {
        "question": "Liệt kê các sản phẩm thuộc nhóm sản phẩm có ID là 1.",
        "query": """
        SELECT p.id, p.name, p.price, p.description, p.quantity, g.name AS group_name
        FROM "Product" p
        JOIN "GroupProduct" g ON p."groupProductId" = g.id
        WHERE p."groupProductId" = 1 AND p."isActive" = true AND p."deletedAt" IS NULL;
        """,
    },
    {
        "question": "Cho tôi danh sách các sản phẩm thuộc danh mục 'Thực phẩm'.",
        "query": """
        SELECT p.id, p.name, p.price, p.description
        FROM "Product" p
        JOIN "_CategoryToProduct" cp ON p.id = cp."B"
        JOIN "Category" c ON cp."A" = c.id
        WHERE c.name ILIKE '%thực phẩm%' AND p."isActive" = true AND p."deletedAt" IS NULL;
        """,
    },
    {
        "question": "Có sản phẩm nào trong khoảng giá từ 100 nghìn đến 300 nghìn không?",
        "query": """
        SELECT id, name, price, description
        FROM "Product"
        WHERE price BETWEEN 100000 AND 300000 AND "isActive" = true AND "deletedAt" IS NULL;
        """,
    },
    {
        "question": "Cho tôi danh sách các cửa hàng ",
        "query": """
        SELECT id, "firstName", "lastName", email, phone, address, "shopName"
        FROM "User"
        WHERE "role" = 'SELLER' AND "isActive" = true;
        """,
    },
    {
        "question": "So sánh các sản phẩm có đánh giá 5 sao.",
        "query": """
        SELECT p.id, p.name, p.price, p.description, p.star
        FROM "Product" p
        WHERE p.star = 5 AND p."isActive" = true AND p."deletedAt" IS NULL;
        """,
    },
    {
        "question": "Liệt kê các sản phẩm có xuất xứ từ Hà Nội.",
        "query": """
        SELECT p.id, p.name, p.price, p.description, c.name AS city_name
        FROM "Product" p
        JOIN "City" c ON p."cityId" = c.id
        WHERE c.name ILIKE '%hà nội%' AND p."isActive" = true AND p."deletedAt" IS NULL;
        """,
    },
    {
        "question": "Tổng giá trị của tất cả các đơn hàng là bao nhiêu?",
        "query": 'SELECT SUM(total) AS total_value FROM "OrderDetail";',
    },
    {
        "question": "Có bao nhiêu sản phẩm thuộc danh mục 'Đồ uống'?",
        "query": """
        SELECT COUNT(*) AS product_count
        FROM "Product" p
        JOIN "_CategoryToProduct" cp ON p.id = cp."B"
        JOIN "Category" c ON cp."A" = c.id
        WHERE c.name ILIKE '%đồ uống%' AND p."isActive" = true AND p."deletedAt" IS NULL;
        """,
    },
    {
        "question": "Cho tôi thông tin chi tiết của đơn hàng có ID là 1, bao gồm sản phẩm và số lượng.",
        "query": """
        SELECT od.id, od.total, od."addressLine", od.phone,
               oi."productId", p.name AS product_name, oi.quantity, oi."unitPrice",
               u."firstName", u."lastName", u.email
        FROM "OrderDetail" od
        JOIN "OrderItem" oi ON od.id = oi."orderId"
        JOIN "Product" p ON oi."productId" = p.id
        JOIN "User" u ON od."userId" = u.id
        WHERE od.id = 1;
        """,
    },
    {
        "question": "Liệt kê các sản phẩm có giá dưới 500 nghìn.",
        "query": """
        SELECT id, name, price, description
        FROM "Product"
        WHERE price < 500000 AND "isActive" = true AND "deletedAt" IS NULL;
        """,
    },
    {
        "question": "Liệt kê 5 sản phẩm có giá cao nhất.",
        "query": """
        SELECT id, name, price, description
        FROM "Product"
        WHERE "isActive" = true AND "deletedAt" IS NULL
        ORDER BY price DESC
        LIMIT 5;
        """,
    },
    {
        "question": "Liệt kê các nhóm sản phẩm hiện có",
        "query": """
        SELECT id, name
        FROM "GroupProduct"
        WHERE "isActive" = true;
        """,
    },
    {
        "question": "So sánh số lượng sản phẩm của các nhóm sản phẩm.",
        "query": """
        SELECT g.id, g.name, COUNT(p.id) AS product_count
        FROM "GroupProduct" g
        LEFT JOIN "Product" p ON g.id = p."groupProductId" AND p."isActive" = true AND p."deletedAt" IS NULL
        WHERE g."isActive" = true
        GROUP BY g.id, g.name
        ORDER BY product_count DESC;
        """,
    },
    {
        "question": "Liệt kê các đơn hàng có trạng thái là đã giao hàng.",
        "query": """
        SELECT od.id, od.total, od."userId", od."createdAt", u."firstName", u."lastName"
        FROM "OrderDetail" od
        JOIN "OrderStatus" os ON od.id = os."orderId"
        JOIN "Status" s ON os."statusId" = s.id
        JOIN "User" u ON od."userId" = u.id
        WHERE s."type" = 'DELIVERED' AND os."isActive" = true;
        """,
    },
    {
        "question": "Đếm số lượng đơn hàng theo từng trạng thái.",
        "query": """
        SELECT s."type", s.name, COUNT(os."orderId") AS order_count
        FROM "Status" s
        LEFT JOIN "OrderStatus" os ON s.id = os."statusId" AND os."isActive" = true
        GROUP BY s."type", s.name
        ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Liệt kê tất cả đánh giá cho sản phẩm có ID là 1.",
        "query": """
        SELECT r.id, r."userId", u."firstName", u."lastName", r.rating, r."comment", r."createdAt"
        FROM "Rating" r
        JOIN "User" u ON r."userId" = u.id
        WHERE r."productId" = 1
        ORDER BY r."createdAt" DESC;
        """,
    },
    {
        "question": "Đếm số lượng sản phẩm theo từng thành phố.",
        "query": """
        SELECT c.id, c.name, COUNT(p.id) AS product_count
        FROM "City" c
        LEFT JOIN "Product" p ON c.id = p."cityId" AND p."isActive" = true AND p."deletedAt" IS NULL
        WHERE c."isActive" = true
        GROUP BY c.id, c.name
        ORDER BY product_count DESC;
        """,
    },
]
