const size = 5 + 10;
const windowWidth = window.innerWidth;
const windowHeight = window.innerHeight;
const max = Math.PI / 3;
const min = Math.PI / 8;
const difference = max - min;

function createElementRandomPos(elements) {
  const x = Math.floor(Math.random() * (window.innerWidth / 2));
  const y = Math.floor(Math.random() * (window.innerHeight / 2));
  const elem = document.createElement("canvas");
  elem.src = "./Adenine.png";
  elem.className = "testDiv";
  elem.style.top = `${y}px`;
  elem.style.left = `${x}px`;
  document.body.appendChild(elem);
  elements.push(elem);
}

function moveElements(elements) {
  const speed = 5;
  const length = elements.length;
  const positions = [];
  const deltas = [];
  let rect;
  let randomAngle;
  let elementsLeft = length;
  for (let index = 0; index < length; index++) {
    rect = elements[index].getBoundingClientRect();
    randomAngle = Math.random() * difference + min;
    deltas.push([speed * Math.sin(randomAngle), speed * Math.cos(randomAngle)]);
    positions.push([rect.left, rect.top]);
  }
  var move = setInterval(() => {
    for (let index = 0; index < length; index++) {
      if (elements[index] == undefined) {
        continue;
      }
      positions[index][0] += deltas[index][0];
      positions[index][1] += deltas[index][1];
      elements[index].style.top = `${positions[index][1]}px`;
      elements[index].style.left = `${positions[index][0]}px`;
      if (
        (positions[index][0] + size >= windowWidth) |
        (positions[index][1] + size >= windowHeight)
      ) {
        elements[index].remove();
        delete elements[index];
        delete positions[index];
        delete deltas[index];
        elementsLeft--;
        if (elementsLeft === 0) {
          clearInterval(move);
        }
      }
    }
  }, 16);
}

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

//ctx.fillRect(20, 20, 100, 100);

function createImageRandomPos(images, xs, ys) {
  let image = new Image();
  image.src = "bacteria.svg";
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

animate();

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < images.length; i++) {
    randomAngle = Math.random() * circle;
    xs[i] += speed * Math.cos(randomAngle);
    ys[i] += speed * Math.sin(randomAngle);
    if (
      (xs[i] < -imgSize) |
      (ys[i] < -imgSize) |
      (xs[i] > windowWidth + imgSize) |
      (ys[i] > windowHeight + imgSize)
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
