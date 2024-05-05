const firebase = require('firebase');
const sqlite3 = require('sqlite3').verbose();

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  databaseURL: "https://rms-pwa-f5c66-default-rtdb.firebaseio.com/",
  projectId: "RMS PWA",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "RMS"
};

firebase.initializeApp(firebaseConfig);

const db = new sqlite3.Database('/Users/dlaczegociasteczkochinskie/Desktop/INZYNIERKA/RMS/RMS/app/data-dev.sqlite');

db.all('SELECT * FROM orders_done', (err, rows) => {
  if (err) {
    console.error(err.message);
    return;
  }
  rows.forEach(row => {
    firebase.database().ref('https://rms-pwa-f5c66-default-rtdb.firebaseio.com/').push(row);
  });
});

db.close();
