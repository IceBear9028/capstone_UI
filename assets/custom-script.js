let divBox = document.getElementById('webCam');

const video = document.createElement('video');
video.autoplay = true;

const testDiv = document.createElement('div');

divBox.appendChild(testDiv);


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