window.onload = () => {
  demarrerCamera();
};

async function demarrerCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;
  video.onloadedmetadata = () => chargerModeles();
}

async function chargerModeles() {
  await Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('./models/weights'),
    faceapi.nets.faceExpressionNet.loadFromUri('./models/weights')
  ]);

  console.log("✅ Modèles chargés avec succès !");
  demarrerDetection();
}

// Définie AVANT d'être appelée
function demarrerDetection() {
  setInterval(async () => {
    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceExpressions();

    console.log(detections);
  }, 200);
}
function demarrerDetection() {
  const canvas = document.getElementById('overlay');
  canvas.style.position = 'absolute';
  canvas.style.top = '0';
  canvas.style.left = '0';

  const ctx = canvas.getContext('2d');
  let derniereDetection = []; // ← garde le dernier résultat

  // Analyse toutes les 200ms (pas trop fréquent)
  setInterval(async () => {
    derniereDetection = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceExpressions();
  }, 200);

  // Affichage fluide séparé de l'analyse
  function dessiner() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.style.width = video.offsetWidth + 'px';
    canvas.style.height = video.offsetHeight + 'px';

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    derniereDetection.forEach(det => {
      const { x, y, width, height } = det.detection.box;

      ctx.strokeStyle = '#00ff88';
      ctx.lineWidth = 2;
      ctx.shadowColor = '#00ff88';
      ctx.shadowBlur = 10;
      ctx.strokeRect(x, y, width, height);

      const emotion = Object.entries(det.expressions)
        .sort((a, b) => b[1] - a[1])[0][0];
      ctx.fillStyle = '#00ff88';
      ctx.font = '14px monospace';
      ctx.fillText(emotion.toUpperCase(), x, y - 8);
    });

    requestAnimationFrame(dessiner); // ← boucle fluide
  }

  dessiner(); // Lance la boucle
}