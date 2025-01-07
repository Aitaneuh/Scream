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
                scrim_channel TEXT
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
                announcement_message_id TEXT,
                pick_message_id,
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
                announcement_message_id TEXT,
                pick_message_id,
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

async def add_auto_message_id(team_id: int, announcement_message_id: int, pick_message_id: int):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        await cursor.execute('''
            UPDATE auto_scrim SET announcement_message_id = ?, pick_message_id = ?  WHERE id = ?''', (announcement_message_id, pick_message_id, team_id))          
        await db.commit()
    await db.close()

async def add_manual_message_id(team_id: int, announcement_message_id: int, pick_message_id: int):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        await cursor.execute('''
            UPDATE manual_scrim SET announcement_message_id = ?, pick_message_id = ?  WHERE id = ?''', (announcement_message_id, pick_message_id, team_id))          
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
            SELECT team_id, date, time, best_of, game_mode, elo, announcement_message_id, pick_message_id
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
                "elo": auto_scrim[5],
                "announcement_message_id": auto_scrim[6],
                "pick_message_id": auto_scrim[7]
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
            SELECT team_id, date, time, best_of, game_mode, elo, announcement_message_id, pick_message_id
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
                "elo": manual_scrim[5],
                "announcement_message_id": manual_scrim[6],
                "pick_message_id": manual_scrim[7]
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
            SELECT teams.id, teams.name, teams.description, teams.elo, teams.captain_id, teams.channel_id, role_id
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
                "channel_id": team[5],
                "role_id": team[6]
            }
        return None

    except Exception as e:
        print(f"An error occurred while retrieving the team: {e}")
        return None

    finally:
        await db.close()

async def get_team_from_message_id(message_id):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        query = """
        SELECT teams.*
        FROM teams
        INNER JOIN (
            SELECT team_id
            FROM auto_scrim
            WHERE pick_message_id = ?
            UNION ALL
            SELECT team_id
            FROM manual_scrim
            WHERE pick_message_id = ?
        ) AS scrims ON teams.id = scrims.team_id;
        """
        cursor = await db.execute(query, (message_id, message_id))
        team = await cursor.fetchone()
        await cursor.close()
        if team:
            return {
                "id": team[0],
                "name": team[1],
                "description": team[2],
                "elo": team[3],
                "captain_id": team[4],
                "channel_id": team[5],
                "role_id": team[6]
            }
        return None


async def get_scrim_from_message_id(pick_message_id):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        query = """
        SELECT id, team_id, date, time, best_of, game_mode, elo, pick_message_id
        FROM auto_scrim
        WHERE pick_message_id = ?
        UNION
        SELECT id, team_id, date, time, best_of, game_mode, elo, pick_message_id
        FROM manual_scrim
        WHERE pick_message_id = ?;
        """
        cursor = await db.execute(query, (pick_message_id, pick_message_id))
        result = await cursor.fetchone()
        await cursor.close()

        if result:
            scrim_info = {
                "id": result[0],
                "team_id": result[1],
                "date": result[2],
                "time": result[3],
                "best_of": result[4],
                "game_mode": result[5],
                "elo": result[6],
                "pick_message_id": result[7],
            }
            return scrim_info
        return None


async def get_team_by_team_id(team_id):
    db = await get_db_connection()
    try:
        async with db.execute("""
            SELECT id, name, description, elo, captain_id, channel_id, role_id
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
                    "channel_id": team[5],
                    "role_id": team[6]
                }
            return None

    except Exception as e:
        print(f"An error occurred while retrieving the team (ID: {team_id}): {e}")
        return None

    finally:
        await db.close()

async def get_team_members(team_id):
    db = await get_db_connection()
    async with db.cursor() as cursor:
        query = "SELECT user_id FROM team_members WHERE team_id = ?"
        cursor = await db.execute(query, (team_id,))
        members = await cursor.fetchall()
        await cursor.close()
        return [member[0] for member in members]
