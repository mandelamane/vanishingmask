import Button from "./button.js";
import * as video from "./video.js";

let blob = null;
let takePictureButton = null;
let vanishButton = null;
let resetButton = null;

function startup() {
    video.init();
    takePictureButton = new Button(document.querySelector("#startbutton"), function() {
        takePictureButton.disable();
        video.takeScreenShot().then(b => {
            blob = b;
            video.showPicture(blob);
            vanishButton.enable();
        })
    });
    vanishButton = new Button(document.querySelector("#vanishbutton"), function() {
        vanishButton.disable();
        vanishmask(blob).then(blob => {
            video.showPicture(blob);
        })
    });
    resetButton = new Button(document.querySelector("#resetbutton"), function() {
        reset();
    });
    reset();
}

async function vanishmask(blob) {
    const  formdata = new FormData();
    formdata.set("picture", blob);
    return await (await fetch('/upload', { method: "POST", body: formdata })).blob();
}

function reset() {
    blob = null;
    takePictureButton.enable();
    vanishButton.disable();
    resetButton.enable();
    video.showVideo();
}

startup();