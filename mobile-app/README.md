# Mobile App

React Native + Expo client with shared API contract and role-aware navigation.

## Stack

- Expo + React Native + TypeScript
- React Navigation
- Axios API client (`src/services/api.ts`)
- Secure token persistence via `expo-secure-store`

## Setup

```bash
cd mobile-app
npm install
npm run start
```

Set `EXPO_PUBLIC_API_BASE_URL` to backend URL.

## Android Build

```bash
cd mobile-app
npm run android
```

For production artifacts, configure EAS Build and signing in Expo project settings.
