module.exports = {
	apps: [
		{
			name: 'hensight',
			script: 'bun',
			args: 'build/index.js',
			interpreter: 'none',
			env: {
				PORT: 5303,
				HOST: '0.0.0.0'
			}
		}
	]
};
