import psycopg2

try:
    # 先连接到默认的 postgres 数据库
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="748156",
        dbname="postgres"  # 使用默认数据库
    )

    # 立即关闭自动提交，用于查询
    conn.autocommit = False

    cur = conn.cursor()
    cur.execute("SELECT version();")
    print("PostgreSQL 版本：", cur.fetchone())

    # 检查数据库是否存在
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'ai_character_chat';")
    if not cur.fetchone():
        print("数据库 ai_character_chat 不存在，正在创建...")

        # 关闭当前游标和连接
        cur.close()
        conn.close()

        # 重新连接并开启自动提交模式来创建数据库
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=5432,
            user="postgres",
            password="748156",
            dbname="postgres"
        )
        conn.autocommit = True  # 必须在连接后立即设置

        cur = conn.cursor()
        cur.execute("CREATE DATABASE ai_character_chat;")
        print("数据库创建成功！")
    else:
        print("数据库 ai_character_chat 已存在")

    cur.close()
    conn.close()
    print("操作完成！")

except Exception as e:
    print(f"错误：{e}")