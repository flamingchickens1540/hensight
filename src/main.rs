use axum::Json;
use axum::{routing::get, Router};
use dotenv::dotenv;
use std::env;
use tba_openapi_rust::apis::{
    configuration::{ApiKey, Configuration},
    team_api::get_team,
};
use tokio;
use tower_http::services::ServeFile;

use hensight::{get_event_predictions, get_event_rankings, get_pulse_data};

#[tokio::main]
async fn main() {
    dotenv().ok();
    let mut tba_config = Configuration::new();
    tba_config.api_key = Some(ApiKey {
        prefix: None,
        key: env::var("TBA_API_KEY").expect("TBA_API_KEY must be set in .env"),
    });

    let reqwest_client = reqwest::Client::new();

    let event_key = "2024cc";

    println!(
        "{:?}",
        get_team(&tba_config, "frc1540", None).await.unwrap()
    );

    let app = Router::new()
        .route_service("/", ServeFile::new("templates/hensight.html"))
        .route_service("/dashboard", ServeFile::new("templates/dashboard.html"))
        .route_service("/menu", ServeFile::new("templates/menu.html"))
        .route_service("/menu/robot", ServeFile::new("templates/robomenu.html"))
        .route_service("/menu/misc", ServeFile::new("templates/misc.html"))
        .route_service("/menu/soon", ServeFile::new("templates/comming_soon.html"))
        .route_service("/menu/games", ServeFile::new("templates/games.html"))
        .route_service("/cad", ServeFile::new("templates/cad.html"))
        .route_service("/reveal", ServeFile::new("templates/reveal.html"))
        .route_service("/testhtml", ServeFile::new("templates/test.html"))
        .route_service("/spin", ServeFile::new("templates/chickenspin.html"))
        .route_service("/crossy", ServeFile::new("templates/crossy.html"))
        .route_service("/autos", ServeFile::new("templates/autos.html"))
        .route_service("/autos2", ServeFile::new("templates/autos2.html"))
        .route_service("/autos3", ServeFile::new("templates/autos3.html"))
        .route_service("/pulse_rip_off", ServeFile::new("templates/pulsemain.html"))
        .route_service(
            "/pulse_schedule",
            ServeFile::new("templates/pulse_schedule.html"),
        )
        .route_service("/style.css", ServeFile::new("templates/style.css"))
        .route_service("/common.js", ServeFile::new("templates/common.js"))
        .route_service("/AmpLane.json", ServeFile::new("static/AmpLanePHGF.traj"))
        .route_service(
            "/CenterLane.json",
            ServeFile::new("static/CenterLanePDEABC.traj"),
        )
        .route_service("/FriedEgg.glb", ServeFile::new("static/FriedEgg.glb"))
        .route_service(
            "/FieldCadSmall",
            ServeFile::new("static/CrescendoFieldSmall.gltf"),
        )
        .route_service(
            "/getrankings",
            get(Json(get_event_rankings(&tba_config, event_key, 20).await)),
        )
        .route_service(
            "/getprediction",
            get(Json(get_event_predictions(&tba_config, event_key).await)),
        )
        .route_service(
            "/getnexusdata",
            get(Json(
                get_pulse_data(
                    reqwest_client,
                    &env::var("NEXUS_API_KEY").expect("NEXUS_API_KEY must be set in .env"),
                    1540,
                    event_key,
                )
                .await,
            )),
        );

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3010")
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap();
}
