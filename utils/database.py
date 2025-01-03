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
                elo TEXT DEFAULT 0,
                captain_id INTEGER NOT NULL,
                channel_id INTEGER
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

async def create_team(user_id: int, team_name: str, description: str, elo: int):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        await cursor.execute('''
            INSERT INTO teams (name, description, elo, captain_id)
            VALUES (?, ?, ?, ?)
        ''', (team_name, description, elo, user_id))

        team_id = cursor.lastrowid

        await cursor.execute('''
            INSERT INTO team_members (team_id, user_id, is_captain)
            VALUES (?, ?, ?)
        ''', (team_id, user_id, 1))
            
        await db.commit()
    await db.close()

async def get_team(user_id):
    db = await get_db_connection()
    cursor = await db.execute("""
        SELECT * 
        FROM teams 
        INNER JOIN team_members ON teams.id = team_members.team_id 
        WHERE team_members.user_id = ?""", (user_id,))
        
    team = await cursor.fetchone()
    if team:
        return {
            "id": team[0],
            "name": team[1],
            "description": team[2],
            "elo": team[3],
            "captain_id": team[4],
            "channel_id": team[5]
        }
    return None  # Explicitly return None if no team is found

