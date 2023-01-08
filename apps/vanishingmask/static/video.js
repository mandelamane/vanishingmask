
let videoElem = null;
let imgElem = null;
let canvasElem = null;
let ctx = null;

const width = 640;
let height = 0;

export async function init() {
    videoElem = document.querySelector("#video");
    imgElem = document.querySelector("#photo");
    canvasElem = document.querySelector('#canvas');
    ctx = canvasElem.getContext('2d');

    try {
        videoElem.srcObject = await navigator.mediaDevices.getUserMedia({video:true, audio: false});
        await videoElem.play();
    } catch(e) {
        window.alert("Initialize Video stream: " + e);
    }

    height = videoElem.videoHeight / (videoElem.videoWidth / width);
    if (isNaN(height)) {
            height = width / (4 / 3);
    }

    for (let e of [videoElem, imgElem, canvasElem]) {
        e.width = width;
        e.height = height;
    }

    showVideo();
}

export function showVideo() {
    imgElem.style.visibility = 'hidden';
}

// return blob
export async function takeScreenShot() {
    ctx.drawImage(videoElem, 0, 0, width, height);

    return new Promise((resolve, reject) => {
        canvasElem.toBlob(resolve);
    })
}

export function showPicture(blob) {
    imgElem.src = URL.createObjectURL(blob);
    imgElem.style.visibility = 'visible';
}