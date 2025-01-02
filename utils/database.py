import aiosqlite
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../data/main.db')

async def get_db_connection():
    db = await aiosqlite.connect(DATABASE_PATH)
    return db

async def create_tables():
    db = await get_db_connection()
    async with db.cursor() as cursor:
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                elo INTEGER DEFAULT 0,
                captain_id INTEGER NOT NULL
            )
        ''')

        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                is_captain BOOLEAN DEFAULT 0,
                FOREIGN KEY (team_id) REFERENCES teams (id) ON DELETE CASCADE
            )
        ''')

        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS scrims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team1_id INTEGER NOT NULL,
                team2_id INTEGER,
                requested_by TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                accepted_at TIMESTAMP,
                scrim_channel TEXT,
                FOREIGN KEY (team1_id) REFERENCES teams (id) ON DELETE CASCADE,
                FOREIGN KEY (team2_id) REFERENCES teams (id) ON DELETE CASCADE
            )
        ''')

        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_stats (
                team_id INTEGER PRIMARY KEY,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                FOREIGN KEY (team_id) REFERENCES teams (id) ON DELETE CASCADE
            )
        ''')

        await db.commit()

    await db.close()
