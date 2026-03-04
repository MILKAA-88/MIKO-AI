const alignedFaceBoxes = results.map(
  ({ faceLandmarks }) => faceLandmarks.align()
)

const alignedFaceTensors = await extractFaceTensors(input, alignedFaceBoxes)

const descriptors = await Promise.all(alignedFaceTensors.map(
  faceTensor => faceapi.computeFaceDescriptor(faceTensor)
))

// free memory
alignedFaceTensors.forEach(t => t.dispose())