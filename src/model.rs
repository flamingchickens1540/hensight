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
    pub myUpcomingMatches: Vec<NexusMatch>,
}
