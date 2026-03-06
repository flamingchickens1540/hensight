import type { statObj } from './types';

let db: any = null;

async function getDB() {
	if (!db) {
		const { Database } = await import('bun:sqlite');

		db = new Database('stats.db');

		db.run('PRAGMA journal_mode = WAL;');

		db.run(`
      CREATE TABLE IF NOT EXISTS stats (
        key TEXT PRIMARY KEY,
        pointsScored INTEGER,
        averagePointsPerMatch INTEGER,
        rpEarned INTEGER,
        penaltyPoints INTEGER,
        autoPoints INTEGER,
        matchesPlayed INTEGER,
        feetClimbed INTEGER,
        redWinCount INTEGER,
        blueWinCount INTEGER
      )
    `);
	}

	return db;
}

export async function addData(key: string, data: statObj) {
	const db = await getDB();

	db.prepare(
		`INSERT INTO stats
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(key)
        DO UPDATE SET
            pointsScored = excluded.pointsScored,
            averagePointsPerMatch = excluded.averagePointsPerMatch,
            rpEarned = excluded.rpEarned,
            penaltyPoints = excluded.penaltyPoints,
            autoPoints = excluded.autoPoints,
            matchesPlayed = excluded.matchesPlayed,
            feetClimbed = excluded.feetClimbed,
            redWinCount = excluded.redWinCount,
            blueWinCount = excluded.blueWinCount;`
	).run(
		key,
		data.pointsScored,
		data.averagePointsPerMatch,
		data.rpEarned,
		data.penaltyPoints,
		data.autoPoints,
		data.matchesPlayed,
		data.feetClimbed,
		data.redWinCount,
		data.blueWinCount
	);
}

export async function getData(key: string) {
	const db = await getDB();
	return db.prepare('SELECT * FROM stats WHERE key = ?').get(key);
}

export { getDB };
