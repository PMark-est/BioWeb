const windowWidth = window.innerWidth;
const windowHeight = window.innerHeight;
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

function createImageRandomPos(images, xs, ys) {
	let image = new Image();
	image.src = 'bacteria.svg';
	const x = Math.floor(Math.random() * window.innerWidth);
	const y = Math.floor(Math.random() * window.innerHeight);
	images.push(image);
	xs.push(x);
	ys.push(y);
}

const images = [];
const xs = [];
const ys = [];
let randomAngle;
const speed = 2;
const circle = 2 * Math.PI;
for (let index = 0; index < 50; index++) {
	createImageRandomPos(images, xs, ys);
}
const imgSize = 30;

function animate() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	for (let i = 0; i < images.length; i++) {
		randomAngle = Math.random() * circle;
		xs[i] += speed * Math.cos(randomAngle);
		ys[i] += speed * Math.sin(randomAngle);
		if (
			xs[i] < -imgSize ||
			ys[i] < -imgSize ||
			xs[i] > windowWidth + imgSize ||
			ys[i] > windowHeight + imgSize
		) {
			xs[i] = Math.floor(Math.random() * window.innerWidth);
			ys[i] = Math.floor(Math.random() * window.innerHeight);
		}
		ctx.drawImage(images[i], xs[i], ys[i], imgSize, imgSize);
	}
	setTimeout(() => {
		requestAnimationFrame(animate);
	}, 16);
}

animate();
