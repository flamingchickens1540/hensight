import { emitter } from '$lib/nexus';

export function GET() {
	let controller: ReadableStreamDefaultController;

	const stream = new ReadableStream({
		start(c) {
			controller = c;
			const send = async (data: unknown) => {
				controller.enqueue(`data: ${JSON.stringify(data)}\n\n`);
			};

			emitter.on('nexus', send);

			return () => emitter.off('nexus', send);
		}
	});

	return new Response(stream, {
		headers: {
			'Content-Type': 'text/event-stream',
			'Cache-Control': 'no-cache',
			Connection: 'keep-alive'
		}
	});
}
