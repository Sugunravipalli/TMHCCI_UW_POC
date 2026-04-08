import snowflake from "snowflake-sdk";
import fs from "fs";

snowflake.configure({ logLevel: "ERROR" });

function getOAuthToken(): string | null {
  const tokenPath = "/snowflake/session/token";
  try {
    if (fs.existsSync(tokenPath)) {
      return fs.readFileSync(tokenPath, "utf-8").trim();
    }
  } catch {
    // Not in SPCS environment
  }
  return null;
}

function getConfig(): snowflake.ConnectionOptions {
  const base: snowflake.ConnectionOptions = {
    account: process.env.SNOWFLAKE_ACCOUNT || "qsb28595.us-east-1",
    warehouse: process.env.SNOWFLAKE_WAREHOUSE || "TMHCCI_POC_WH",
    database: process.env.SNOWFLAKE_DATABASE || "TMHCCI_UW_POC",
    schema: process.env.SNOWFLAKE_SCHEMA || "CURATED",
    role: process.env.SNOWFLAKE_ROLE || "SYSADMIN",
  };

  const token = getOAuthToken();
  if (token) {
    return {
      ...base,
      host: process.env.SNOWFLAKE_HOST!,
      token,
      authenticator: "OAUTH",
    };
  }

  return {
    ...base,
    username: process.env.SNOWFLAKE_USER || "",
    authenticator: "EXTERNALBROWSER",
  };
}

// Store connection on globalThis so it survives Next.js dev-mode hot reloads.
// Without this, every module re-evaluation resets the variable and triggers
// a new EXTERNALBROWSER auth prompt.
const g = globalThis as unknown as { __sfConn?: snowflake.Connection };

function getPooledConnection(): snowflake.Connection | null {
  return g.__sfConn && g.__sfConn.isUp() ? g.__sfConn : null;
}

function setPooledConnection(conn: snowflake.Connection) {
  g.__sfConn = conn;
}

function getConnection(): Promise<snowflake.Connection> {
  return new Promise((resolve, reject) => {
    const existing = getPooledConnection();
    if (existing) {
      resolve(existing);
      return;
    }

    const conn = snowflake.createConnection(getConfig());
    conn.connect((err, c) => {
      if (err) {
        console.error("Snowflake connection error:", err.message);
        reject(err);
      } else {
        setPooledConnection(c);
        resolve(c);
      }
    });
  });
}

export async function query<T = Record<string, unknown>>(
  sql: string,
  binds: snowflake.Binds = [],
  retries = 1
): Promise<T[]> {
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const conn = await getConnection();
      return await new Promise<T[]>((resolve, reject) => {
        conn.execute({
          sqlText: sql,
          binds,
          complete: (err, _stmt, rows) => {
            if (err) {
              reject(err);
            } else {
              resolve((rows as T[]) || []);
            }
          },
        });
      });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
        if (attempt < retries && msg.includes("terminated")) {
          g.__sfConn = undefined;
          continue;
        }
      throw err;
    }
  }
  throw new Error("Query failed after retries");
}
