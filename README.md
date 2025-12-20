# Pet Adoption

A Django-based web application for browsing pets, submitting adoption requests, and viewing pet care products.

## Overview
- User accounts with registration, login, OTP verification.
- Pet listings with details, images, and adoption status.
- Adoption request workflow with admin review and success confirmation.
- Simple pet quiz to suggest species based on preferences.
- Pet food catalog with brand images and buy links.

## Tech Stack
- Backend: Django 5
- Database: PostgreSQL (production), SQLite (local dev)
- Frontend: Django templates + CSS
- Server: Gunicorn

## App Structure
- Project: `project/`
- App: `petadoption/`
- Templates: `petadoption/templates/`
- Static: `petadoption/static/`

## Key Models (conceptual)
- `EnterPets`: basic pet info (name, age, specie, image, is_adopted, etc.)
- `AdoptionForm`: user-submitted request linked to a pet
- `PetFood`: brand name, image, and buy link

## Core Pages
- Home: `/`
- Login: `/login/`
- Register: `/register/`
- Verify OTP: `/verify-otp/`
- Pets list: `/pets/`
- Search pets: `/search-pets/`
- Pet detail: `/pet/<id>/`
- Submit adoption request: `/adopt/<id>/`
- Adoption success: `/adoption-success/`
- My requests: `/my-requests/`
- Logout: `/logout/`
- Pet quiz: `/pet-quiz/`
- Quiz result: `/pet-quiz-result/`
- Pet food: `/petfood/`

## Admin Behavior (summary)
- Admin can review adoption requests.
- When a request is approved, the associated pet is marked as adopted.
- Admin can edit , add , delete pets
## Notes
- CSRF trusted origins are configured for Azure App Service.
- Environment variables drive `SECRET_KEY`, `DEBUG`, `ENVIRONMENT`, and `DATABASE_URL`.
##production-link:
- pets12-gvhbg3a4ebebesfn.uaenorth-01.azurewebsites.net
