<script lang="ts">
  import { browser } from '$app/environment'
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
  import { GLTFLoader } from 'three/examples/jsm/Addons.js';
  import { onMount } from 'svelte'
  import * as THREE from 'three'
	import { goto } from '$app/navigation';

  // Declare a variable to hold the container element
  let canvasContainer: any

  const loader = new GLTFLoader()

  if (browser) {
    let camera: THREE.PerspectiveCamera
    let scene: THREE.Scene
    let renderer: THREE.WebGLRenderer
    let controls: OrbitControls
    let light: THREE.DirectionalLight

    let canvasWidth = 1920
    let canvasHeight = 1080

    // Run this code when the component is mounted
    onMount(() => {
      scene = new THREE.Scene()
      camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000) // Aspect ratio set to 1 initially, the first parameter is the field of view, the second is the aspect ratio, the third is the near clipping plane, and the fourth is the far clipping plane
      renderer = new THREE.WebGLRenderer()
      controls = new OrbitControls(camera, renderer.domElement)
      light = new THREE.DirectionalLight(0xffffff, 3)

      canvasWidth = canvasContainer.clientWidth
      canvasHeight = canvasContainer.clientHeight
      
      loader.load( '/src/lib/assets/koenigsegg-ccx.glb', function(gltf) {
        scene.add( gltf.scene );
      }, undefined, function(error) {
        console.error( error );
      });

      scene.background = new THREE.Color(0x1c1c1c)
      renderer.setSize(canvasWidth, canvasHeight)
      renderer.domElement.classList.add('size-full')
      canvasContainer.appendChild(renderer.domElement)

      light.position.set(camera.position.x, camera.position.y, camera.position.z)
      scene.add(light)
      const ambient = new THREE.AmbientLight(0xffffff, 0.3)
      scene.add(ambient)

      controls.enableDamping = true
      controls.dampingFactor = 0.05
      controls.autoRotate = true
      controls.autoRotateSpeed = 1.5
      controls.enableZoom = true;
      controls.maxDistance = 10;
      controls.enablePan = false;

      camera.position.z = 5

      animate()
    })

    // Function to render the scene
    const render = () => {
      renderer.clear()
      renderer.render(scene, camera)
    }

    const animate = () => {
      requestAnimationFrame(animate)

      // Update the camera's aspect ratio and position and change light position to match camera
      camera.aspect = canvasWidth / canvasHeight
      camera.updateProjectionMatrix()
      light.position.set(camera.position.x, camera.position.y, camera.position.z)
      
      controls.update()
      render()
    }
  }
</script>
<section bind:this={canvasContainer} class="h-67.5 w-120 flex justify-center items-center">
    <!-- The canvas element will be appended here -->
</section>
<div class="w-full h-67.5 m-auto text-center border-14 border-(--yellow) absolute z-10">
    <nav class="p-1 flex gap-2 justify-center bottom-1 fixed w-full text-3xl font-bold">
        <button
            class="rounded-xl border-4 border-(--yellow) p-1.5 w-[10 bg-(--black)"
            onclick={() => {
                goto('/external/');
            }}>Back</button
	    >
    </nav>
</div>