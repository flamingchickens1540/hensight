import { emitter } from '$lib/nexus';
import { send } from 'vite';

export function GET() {
	let controller: ReadableStreamDefaultController;

	const stream = new ReadableStream({
		start(c) {
			controller = c;
			const send = async (data: unknown) => {
				controller.enqueue(`data: ${JSON.stringify(data)}\n\n`);
			};

			emitter.on('nexus', send);
		},
		cancel() {
			emitter.off('nexus', send);
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
