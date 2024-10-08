use chrono::{Datelike, Local, TimeZone};
use model::PulseData;
use rand::{seq::SliceRandom, thread_rng};
use serde_json;
use std::ops::Deref;
use tba_openapi_rust::{
    apis::{configuration::Configuration, event_api},
    models::event_ranking_rankings_inner::EventRankingRankingsInner,
};

mod model;

pub use model::{NexusEventStatus, NexusMatch, SlideData, StatboticsReturn, StatboticsTeamYear};

pub fn get_slide<'a>(
    slides: &'a Vec<impl Fn(&SlideData) -> Option<&'a str>>,
    slide_data: SlideData,
) -> String {
    match slides.choose(&mut thread_rng()).unwrap()(&slide_data) {
        Some(slide) => String::from(slide),
        None => get_slide(slides, slide_data),
    }
}

pub async fn get_statbotics_data(client: reqwest::Client, team_number: &u32) -> StatboticsReturn {
    let data = client
        .get(format!(
            "https://api.statbotics.io/v3/team_year/{}/{}",
            team_number,
            chrono::Utc::now().year()
        ))
        .header("accept", "application/json")
        .send()
        .await
        .unwrap()
        .json::<StatboticsTeamYear>()
        .await
        .unwrap();

    return StatboticsReturn {
        epa_total: data.epa.total_points.mean,
        wins: data.record.season.wins,
        losses: data.record.season.losses,
    };
}

pub async fn get_event_predictions(
    config: &Configuration,
    event_key: &str,
) -> serde_json::value::Value {
    event_api::get_event_predictions(&config, event_key, None)
        .await
        .unwrap()
}

pub async fn get_event_rankings(
    config: &Configuration,
    event_key: &str,
    truncate_amount: usize,
) -> Vec<EventRankingRankingsInner> {
    let mut rankings = event_api::get_event_rankings(config, event_key, None)
        .await
        .unwrap()
        .rankings;
    rankings.truncate(truncate_amount);
    rankings
}

#[allow(non_snake_case)]
pub async fn get_pulse_data(
    client: reqwest::Client,
    nexus_api_key: &str,
    team_number: &u32,
    event_key: &str,
) -> PulseData {
    let data = client
        .get(format!("https://frc.nexus/api/v1/event/{}", event_key))
        .header("Nexus-Api-Key", nexus_api_key)
        .send()
        .await
        .unwrap()
        .json::<NexusEventStatus>()
        .await
        .unwrap();

    let myUpcommingMatches: Vec<NexusMatch> = data
        .matches
        .into_iter()
        .filter(|m| {
            (m.redTeams
                .as_ref()
                .unwrap()
                .contains(&team_number.to_string())
                || m.blueTeams
                    .as_ref()
                    .unwrap()
                    .contains(&team_number.to_string()))
                && m.status != "On field"
        })
        .collect();

    let matchInfo: String;
    match myUpcommingMatches.len() {
        1.. => {
            let nexus_match = &myUpcommingMatches[0];

            let queue_time = (Local
                .timestamp_opt(
                    nexus_match
                        .times
                        .get("estimatedQueueTime")
                        .unwrap()
                        .as_number()
                        .unwrap()
                        .as_i64()
                        .unwrap()
                        / 1000,
                    0,
                )
                .unwrap()
                - Local::now())
            .num_seconds();

            let formated_time: String;
            match &queue_time {
                3600.. => {
                    formated_time = format!("and will queue in {} hour(s)", queue_time / 3600)
                }
                60..3600 => {
                    formated_time = format!("and will be queue in {} minute(s)", queue_time / 60)
                }
                30..60 => formated_time = format!("and will queue in {} seccound(s)", queue_time),
                ..30 => formated_time = "is queueing NOW".to_string(),
            }
            println!("{:?}", queue_time);
            matchInfo = format!(
                "Team {}'s next match is {} {}",
                team_number, nexus_match.label, formated_time
            );
        }
        0 => {
            matchInfo = format!(
                "Team {} doesn't have any future matches scheduled yet",
                team_number
            )
        }
    }

    return PulseData {
        matchInfo,
        partsRequests: data
            .partsRequests
            .iter()
            .map(|pr| format!("Part request for team {}: {}", pr.requestedByTeam, pr.parts))
            .collect(),
        announcements: data
            .announcements
            .iter()
            .map(|a| format!("Event announcement: {}", a.announcement))
            .collect(),
        myUpcommingMatches,
        nowQueuing: data.nowQueuing,
    };
}
