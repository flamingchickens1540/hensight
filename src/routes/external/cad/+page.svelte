<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import type { WebGLRenderer } from 'three';

	let canvasContainer: HTMLDivElement;

	onMount(async () => {
		const THREE = await import('three');
		const { OrbitControls } = await import('three/examples/jsm/controls/OrbitControls.js');
		const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');

		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
		const renderer = new THREE.WebGLRenderer();
		const controls = new OrbitControls(camera, renderer.domElement);
		const ambientLight = new THREE.AmbientLight(0xffffff, 0.3)
		const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
		const loader = new GLTFLoader();

		const canvasWidth = canvasContainer.clientWidth;
		const canvasHeight = canvasContainer.clientHeight;

		const gltf = await loader.loadAsync('/src/lib/assets/cad.glb');
		scene.add(gltf.scene);


		scene.background = new THREE.Color(0x1c1c1c);

		renderer.setSize(canvasWidth, canvasHeight);
		renderer.domElement.classList.add('size-full');
		canvasContainer.appendChild(renderer.domElement);

		controls.enableDamping = true;
		controls.autoRotate = true;
		controls.autoRotateSpeed = 3;
		controls.enableZoom = true;
		controls.maxDistance = 2;
		controls.enablePan = false;
		controls.update();

		camera.position.z = 5;
		camera.aspect = canvasWidth / canvasHeight;
		camera.updateProjectionMatrix();

		scene.add(ambientLight)
		let camPos = camera.position
		directionalLight.position.set(camPos.x, camPos.y, camPos.z);
		
		scene.add(directionalLight)

		function resizeRendererToDisplaySize(renderer: WebGLRenderer) {
			const canvas = renderer.domElement;
			const width = canvas.clientWidth;
			const height = canvas.clientHeight;
			const needResize = canvas.width !== width || canvas.height !== height;
			if (needResize) {
				renderer.setSize(width, height, false);
			}

			return needResize;
		}

		function animate() {
			if (resizeRendererToDisplaySize(renderer)) {
				const canvas = renderer.domElement;
				camera.aspect = canvas.clientWidth / canvas.clientHeight;
				camera.updateProjectionMatrix();
			}
			let camPos = camera.position
			directionalLight.position.set(camPos.x, camPos.y, camPos.z);

			renderer.render(scene, camera);

			requestAnimationFrame(animate);
			controls.update();
		}

		animate();
	});
</script>

<div bind:this={canvasContainer} class="h-67.5 w-120 flex justify-center items-center"> 
	<!-- The canvas element will be appended here -->
</div>

<div class="w-full h-67.5 m-auto text-center border-14 border-(--yellow) absolute z-10">
	<nav class="p-1 flex gap-2 justify-center bottom-1 fixed w-full text-3xl font-bold">
		<button
			class="rounded-xl border-4 border-(--yellow) p-1.5 w-[10 bg-(--black)"
			onclick={() => goto('/external/')}>
			Back
		</button>
	</nav>
</div>