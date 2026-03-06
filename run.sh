pm2 stop ecosystem.config.cjs
bun i
bun run build
pm2 start ecosystem.config.cjs