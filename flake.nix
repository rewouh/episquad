{
  description = "Poetry2nix builder to run the Episquad tool";
  
  inputs.rewuchain.url = "git+ssh://git@github.com/rewouh/rewuchain.git";

  outputs = { self, rewuchain }: 
    let 
      system = "x86_64-linux";
      episquad = rewuchain.poetry.mkPoetryApplication { projectDir = ./.; };
    in {
      devShells.${system}.default = rewuchain.pkgs.mkShell {
        buildInputs = [
          episquad
        ];
      };
    };
}

