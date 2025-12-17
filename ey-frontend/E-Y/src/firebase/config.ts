
// Firebase config for retail-sales-8690c (Your project)
// Set these environment variables in your deployment platform (Vercel)
// Go to: Firebase Console > Project Settings > Your apps > Web app > Config
export const firebaseConfig = {
  "projectId": process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || "",
  "apiKey": process.env.NEXT_PUBLIC_FIREBASE_API_KEY || "",
  "authDomain": process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || "",
  "storageBucket": process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET || "",
  "messagingSenderId": process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || "",
  "appId": process.env.NEXT_PUBLIC_FIREBASE_APP_ID || ""
};
