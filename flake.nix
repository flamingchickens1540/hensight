{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    rust-overlay.url = "github:oxalica/rust-overlay";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    rust-overlay,
    systems,
  }:
    flake-utils.lib.eachSystem (import systems)
    (system: let
      overlays = [(import rust-overlay)];
      pkgs = import nixpkgs {
        inherit system overlays;
      };
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          cargo
          rustfmt
          clippy
          rust-analyzer
        ];
      };
      packages.default = pkgs.rustPlatform.buildRustPackage {
        pname = "hensight";
        version = "0.0.1";
        src = ./.;

        cargoLock = {
          lockFile = ./Cargo.lock;
          outputHashes."tba-openapi-rust-3.9.5" = "sha256-CgrnFa+ziQlZKj2Fl/QgDypylOQWXPPP8OZzoC00h4w=";
        };

        nativeBuildInputs = [pkgs.pkg-config];
        PKG_CONFIG_PATH = "${pkgs.openssl.dev}/lib/pkgconfig";
      };
    });
}
