import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

const firebaseConfig = {
  apiKey: "AIzaSyD8mXqEUIBn-n78Ene8_TJMfwq4V8BLaVc",
  authDomain: "rms-pwa-f5c66.firebaseapp.com",
  projectId: "rms-pwa-f5c66",
  storageBucket: "rms-pwa-f5c66.appspot.com",
  messagingSenderId: "470987624417",
  appId: "1:470987624417:web:dcda0a755c2c17ab750ca0",
  measurementId: "G-Y7PBZTW5P9"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);