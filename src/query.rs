// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 Finnegan Dion-Kuhn

use axum::{http::StatusCode, Json};
use chrono::{Datelike, Local, TimeZone};
use rand::{seq::SliceRandom, thread_rng};
use tba_openapi_rust::{
    apis::{configuration::Configuration, event_api},
    models::event_ranking_rankings_inner::EventRankingRankingsInner,
};
use tracing::error;

pub use crate::model::{
    NexusEventStatus, NexusMatch, PulseData, SlideData, StatboticsReturn, StatboticsTeamYear,
};

pub fn get_slide<'a>(
    slides: &'a Vec<impl Fn(&SlideData) -> Option<&'a str>>,
    slide_data: SlideData,
) -> String {
    match slides.choose(&mut thread_rng()).unwrap()(&slide_data) {
        Some(slide) => String::from(slide),
        None => get_slide(slides, slide_data),
    }
}

pub async fn get_statbotics_data(
    client: reqwest::Client,
    team_key: &u16,
    event_key: &str,
) -> StatboticsReturn {
    let data = client
        .get(format!(
            "https://api.statbotics.io/v3/team_year/{}/{}",
            team_key,
            chrono::Utc::now().year()
        ))
        .header("accept", "application/json")
        .send()
        .await
        .unwrap()
        .json::<StatboticsTeamYear>()
        .await
        .unwrap();

    StatboticsReturn {
        team_key: *team_key,
        event_key: event_key.to_string(),
        epa_total: data.epa.total_points.mean,
        wins: data.record.season.wins,
        losses: data.record.season.losses,
    }
}

pub async fn get_event_predictions(
    config: &Configuration,
    event_key: &str,
) -> serde_json::value::Value {
    event_api::get_event_predictions(config, event_key, None)
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
    team_key: &u16,
    event_key: &str,
) -> Result<Json<PulseData>, StatusCode> {
    let data: NexusEventStatus = match client
        .get(format!("https://frc.nexus/api/v1/event/{}", event_key))
        .header("Nexus-Api-Key", nexus_api_key)
        .send()
        .await
        .unwrap()
        .json::<NexusEventStatus>()
        .await
    {
        Ok(d) => d,
        Err(e) => {
            error!("could not get nexus data: {}", e.to_string());
            return Err(StatusCode::NO_CONTENT);
        }
    };

    let myUpcommingMatches: Vec<NexusMatch> = data
        .matches
        .into_iter()
        .filter(|m| {
            (m.redTeams.as_ref().unwrap().contains(&team_key.to_string())
                || m.blueTeams
                    .as_ref()
                    .unwrap()
                    .contains(&team_key.to_string()))
                && m.status != "On field"
        })
        .collect();

    let matchInfo: String = if !myUpcommingMatches.is_empty() {
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

        format!(
            "Team {}'s next match is {} {}",
            team_key,
            nexus_match.label,
            match &queue_time {
                3600.. => {
                    format!("and will queue in {} hour(s)", queue_time / 3600)
                }
                60..3600 => {
                    format!("and will queue in {} minute(s)", queue_time / 60)
                }
                30..60 => format!("and will queue in {} second(s)", queue_time),
                ..30 => "is queueing NOW".to_string(),
            }
        )
    } else {
        format!(
            "Team {} doesn't have any future matches scheduled yet",
            team_key
        )
    };

    Ok(Json(PulseData {
        teamKey: *team_key,
        eventKey: event_key.to_string(),
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
    }))
}
