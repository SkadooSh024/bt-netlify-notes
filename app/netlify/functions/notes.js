const { Pool } = require("pg");

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.DATABASE_URL?.includes("render.com")
    ? { rejectUnauthorized: false }
    : false,
});

async function init() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS notes (
      id SERIAL PRIMARY KEY,
      content TEXT NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
  `);
}
let inited = false;

exports.handler = async (event) => {
  try {
    if (!inited) {
      await init();
      inited = true;
    }

    if (event.httpMethod === "GET") {
      const { rows } = await pool.query(
        "SELECT * FROM notes ORDER BY id DESC LIMIT 50"
      );
      return {
        statusCode: 200,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(rows),
      };
    }

    if (event.httpMethod === "POST") {
      const body = JSON.parse(event.body || "{}");
      const content = String(body.content || "").trim();
      if (!content) {
        return { statusCode: 400, body: "content is required" };
      }
      const { rows } = await pool.query(
        "INSERT INTO notes(content) VALUES($1) RETURNING *",
        [content]
      );
      return {
        statusCode: 201,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(rows[0]),
      };
    }

    return { statusCode: 405, body: "Method Not Allowed" };
  } catch (e) {
    return { statusCode: 500, body: String(e?.message || e) };
  }
};
