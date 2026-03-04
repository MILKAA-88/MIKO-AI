const mtcnnForwardParams = {
  // limiting the search space to larger faces for webcam detection
  minFaceSize: 200
}

const mtcnnResults = await faceapi.mtcnn(document.getElementById('inputVideo'), mtcnnForwardParams)