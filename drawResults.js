faceapi.drawDetection('overlay', mtcnnResults.map(res => res.faceDetection), { withScore: false })
faceapi.drawLandmarks('overlay', mtcnnResults.map(res => res.faceLandmarks), { lineWidth: 4, color: 'red' })

results.forEach((bestMatch, i) => {
  const box = fullFaceDescriptions[i].detection.box
  const text = bestMatch.toString()
  const drawBox = new faceapi.draw.DrawBox(box, { label: text })
  drawBox.draw(canvas)
})