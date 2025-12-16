
// Firebase config for retail-sales-8690c (Your project)
// You may need to get the actual web app config from Firebase Console
// Go to: Firebase Console > Project Settings > Your apps > Web app > Config
export const firebaseConfig = {
  "projectId": process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || "retail-sales-8690c",
  "apiKey": process.env.NEXT_PUBLIC_FIREBASE_API_KEY || "AIzaSyDYgkvI5bp4DY6uy12GJRTBqSpzjf1-WFE",
  "authDomain": process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || "retail-sales-8690c.firebaseapp.com",
  "storageBucket": process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET || "retail-sales-8690c.appspot.com",
  "messagingSenderId": process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || "",
  "appId": process.env.NEXT_PUBLIC_FIREBASE_APP_ID || ""
};
