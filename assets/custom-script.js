// const video = document.getElementsByClassName('webCam');

// if (navigator.mediaDevices.getUserMedia) {
// 	navigator.mediaDevices.getUserMedia({ video: true })
//         .then( (stream) => { 
//           video.srcObject = stream;
//     	})
//   		.catch(function (error) {
//           console.log("Something went wrong!");
//           console.log(error);
//           return;
//         });
// };
window.onload = () => {
    let first_btn = document.getElementById('btn_0');

    first_btn.style.borderTopLeftRadius = 10;
    first_btn.style.borderBottomLeftRadius = 10;
    first_btn.style.border = '1px solid #808080';
}




