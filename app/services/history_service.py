from urllib.parse import urlparse, parse_qs
from app.config import get_config

config = get_config()


def get_history_str(history) -> str:
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])


def convert_sqlalchemy_to_psycopg2(sqlalchemy_uri: str) -> str:
    """
    Convert SQLAlchemy PostgreSQL URI to psycopg2 connection string.
    Example: 'postgresql+psycopg2://user:pass@localhost:5444/dbname' ->
             'dbname=dbname user=user password=pass host=localhost port=5444'
    """
    parsed = urlparse(sqlalchemy_uri)
    dbname = parsed.path.lstrip("/")
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port
    return f"dbname={dbname} user={user} password={password} host={host} port={port}"


from langchain_community.chat_message_histories import PostgresChatMessageHistory


def get_chat_history(session_id: str) -> PostgresChatMessageHistory:
    sqlalchemy_uri = config.DB_URL
    psycopg2_conn_str = convert_sqlalchemy_to_psycopg2(sqlalchemy_uri)
    return PostgresChatMessageHistory(
        connection_string=psycopg2_conn_str,
        session_id=session_id,
        table_name="ChatMessageHistory",
    )
