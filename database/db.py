import sqlite3

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

DATABASE = "database/stockvision.db"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # ======================================================
    # USERS
    # ======================================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )

    """)

    # ======================================================
    # PREDICTIONS
    # ======================================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS predictions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        stock_symbol TEXT NOT NULL,

        current_price REAL,

        predicted_price REAL,

        change_percent REAL,

        signal TEXT,

        prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)

            REFERENCES users(id)

    )

    """)

    # ==========================================
    # DATABASE MIGRATION
    # Add profile_image column if missing
    # ==========================================

    cursor.execute("PRAGMA table_info(users)")

    columns = [

        column[1]

        for column in cursor.fetchall()

    ]

    if "profile_image" not in columns:

        cursor.execute("""

            ALTER TABLE users

            ADD COLUMN profile_image TEXT

            DEFAULT 'default.png'

        """)

    # ======================================================
    # WATCHLIST
    # ======================================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS watchlist(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        symbol TEXT NOT NULL,

        added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE(user_id, symbol),

        FOREIGN KEY(user_id)

            REFERENCES users(id)

    )

    """)

    # ======================================================
    # PORTFOLIO
    # ======================================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS portfolio(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        stock_symbol TEXT NOT NULL,

        quantity INTEGER NOT NULL,

        buy_price REAL NOT NULL,

        purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
            REFERENCES users(id)

    )

    """)

    conn.commit()

    conn.close()


# ==========================================================
# USER REGISTRATION
# ==========================================================

def create_user(name, email, password):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""

        INSERT INTO users(

            name,

            email,

            password

        )

        VALUES(?,?,?)

        """,

        (

            name,

            email,

            generate_password_hash(password)

        )

        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ==========================================================
# USER LOGIN
# ==========================================================

def login_user(email, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM users

    WHERE email=?

    """,

    (email,)

    )

    user = cursor.fetchone()

    conn.close()

    if user is None:

        return None

    if check_password_hash(

        user["password"],

        password

    ):

        return user

    return None


# ==========================================================
# SAVE PREDICTION
# ==========================================================

def save_prediction(

    user_id,

    symbol,

    current,

    predicted,

    change,

    signal

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO predictions(

        user_id,

        stock_symbol,

        current_price,

        predicted_price,

        change_percent,

        signal

    )

    VALUES(?,?,?,?,?,?)

    """,

    (

        user_id,

        symbol,

        current,

        predicted,

        change,

        signal

    )

    )

    conn.commit()

    conn.close()


# ==========================================================
# FETCH HISTORY
# ==========================================================

def fetch_predictions(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM predictions

    WHERE user_id=?

    ORDER BY prediction_time DESC

    """,

    (user_id,)

    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# EXPORT HISTORY
# ==========================================================

def fetch_all_predictions(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM predictions

    WHERE user_id=?

    ORDER BY prediction_time DESC

    """,

    (user_id,)

    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# CLEAR HISTORY
# ==========================================================

def clear_history(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE

    FROM predictions

    WHERE user_id=?

    """,

    (user_id,)

    )

    conn.commit()

    conn.close()


# ==========================================================
# WATCHLIST
# ==========================================================

def add_to_watchlist(user_id, symbol):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR IGNORE

    INTO watchlist(

        user_id,

        symbol

    )

    VALUES(?,?)

    """,

    (

        user_id,

        symbol.upper()

    )

    )

    conn.commit()

    conn.close()


def get_watchlist(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM watchlist

    WHERE user_id=?

    ORDER BY added_on DESC

    """,

    (user_id,)

    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_from_watchlist(user_id, watchlist_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE

    FROM watchlist

    WHERE id=?

    AND user_id=?

    """,

    (

        watchlist_id,

        user_id

    )

    )

    conn.commit()

    conn.close()

# ==========================================
# USER PROFILE HELPERS
# ==========================================

def get_user_by_id(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM users

        WHERE id=?

    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return user


def get_prediction_count(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM predictions

        WHERE user_id=?

    """, (user_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_watchlist_count(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM watchlist

        WHERE user_id=?

    """, (user_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count

# ==========================================
# UPDATE USER PROFILE
# ==========================================

def update_user(user_id, name, email):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""

            UPDATE users

            SET

                name=?,

                email=?

            WHERE id=?

        """,

        (

            name,

            email,

            user_id

        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()

# ==========================================
# CHANGE PASSWORD
# ==========================================

def update_password(user_id, new_password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE users

        SET password=?

        WHERE id=?

    """,

    (

        generate_password_hash(new_password),

        user_id

    ))

    conn.commit()

    conn.close()

# ==========================================
# PROFILE IMAGE
# ==========================================

def update_profile_image(user_id, filename):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE users

        SET profile_image=?

        WHERE id=?

    """,

    (

        filename,

        user_id

    ))

    conn.commit()

    conn.close()

# ==========================================
# PORTFOLIO
# ==========================================

def add_portfolio_stock(user_id, symbol, quantity, buy_price):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO portfolio(

            user_id,

            stock_symbol,

            quantity,

            buy_price

        )

        VALUES(?,?,?,?)

    """,

    (

        user_id,

        symbol.upper(),

        quantity,

        buy_price

    ))

    conn.commit()

    conn.close()


def get_portfolio(user_id):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM portfolio

        WHERE user_id=?

        ORDER BY purchase_date DESC

    """,

    (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_portfolio_stock(user_id, stock_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM portfolio

        WHERE id=?

        AND user_id=?

    """,

    (

        stock_id,

        user_id

    ))

    conn.commit()

    conn.close()