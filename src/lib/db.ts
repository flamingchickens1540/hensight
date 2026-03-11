import { eventKey } from './config';
import type { statObj } from './types';

let db: any = null;
let clickDB: any = null;

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

async function getClickDB() {
	if (!clickDB) {
		const { Database } = await import('bun:sqlite');

		clickDB = new Database('clicks.db');

		clickDB.run(`
      CREATE TABLE IF NOT EXISTS stats (
        key TEXT PRIMARY KEY,
        clicks INT
      )
    `);
	}

	return clickDB;
}

export async function setClicks(clicks: number) {
	const db = await getClickDB();

	db.prepare(
		`INSERT INTO stats
        VALUES (?, ?)
        ON CONFLICT(key)
        DO UPDATE SET
            clicks = excluded.clicks;`
	).run(eventKey, clicks);

	let globalCount = 0;
	const res = db.prepare(`Select * FROM stats`).all();
	for (const item of res) {
		if (item.key == 'GLOBAL') continue;
		globalCount += item.clicks;
	}

	db.prepare(
		`INSERT INTO stats
        VALUES ('GLOBAL', ?)
        ON CONFLICT(key)
        DO UPDATE SET
            clicks = excluded.clicks;`
	).run(globalCount);
}

export async function getClicks(key: string) {
	let db = await getClickDB();
	const res = db.prepare('SELECT clicks FROM stats WHERE key = ?').get(key);
	if (res) return res.clicks;
	else return 0;
}

export { getDB };
