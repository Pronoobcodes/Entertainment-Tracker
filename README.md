# Entertainment Tracker

A Django web application for tracking movies, TV series, anime, and manga across multiple platforms.

## Features

- **Multi-Source Support**
  - Movies & TV Series from TMDb (The Movie Database)
  - Anime from MyAnimeList (MAL)
  - Manga from MangaDex

- **User Management**
  - Email-based authentication
  - User profiles with customizable information
  - Password change functionality

- **Media Library**
  - Track content in three categories:
    - Currently Watching/Reading
    - Completed
    - Plan to Watch/Read
  - Browse popular content with filters (genre, year)
  - Detailed media information (poster, synopsis, ratings, etc.)

- **Search Functionality**
  - Unified search across all media types
  - Results aggregated from all sources

## Tech Stack

- **Backend**: Django 6.0
- **Database**: SQLite3
- **Frontend**: Bootstrap 5.3, jQuery
- **APIs**: TMDb, MyAnimeList, MangaDex

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "Entertainment Tracker"
   ```

2. **Create and activate a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   TMDB_BEARER_TOKEN=your_tmdb_bearer_token
   MAL_CLIENT_ID=your_mal_client_id
   MAL_CLIENT_SECRET=your_mal_client_secret
   ```

   **How to get API credentials:**
   - **TMDb API**: Visit https://www.themoviedb.org/settings/api and create an API key
   - **MAL API**: Visit https://myanimelist.net/apiconfig and register your application
   - **MangaDex API**: No API key required (public API)

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://localhost:8000/`

## Project Structure

```
Entertainment Tracker/
├── main/                           # Main app (core features)
│   ├── models.py                   # Media and UserMedia models
│   ├── views.py                    # Views for browsing, details, library
│   ├── urls.py                     # URL routing
│   ├── services/                   # API integration services
│   │   ├── tmdb.py                # TMDb API integration
│   │   ├── mal.py                 # MyAnimeList API integration
│   │   ├── dex.py                 # MangaDex API integration
│   │   ├── search.py              # Unified search service
│   │   └── details.py             # Media details service
│   └── templates/main/            # Django templates
│       ├── body.html              # Base template
│       ├── nav.html               # Navigation bar
│       ├── detail.html            # Media detail page
│       ├── card.html              # Media card component
│       ├── category.html          # Category browse page
│       └── search.html            # Search results page
│
├── users/                         # User management app
│   ├── models.py                  # CustomUser model
│   ├── views.py                   # Auth and profile views
│   ├── urls.py                    # URL routing
│   ├── forms.py                   # Registration and password forms
│   └── templates/users/           # User templates
│       ├── auth.html              # Login/Register
│       ├── profile.html           # User library
│       ├── password.html          # Change password
│       └── update_user.html       # Update profile
│
├── Tracker/                       # Project configuration
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Main URL config
│   └── wsgi.py                    # WSGI configuration
│
├── static/                        # Static files
│   ├── styles/main.css            # Custom styles
│   └── js/main.js                 # JavaScript utilities
│
├── requirements.txt               # Python dependencies
├── manage.py                      # Django management script
└── db.sqlite3                     # SQLite database

```

## Usage

### For Users

1. **Register/Login**
   - Create an account using email and password
   - Or login with existing credentials

2. **Browse Content**
   - Navigate to Movies, Series, Anime, or Manga
   - Use filters (genre, year) to narrow results
   - Use search bar for specific titles

3. **Add to Library**
   - Click "Add to Library" on any media detail page
   - Content will be added to "Plan to Watch/Read" by default

4. **Manage Library**
   - Visit your profile to see all tracked content
   - Use status buttons to move items between categories
   - Change your profile information and password

### Admin Access

Access the Django admin panel at `/admin/` to:
- Manage users
- View and edit media database
- Monitor user libraries

## API Details

### Endpoints

| Feature | Endpoint | Auth Required |
|---------|----------|---------------|
| Home/Search | `/` | No |
| Browse Movies | `/movies/` | No |
| Browse Series | `/series/` | No |
| Browse Anime | `/anime/` | No |
| Browse Manga | `/mangas/` | No |
| Media Detail | `/<source>/<id>/` | No |
| Add to Library | `/<source>/<id>/add/` | Yes |
| User Profile | `/users/profile/` | Yes |
| User Library | `/users/profile/` | Yes |
| Update Profile | `/users/update_user/` | Yes |
| Change Password | `/users/change_password/` | Yes |

### Supported Media Sources

- **tmdb**: The Movie Database (movies & TV)
- **mal**: MyAnimeList (anime)
- **mangadex**: MangaDex (manga)

## Features Detail

### Media Browsing
- **Popular Lists**: Browse trending content by type
- **Filtering**: Filter by genre and year
- **Pagination**: Navigate through multiple pages of results

### User Library
- **Three Status Categories**:
  - Watching/Reading: Currently tracking
  - Completed: Finished content
  - Plan to Watch/Read: Added to watchlist

- **Status Management**: Click buttons on profile to change status
- **Quick View**: See posters, titles, and basic info for all tracked content

### Search
- **Unified Search**: Search across all media types simultaneously
- **Smart Results**: Aggregates results from all sources
- **Source Indication**: See which platform each result comes from

## Customization

### Adding New Media Sources

1. Create a new service file in `main/services/` (e.g., `anilist.py`)
2. Implement search and detail functions
3. Update `services/search.py` and `services/details.py`
4. Add new category in `views.py` `CATEGORY_CONFIG`
5. Update URLs in `main/urls.py`

### Styling

Edit `static/styles/main.css` to customize:
- Color scheme (CSS variables at top)
- Typography
- Component styles
- Dark theme styling

## Troubleshooting

### API Credentials Not Working

1. Verify `.env` file is in the project root
2. Check that credentials are correct
3. For TMDb, ensure you're using Bearer token format
4. Restart the development server after updating `.env`

### Database Issues

```bash
# Reset database
python manage.py migrate 0001
python manage.py migrate

# Recreate from scratch
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Missing Dependencies

```bash
# Reinstall all requirements
pip install --upgrade -r requirements.txt
```

## Performance Notes

- Results are cached temporarily to reduce API calls
- Static files are served efficiently with Bootstrap CDN
- Database queries are optimized with `select_related()`
- Search results are limited to prevent overload

## Future Enhancements

- [ ] User ratings and reviews
- [ ] Social features (friends, recommendations)
- [ ] Watchlist sharing
- [ ] Episode tracking for TV series
- [ ] Reading progress for manga
- [ ] API rate limiting and caching
- [ ] Mobile app
- [ ] Dark/Light mode toggle

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please check the project documentation or create an issue.

---

**Happy Tracking!** 🎬🎥📺✨
