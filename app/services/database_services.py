from os import getenv
import psycopg2
from psycopg2 import sql

configs = {
    "host": getenv("DB_HOST"),
    "database": getenv("DB_NAME"),
    "user": getenv("DB_USER"),
    "password": getenv("DB_PASSWORD")
}

class DatabaseConnector:
    @classmethod
    def get_conn_cur(cls):
        cls.conn = psycopg2.connect(**configs)
        cls.cur = cls.conn.cursor()

        cls.cur.execute("""
            CREATE TABLE IF NOT EXISTS animes(
                id              BIGSERIAL PRIMARY KEY,
                anime           VARCHAR(100) NOT NULL UNIQUE,
                released_date   DATE NOT NULL,
                seasons         INTEGER NOT NULL
            );
        """)

        cls.conn.commit()
    
    @classmethod
    def commit_and_close(cls):
        cls.conn.commit()
        cls.cur.close()
        cls.conn.close()
    
    @classmethod
    def serializer(cls, data: tuple, keys: list[str]):
        return dict(zip(keys, data))
    
    @classmethod
    def to_add_anime(cls, payload: dict):
        cls.get_conn_cur()
        
        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]
        
        query = sql.SQL(
            """
            INSERT INTO
                animes ({columns})
            VALUES
                ({values})
            RETURNING *
            """
        ).format(columns = sql.SQL(",").join(columns), values = sql.SQL(",").join(values))

        cls.cur.execute(query)
        inserted_anime = cls.cur.fetchone()

        cls.commit_and_close()

        return inserted_anime

    @classmethod
    def get_all_animes(cls):
        cls.get_conn_cur()

        query = sql.SQL(
            """
            SELECT 
                id, anime, TO_CHAR(released_date, 'DD/MM/YYYY'), seasons
            FROM animes;
            """
        )

        cls.cur.execute(query)

        animes_list = cls.cur.fetchall()

        cls.commit_and_close()

        return animes_list

    @classmethod
    def get_columns_names(cls):
        cls.get_conn_cur()

        query = sql.SQL(
            """
            SELECT
                column_name
            FROM
                information_schema.COLUMNS
            WHERE table_name = 'animes'
            ORDER BY ordinal_position;
            """
        )

        cls.cur.execute(query)
        
        columns_name = cls.cur.fetchall()

        cls.commit_and_close()

        return [row[0] for row in columns_name]

    @classmethod
    def get_specific_anime(cls,id: int):
        cls.get_conn_cur()

        query = sql.SQL(
            """
            SELECT
                id, anime, TO_CHAR(released_date, 'DD/MM/YYYY'), seasons
            FROM
                animes
            WHERE
                id = %s
            """
        )

        cls.cur.execute(query, (id,))
        specific_anime = cls.cur.fetchone()
        cls.commit_and_close()

        return specific_anime
    
    @classmethod
    def updated_anime(cls, id: int, payload: dict):
        cls.get_conn_cur()

        columns = [sql.Identifier(key) for key in payload.keys()]

        if 'anime' in payload.keys():
            payload['anime'] = payload['anime'].title()

        values = [sql.Literal(value) for value in payload.values()]

        query = sql.SQL(
            """
            UPDATE
                animes
            SET
                ({columns}) = ROW({values})
            WHERE
                id={id}
            RETURNING
                id, anime, TO_CHAR(released_date, 'DD/MM/YYYY'), seasons
            """
        ).format(
            id = sql.Literal(id),
            columns = sql.SQL(',').join(columns),
            values = sql.SQL(',').join(values)
        )

        cls.cur.execute(query, [id])
        att_anime = cls.cur.fetchone()
        cls.commit_and_close()

        return att_anime
    
    @classmethod
    def delete_anime(cls, id: int):
        cls.get_conn_cur()

        query = sql.SQL(
            """
            DELETE FROM
                animes
            WHERE
                id = {id}
            RETURNING *
            """
        ).format(id = sql.Literal(id))

        cls.cur.execute(query, (id,))
        deleted_anime = cls.cur.fetchone()
        cls.commit_and_close()

        if deleted_anime == None:
            raise TypeError

        return deleted_anime