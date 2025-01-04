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
                channel_id INTEGER,
                role_id INTEGER
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
            CREATE TABLE IF NOT EXISTS auto_scrim (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                best_of TEXT NOT NULL,
                game_mode TEXT NOT NULL,
                elo TEXT NOT NULL,
                FOREIGN KEY (team_id) REFERENCES teams (id) ON DELETE CASCADE
            )
        ''')

        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS manual_scrim (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                best_of TEXT NOT NULL,
                game_mode TEXT NOT NULL,
                elo TEXT NOT NULL,
                FOREIGN KEY (team_id) REFERENCES teams (id) ON DELETE CASCADE
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

async def create_auto_scrim(team_id: str, date: str, time: str, best_of: str, game_mode: str, elo: str):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        await cursor.execute('''
            INSERT INTO auto_scrim (team_id, date, time, best_of, game_mode, elo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (team_id, date, time, best_of, game_mode, elo))
            
        await db.commit()
    await db.close()

async def create_manual_scrim(team_id: str, date: str, time: str, best_of: str, game_mode: str, elo: str):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        await cursor.execute('''
            INSERT INTO manual_scrim (team_id, date, time, best_of, game_mode, elo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (team_id, date, time, best_of, game_mode, elo))
            
        await db.commit()
    await db.close()

async def edit_team(team_id: int, team_name: str, description: str, elo: int):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        await cursor.execute('''
            UPDATE teams SET name = ?, description = ?, elo = ? WHERE id = ?''', (team_name, description, elo, team_id))          
        await db.commit()
    await db.close()

async def add_channel_id(team_id: int, channel_id: int):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        await cursor.execute('''
            UPDATE teams SET channel_id = ? WHERE id = ?''', (channel_id, team_id))          
        await db.commit()
    await db.close()

async def add_role_id(team_id: int, role_id: int):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        await cursor.execute('''
            UPDATE teams SET role_id = ? WHERE id = ?''', (role_id, team_id))          
        await db.commit()
    await db.close()

async def edit_auto_scrim(team_id: int, date: str, time: str, best_of: str, game_mode: str, elo: str):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        await cursor.execute('''
            UPDATE auto_scrim SET date = ?, time = ?, best_of = ?, game_mode = ?, elo = ? WHERE team_id = ?''', (date, time, best_of, game_mode, elo, team_id))          
        await db.commit()
    await db.close()

async def get_auto_scrim(team_id):
    db = await get_db_connection()
    try:
        cursor = await db.execute("""
            SELECT team_id, date, time, best_of, game_mode, elo
            FROM auto_scrim
            WHERE team_id = ?""", (team_id,))
        
        auto_scrim = await cursor.fetchone()

        if auto_scrim:
            return {
                "team_id": auto_scrim[0],
                "date": auto_scrim[1],
                "time": auto_scrim[2],
                "best_of": auto_scrim[3],
                "game_mode": auto_scrim[4],
                "elo": auto_scrim[5]
            }
        return None

    except Exception as e:
        print(f"An error occurred while retrieving the auto scrim: {e}")
        return None

    finally:
        await db.close()

async def get_manual_scrim(team_id):
    db = await get_db_connection()
    try:
        cursor = await db.execute("""
            SELECT team_id, date, time, best_of, game_mode, elo
            FROM manual_scrim
            WHERE team_id = ?""", (team_id,))
        
        manual_scrim = await cursor.fetchone()

        if manual_scrim:
            return {
                "team_id": manual_scrim[0],
                "date": manual_scrim[1],
                "time": manual_scrim[2],
                "best_of": manual_scrim[3],
                "game_mode": manual_scrim[4],
                "elo": manual_scrim[5]
            }
        return None

    except Exception as e:
        print(f"An error occurred while retrieving the auto scrim: {e}")
        return None

    finally:
        await db.close()


async def get_team(user_id):
    db = await get_db_connection()
    try:
        cursor = await db.execute("""
            SELECT teams.id, teams.name, teams.description, teams.elo, teams.captain_id, teams.channel_id
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
        return None

    except Exception as e:
        print(f"An error occurred while retrieving the team: {e}")
        return None

    finally:
        await db.close()


async def get_team_by_team_id(team_id):
    db = await get_db_connection()
    try:
        async with db.execute("""
            SELECT id, name, description, elo, captain_id, channel_id
            FROM teams
            WHERE id = ?
        """, (team_id,)) as cursor:
            
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
            return None

    except Exception as e:
        print(f"An error occurred while retrieving the team (ID: {team_id}): {e}")
        return None

    finally:
        await db.close()
