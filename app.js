console.log(faceapi);

const run = async()=>{
    if (!faceapi) {
        console.error('faceapi is not loaded');
        return;
    }
    // We need to load our models
    // Loading the models is going to use await

    await Promise.all([
        faceapi.nets.ssdMobilenetv1.loadFromUri('./models'),
        faceapi.nets.faceLandmark68Net.loadFromUri('./models'),
        faceapi.nets.faceRecognitionNet.loadFromUri('./models'),
        faceapi.nets.ageGenderNet.loadFromUri('./models'),
    ])

    const face1 = document.getElementById('face')
    let faceAIData = await faceapi.detectAllFaces(face1).withFaceLandmarks().withFaceDescriptors().withAgeAndGender()
    console.log(faceAIData);

}

run()