use serde::{Deserialize, Serialize};
use serde_json;

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct SlideData {}

#[allow(non_snake_case)]
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct NexusMatch {
    pub label: String,
    pub status: String,
    pub redTeams: Option<Vec<String>>,
    pub blueTeams: Option<Vec<String>>,
    pub times: serde_json::Map<String, serde_json::Value>,
    pub breakAfter: Option<String>,
    pub replayOf: Option<String>,
}

#[allow(non_snake_case)]
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct NexusAnnouncement {
    pub id: String,
    pub announcement: String,
    pub postedTime: i64,
}

#[allow(non_snake_case)]
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct NexusPartsRequest {
    pub id: String,
    pub parts: String,
    pub requestedByTeam: String,
    pub postedTime: i64,
}

#[allow(non_snake_case)]
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct NexusEventStatus {
    pub eventKey: String,
    pub dataAsOfTime: i64,
    pub nowQueuing: Option<String>,
    pub matches: Vec<NexusMatch>,
    pub announcements: Vec<NexusAnnouncement>,
    pub partsRequests: Vec<NexusPartsRequest>,
}

#[allow(non_snake_case)]
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct PulseData {
    pub matchInfo: String,
    pub announcements: Vec<String>,
    pub partsRequests: Vec<String>,
    pub nowQueuing: Option<String>,
    pub myUpcommingMatches: Vec<NexusMatch>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsReturn {
    pub epa_total: f64,
    pub wins: u32,
    pub losses: u32,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsTeamYear {
    pub team: String,
    pub year: u32,
    pub name: String,
    pub country: String,
    pub state: String,
    pub district: String,
    pub offseason: bool,
    pub epa: StatboticsEpa,
    pub record: StatboticsRecord,
    pub district_points: u32,
    pub district_rank: u32,
    pub competing: StatboticsCompeting,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsCompeting {
    pub this_week: bool,
    pub next_event_key: Option<String>,
    pub next_event_name: Option<String>,
    pub next_event_week: Option<String>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsRecord {
    pub season: StatboticsRecordDetails,
    pub full: StatboticsRecordDetails,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsRecordDetails {
    pub wins: u32,
    pub losses: u32,
    pub ties: u32,
    pub count: u32,
    pub winrate: f64,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsEpa {
    pub total_points: StatboticsPoints,
    pub unitless: f32,
    pub conf: Vec<f64>,
    pub breakdown: StatboticsEpaBreakdown,
    pub stats: StatboticsEpaStats,
    pub ranks: StatboticsRanks,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsRanks {
    pub total: StatboticsRankDetails,
    pub country: StatboticsRankDetails,
    pub state: StatboticsRankDetails,
    pub district: StatboticsRankDetails,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsRankDetails {
    pub rank: u32,
    pub percentile: f64,
    pub team_count: u32,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsEpaStats {
    pub start: f64,
    pub pre_champs: f64,
    pub max: f64,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsPoints {
    pub mean: f64,
    pub sd: f64,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct StatboticsEpaBreakdown {
    pub total_points: StatboticsPoints,
    pub auto_points: StatboticsPoints,
    pub teleop_points: StatboticsPoints,
    pub endgame_points: StatboticsPoints,
    pub melody_rp: StatboticsPoints,
    pub harmony_rp: StatboticsPoints,
    pub tiebreaker_points: StatboticsPoints,
    pub auto_leave_points: StatboticsPoints,
    pub auto_notes: StatboticsPoints,
    pub auto_note_points: StatboticsPoints,
    pub teleop_notes: StatboticsPoints,
    pub teleop_note_points: StatboticsPoints,
    pub amp_notes: StatboticsPoints,
    pub amp_points: StatboticsPoints,
    pub speaker_notes: StatboticsPoints,
    pub speaker_points: StatboticsPoints,
    pub amplified_notes: StatboticsPoints,
    pub total_notes: StatboticsPoints,
    pub total_note_points: StatboticsPoints,
    pub endgame_park_points: StatboticsPoints,
    pub endgame_on_stage_points: StatboticsPoints,
    pub endgame_harmony_points: StatboticsPoints,
    pub endgame_trap_points: StatboticsPoints,
    pub endgame_spotlight_points: StatboticsPoints,
    pub rp_1: StatboticsPoints,
    pub rp_2: StatboticsPoints,
}
