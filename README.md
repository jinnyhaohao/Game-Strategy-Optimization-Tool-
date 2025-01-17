# TFT Analyzer

TFT Analyzer is a full-stack web application designed to analyze Teamfight Tactics (TFT) performance and provide actionable insights such as unit synergies, top-performing traits, and personalized recommendations based on match history. The app integrates Riot Games' API to fetch summoner data and uses a backend database for processing and storing information.

---

## Features

- **Summoner Analysis**: View statistics such as average placement, total damage dealt, and first-place wins.
- **Unit Recommendations**: Get insights on top unit pairs and strictly diverse combinations of units.
- **Top Traits Analysis**: Discover the top-performing traits and their diverse combinations.
- **Responsive User Interface**: An interactive and user-friendly React-based frontend.

---

## Tech Stack

### Frontend
- **React** (JavaScript Library)
- **CSS** for styling

### Backend
- **Flask** (Python)
- **Riot Games API** for summoner and match data
- **PostgreSQL** for data storage

### Tools
- **Flask-CORS** to handle cross-origin resource sharing

---

## Installation

### Prerequisites
- **Node.js** (for frontend development)
- **Python 3.x** (for backend development)
- **PostgreSQL**
- **Riot Games API Key**
## Usage

1. Open the frontend in your browser:
   ```
   http://localhost:3000
   ```
2. Enter your **Summoner Name**, **Region**, and **Tag**.


3. View:
   - Summoner Analysis: Average placement, damage, and wins.
   - Top Traits and Unit Recommendations.
---

## Acknowledgments

- Riot Games API: For providing the data.

- React and Flask: For powering the application.
