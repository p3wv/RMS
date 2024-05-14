import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getDatabase, ref } from "firebase/database";

const firebaseConfig = {
    apiKey: "AIzaSyD6k3nIjIAfmhVbLKJWDz8qylxpJOvI0p4",
    authDomain: "rms-test-d41de.firebaseapp.com",
    projectId: "rms-test-d41de",
    storageBucket: "rms-test-d41de.appspot.com",
    messagingSenderId: "1084831064966",
    appId: "1:1084831064966:web:43f0a1b7a15841436a4207"
};

  const app = initializeApp(firebaseConfig);
  const db = getDatabase();
  const reference =ref (db, 'previous_orders/')

  function writeOrderData(id, email, address, name, total, items) {
    const db = getDatabase();
    const reference = ref(db, 'previous_orders/' + id);

    set(reference, {
      id: id,
      email: email,
      address: address,
      name: name,
      total: total,
      items: items
    });
  }

writeOrderData()

// firebase.database().ref(/* path */).set({
//  /* attribute: value */
// });