console.log('안녕하세요');


const testDiv = document.getElementsByClassName('webCamContainer');
const video = document.createElement('video');
console.log(video);
console.log(testDiv);
video.autoplay = true;
video.muted = true;

testDiv.appendChild('video');

//const video = document.createElement("video");
//
//const testDiv = document.createElement("div");

//const testDivConsole = document.querySelector(".main.container");
//console.log(testDivConsole);
//console.log(divBox.childElementCount);
//divBox.appendChild(testDiv);
//console.log('시바련들아');
//console.log(divBox.childElementCount);

if (navigator.mediaDevices.getUserMedia) {
	navigator.mediaDevices.getUserMedia({ video: true })
        .then( (stream) => { 
          video.srcObject = stream;
    	})
  		.catch(function (error) {
          console.log("Something went wrong!");
          console.log(error);
          return;
        });
};