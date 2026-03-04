// 0.6 is a good distance threshold value to judge
// whether the descriptors match or not
const maxDescriptorDistance = 0.6
const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, maxDescriptorDistance)

const results = fullFaceDescriptions.map(fd => faceMatcher.findBestMatch(fd.descriptor))