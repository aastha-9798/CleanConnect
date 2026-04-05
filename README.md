# **CleanConnect**
This repository contains the documentation for CleanConnect.
## Project Overview
Improper waste disposal is one of the most pressing environmental and public health challenges faced by urban and semi-urban areas today. Waste problems often go unreported, or reported cases lack sufficient evidence and location accuracy. Additionally, community participation in cleanliness drives is limited due to poor awareness and coordination. Improper waste management has a direct impact on environmental sustainability, public health, and the quality of life. Uncollected and unsegregated waste leads to air, water, and soil pollution, increases the spread of diseases, and contributes to climate change through greenhouse gas emissions.
## Approach
The current approach involves designing as a web-based application that integrates geo-location services, image processing, and community engagement features to create an efficient waste management platform. The system follows a client–server architecture. The frontend allows users to register/login, upload geo-tagged images, report waste issues, tag authorities, and initiate cleanliness drives. 

The backend handles data storage, user authentication, notification services, and analytics. 

Authentication has been implemented with JWT access tokens and refresh tokens. On successful authentication the API returns a short lived JWT access token that expires after 15 minutes, and a refresh token that expires after 7 days. User can also upload reports using the “Raise an Issue” section of our website. It allows users to share the exact geolocation of their report along with picture of the concern being reported.  

The geolocation enables users to view cleanliness drives organised near them, I.e. in their locality or nearby. This feature is to be added in the “Home” tab as “Community Feed”.
## Tech Stack
- Frontend: HTML, CSS, JavaScript 
- Backend: Python (Flask/Django) 
- Database: MySQL / PostgreSQL 
- Computer Vision: OpenCV with Python for waste image classification (dry vs wet waste) 
- Cloud & Storage: Firebase or AWS for authentication, real-time notifications, and image storage. 
