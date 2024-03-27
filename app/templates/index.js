// if("serviceWorker" in navigator){
//     navigator.serviceWorker.register("service_worker.js").then(registration=>{
//       console.log("SW Registered!");
//     }).catch(error=>{
//       console.log("SW Registration Failed");
//     });
// }else{
//   console.log("Not supported");
// }

if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register('/service-worker.jss')
            .then(function (registration) {
                console.log('Service Worker registered with scope:', registration.scope);
            })
            .catch(function (error) {
                console.error('Service Worker registration failed:', error);
            });
    });
}