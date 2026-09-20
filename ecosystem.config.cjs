module.exports = {
	apps: [
		{
			name: 'hensight',
			script: 'bun',
			args: 'build/index.js',
			interpreter: 'none',
			env: {
				PORT: 5302,
				HOST: '0.0.0.0'
			}
		}
	]
};
