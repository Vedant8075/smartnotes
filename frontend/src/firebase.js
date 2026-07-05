// Firebase initialization for the frontend app
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyB54mFSc6TAgRr5pscv49UiTS7Igo9eyyg",
  authDomain: "smartnotes-3c8e6.firebaseapp.com",
  projectId: "smartnotes-3c8e6",
  storageBucket: "smartnotes-3c8e6.firebasestorage.app",
  messagingSenderId: "182219819754",
  appId: "1:182219819754:web:9a46700871767179166593",
  measurementId: "G-0DV2MY7JDZ"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
export { app, auth, googleProvider };

