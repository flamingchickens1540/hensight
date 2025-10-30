# Hensight

Hensight is a fun pit display! It has two parts. Internal Hensight is for pit crew, displaying match schedule, queue timer, livestream, and more. External Hensight is for pit visitors, where it shows fun facts about the events, robot cad, and more.

## Usage

```bash
# install required packages
bun i pm2 -g
bun i
# build program
bun run build
# run program
pm2 start ecosystem.js
```