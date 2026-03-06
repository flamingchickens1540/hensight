import { Database } from 'bun:sqlite';
import type { statObj } from './types';

const db = new Database('stats.db');

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

export function addData(key: string, data: statObj) {
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

export function getData(key: string) {
	return db.prepare('SELECT * FROM stats WHERE key = ?').get(key);
}

export default db;
