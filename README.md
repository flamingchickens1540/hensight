# Hensight

Hensight is a fun pit display! It has two parts. Internal Hensight is for pit crew, displaying match schedule, queue timer, livestream, and more. External Hensight is for pit visitors, where it shows fun facts about the events, robot cad, and more.

## Usage
1. Install [bun](https://bun.sh)
2. Install [PM2](https://pm2.io/docs/runtime/guide/installation/)
3. Run the program
```bash
source update.sh
```

## Config
Open `src/lib/config.ts` and set the following values:

```ts
export const eventKey = '2026orwil';
export const lastEventKey = '2026orsal';
export const year = '2026';
export const pointsLastYear = 4697484;
export const team = '1540';
export const timeZone = 'America/Los_Angeles';
export const bottomLeft = 'announcements'; // either rotations to show who is supposed to be in the pits based off 1540 schedule or announcemnts to show nexus announcements (recommended for other teams)
```

### API Config
- Visit [The Blue Alliance](https://www.thebluealliance.com/account/login?next=http://www.thebluealliance.com/account) and create an API Key.
- Visit the [Nexus API Page](https://frc.nexus/en/api) and create three things
  1. A pull API Key
  2. A push webhook, enting the URL of your program (https://whatever.your.ip.is/api/nexus), and selecting "All Events" and "Live event status"
  3. A webhook token.

Open `.env` and put your two API keys and token in:
```
tbaKey = <insertKey>
nexusKey = <insertKey>
nexusWebhookToken = <insertToken>
```

### External Hensight
- If you plan to use external hensight, place a GLB of your robot's cad in `src/lib/assets` and make sure it's named `cad.glb`
- You you might also remove outreach unless you like giving us free advertising 😁
- Statistics are updated for the current event when the page loads, and visit `/external/updateStats` in your browser to update global statistics
- If you wish to reset button presses, simply delete `clicks.db`