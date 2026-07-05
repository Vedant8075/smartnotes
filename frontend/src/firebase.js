// Firebase initialization for the frontend app
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyB54mFSc6TAgRr5pscv49UiTS7Igo9eyyg",
  authDomain: "smartnotes-3c8e6.firebaseapp.com",
  projectId: "smartnotes-3c8e6",
  storageBucket: "smartnotes-3c8e6.firebasestorage.app",
  messagingSenderId: "182219819754",
  appId: "1:182219819754:web:d0faba082c7d908d166593",
  measurementId: "G-5YBXREZS0Y"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
export { app, auth, googleProvider };

