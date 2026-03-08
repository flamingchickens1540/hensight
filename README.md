# Hensight

Hensight is a fun pit display! It has two parts. Internal Hensight is for pit crew, displaying match schedule, queue timer, livestream, and more. External Hensight is for pit visitors, where it shows fun facts about the events, robot cad, and more.

## Usage

```bash
# install pm2
bun  i  pm2  -g

# run program
source  update.sh
```

## Config

Open `src/lib/config.ts`:

```ts
export const eventKey = '2026pncmp';
export const year = '2026';
export const team = '1540';
export const timeZone = 'America/Los_Angeles';
```

Open `.env` and enter your tba and nexus api key as such:

```
tbaKey = <insertKey>
nexusKey = <insertKey>
```
