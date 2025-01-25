{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    rust-overlay.url = "github:oxalica/rust-overlay";
  };

  outputs =
    {
      self,
      nixpkgs,
      rust-overlay,
    }:
    nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed (
      system:
      let
        overlays = [ (import rust-overlay) ];
        pkgs = import nixpkgs {
          inherit system overlays;
        };
      in
      {
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

          useFetchCargoVendor = true;

          cargoHash = "sha256-xTjQ4wjEEDN2MdorKkw+rSmI6ua02eI1TonWHFJsbTY=";

          nativeBuildInputs = [ pkgs.pkg-config ];
          PKG_CONFIG_PATH = "${pkgs.openssl.dev}/lib/pkgconfig";
        };
      }
    );
}
