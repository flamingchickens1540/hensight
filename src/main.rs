use axum::Json;
use axum::{routing::get, Router};
use dotenv::dotenv;
use fix_fn::fix_fn;
use rand::seq::SliceRandom;
use rand::thread_rng;
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

    // closure so tba_api can be used by them in the future
    #[rustfmt::skip]
    let slides = vec![
        |_| Some("<h4>Team 1540 Thanks</h4><h3>YOU</h3><h4>for joining us in our pits!</h4>"),
        |_| Some("<h4>During each match over</h4><h2 style='font-size:13rem;'i>520,000</h2><h4>eggs are laid in the US!</h4>"),
        |_| Some("<h4>There are as many people that do FIRST as feathers on </h4><h2>Ten and Half chickens!</h2>"),
        |_| Some("<h4>A chicken of the non-flaming variety is expected to score</h4><h3>0</h3><h4>notes during a match!</h4>"),
        |_| Some("<h4>The heaviest chicken was 22lbs! That is</h4><h3>93 lbs</h3><h4>less than the weight of our robot!</h4>"),
        |_| Some("<h4>Our robot is named Fried Egg because</h4><h2>We're cooking</h2><h4>this year!</h4>"),
        |_| Some("<h1 style='font-size:3rem;'>However, in the whimsical scenario where we decide to replace the robot on the field with a live chicken, a cascade of unforeseen consequences would likely unfold. Picture this: amidst the high-stakes game, the unsuspecting chicken, blissfully unaware of the intricate rules governing the match, would likely become the unwitting perpetrator of an array of tech fouls. The referee, undoubtedly perplexed by the surreal turn of events, might find themselves compelled to brandish a red card, signaling not only an expulsion from the game but also drawing attention to the peculiar nature of the infringement.</h1>"),
        |_| Some("<h4>Chickens can squawk as loud as</h4><h2>70 decibels<h2><h4>about as loud as the average classroom</h4>"),
        |_| Some("<h4>FRC Students eat approximately</h4><h3 style=\"font-size: 11rem;\">7,917,000</h3><h4>chickens per year</h4>"),
        |_| Some("<h4>A chicken of the non-flaming variety can make a speaker cycle in</h4><h2>3 seconds!</h2>"),
        |_| Some("<h5>A chicken running on a hamster wheel would take</h5><h3 style=\"font-size:13rem;\">5 hours</h3><h5>to generate enough power for a ES 17-12 battery</h5>"),
        |_| Some("<marquee class=\"marquee\" behavior=\"alternate\" direction=\"down\"scrollamount=\"20\" id=\"logo\"><marquee style=\"margin-bottom: 160px\" behavior=\"alternate\" width=\"100%\" scrollamount=\"20\"><img width=\"250px\" src=\"https://avatars.githubusercontent.com/u/5280254?s=200&v=4\" alt=\"dvd\" id=\"spin\"></marquee></marquee><p id=\"msg\">inside of my head rn</p>"),
    ];

    let get_slide = fix_fn!(|get_slide| -> String {
        match slides.choose(&mut thread_rng()).unwrap()(1) {
            Some(slide) => String::from(slide),
            None => get_slide(),
        }
    });

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
        )
        .route_service("/request", get(get_slide()));

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3010")
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap();
}
