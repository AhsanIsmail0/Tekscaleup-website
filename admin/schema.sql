CREATE TABLE IF NOT EXISTS content (
 id TEXT PRIMARY KEY, type TEXT NOT NULL, slug TEXT NOT NULL, payload TEXT NOT NULL,
 status TEXT NOT NULL CHECK(status IN ('draft','published','archived')),
 version INTEGER NOT NULL DEFAULT 1, updated_at TEXT NOT NULL,
 UNIQUE(type,slug)
);
CREATE INDEX IF NOT EXISTS content_public ON content(type,status);
CREATE TABLE IF NOT EXISTS admin_login_limits (
 bucket TEXT PRIMARY KEY, attempts INTEGER NOT NULL, expires INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS admin_login_expiry ON admin_login_limits(expires);
