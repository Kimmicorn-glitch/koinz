# Web App

Next.js (App Router) frontend with Tailwind-driven red/white minimal geometric dashboard design.

## Design System

- Palette: deep red `#B11226`, soft red `#EE425E`, white backgrounds
- UI language: thin borders, rounded 2xl cards, soft shadows
- Motion: fade/slide transitions for dashboard cards and chart elements
- Components: worker profile cards, employer analytics cards, circular match indicator

## Environment Setup

```bash
cd web-app
npm install
npm run dev
```

Set `NEXT_PUBLIC_API_BASE_URL` to backend API URL.

## UI Theme Guidelines

- Keep white-first canvas with red accent blocks
- Avoid bulky UI kits; use Tailwind utilities and custom components
- Preserve responsive card grids for mobile/tablet/desktop breakpoints
- Maintain role-based entry points:
  - `/employer/dashboard`
  - `/worker/dashboard`
