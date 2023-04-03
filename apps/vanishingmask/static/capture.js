import Button from "./button.js";
import * as video from "./video.js";

let blob = null;
let m2f_blob = null;
let uploadInput = null;
let takePictureButton = null;
let vanishButton = null;
let resetButton = null;
let downloadButton = null;

function startup() {
    video.init();
    uploadInput = document.querySelector('#fileinput');
    uploadInput.addEventListener("change", function (ev) {
        takePictureButton.disable();
        vanishButton.enable();
        changeImage(ev);
    });
    takePictureButton = new Button(document.querySelector("#startbutton"), function () {
        takePictureButton.disable();
        video.takeScreenShot().then(b => {
            blob = b;
            video.showPicture(blob);
            vanishButton.enable();
        })
    });
    vanishButton = new Button(document.querySelector("#vanishbutton"), function () {
        vanishButton.disable();
        uploadInput.disabled = true;
        vanishmask(blob).then(blob => {
            m2f_blob = blob;
            video.showPicture(blob);
            downloadButton.enable();
        })
    });
    resetButton = new Button(document.querySelector("#resetbutton"), function () {
        reset();
    });
    downloadButton = new Button(document.querySelector("#downloadbutton"), function () {
        download(m2f_blob);
    });
    reset();
}

async function vanishmask(blob) {
    const formdata = new FormData();
    formdata.set("picture", blob);
    return await (await fetch('/upload', { method: "POST", body: formdata })).blob();
}

function download(blob) {
    if (blob) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        document.body.appendChild(a);
        a.download = 'mask2face.png';
        a.href = url;
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
    }
}

function changeImage(ev) {
    const file = ev.target.files[0];
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        const dataUrl = reader.result;
        blob = dataUrlToBlob(dataUrl);
        video.showPicture(blob);
    });
    reader.readAsDataURL(file);
}

function dataUrlToBlob(dataUrl) {
    const parts = dataUrl.split(';base64,');
    const contentType = parts[0].split(':')[1];
    const raw = window.atob(parts[1]);
    const rawLength = raw.length;
    const uInt8Array = new Uint8Array(rawLength);

    for (let i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }

    return new Blob([uInt8Array], { type: contentType });
}

function reset() {
    blob = null;
    m2f_blob = null
    uploadInput.disabled = false;
    takePictureButton.enable();
    vanishButton.disable();
    resetButton.enable();
    downloadButton.disable();
    video.showVideo();
}

startup();