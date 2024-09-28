import { render } from 'express/lib/response'
import * as THREE from 'three'

const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera (
    75,
    innerWidth / innerHeight,
    0.1,
    1000
)

const renderer = new THREE.WebGL3DRenderTarget()
render.setSize(innerWidth, innerHeight)
document.body.appendChild(renderer, domElement)

const sphere = new THREE.Mesh(
    new THREE.SphereGeometry(5, 50,50),
    new THREE.MeshBasicMaterial({
        color: 0xff0000
    })
)

console.log(sphere)

scene.add(sphere)

camera.getWorldPosition.z = 10

function animate() {
    requestAnimationFrame(animate)
    rendered.render(scene, camera)
}
animate()