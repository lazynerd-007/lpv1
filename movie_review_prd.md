# LemonNPie Platform - Product Requirements Document

## 1. Executive Summary

LemonNPie is a comprehensive Nollywood movie review platform that allows multiple user types to discover, rate, and review Nigerian films. The platform will serve as a community-driven database of Nollywood movies with user-generated content and professional critic reviews. The name reflects our rating philosophy: "Lemon" for disappointing films and "Pie" for exceptional movies.

### Vision
To become the definitive platform for Nollywood movie reviews, celebrating Nigerian cinema while helping audiences discover quality films and avoid disappointing ones.

### Success Metrics
- User engagement: Average session duration > 8 minutes
- Content quality: Average review length > 100 words
- Community growth: 25% month-over-month user growth
- Review authenticity: <5% spam/fake reviews

## 2. Technical Architecture

### Technology Stack
- **Frontend**: Vue.js 3 with Composition API
- **UI Framework**: DaisyUI (Tailwind CSS-based)
- **Backend**: Python (FastAPI/Django)
- **Database**: PostgreSQL
- **Architecture**: Monolithic application
- **Development Approach**: Frontend-first with mock data

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue.js App    │────│  Python API     │────│   PostgreSQL    │
│   (DaisyUI)     │    │   (FastAPI)     │    │    Database     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 3. User Types & Permissions

### 3.1 Guest Users
**Capabilities:**
- View movie details and information
- Read all reviews and ratings
- Browse movie catalogs and search
- View critic profiles and reviews
- Access basic filtering and sorting

**Limitations:**
- Cannot write reviews or rate movies
- Cannot create watchlists
- Limited access to advanced features

### 3.2 Registered Users
**Capabilities:**
- All guest user capabilities
- Write and edit their own reviews
- Rate movies (1-10 scale)
- Create and manage personal watchlists
- Follow other users and critics
- Like/dislike reviews
- Comment on reviews
- Create custom movie lists

**Profile Features:**
- Review history
- Rating statistics
- Watchlist management
- Following/followers system

### 3.3 Verified Critics
**Capabilities:**
- All registered user capabilities
- Verified badge display
- Priority review placement
- Enhanced profile customization
- Access to pre-release screening data
- Advanced analytics dashboard
- Bulk import tools for existing reviews

**Verification Requirements:**
- Professional film critic credentials
- Published work verification
- Application and approval process

## 4. Core Features

### 4.1 Nollywood Movie Database
**Movie Information:**
- Title (English/Local language), release date, runtime
- Genre (Drama, Comedy, Action, Romance, Thriller, etc.)
- Director, producer, cast, and crew information
- Plot synopsis and trailers
- Production company and budget (when available)
- Cinema/streaming platform availability
- Poster and promotional images
- Filming locations across Nigeria
- Language (English, Igbo, Yoruba, Hausa, Pidgin, etc.)

**Nollywood-Specific Features:**
- Production state/region (Lagos, Abuja, Enugu, Kano, etc.)
- Cinema chain availability (Filmhouse, Genesis, Silverbird, etc.)
- Streaming platform presence (Netflix, Prime Video, IROKOtv, etc.)
- Awards and nominations (AMVCA, AMAA, etc.)
- Box office performance in Nigerian markets

**Data Sources:**
- Manual curation of Nollywood releases
- Industry partnerships with distributors
- User-submitted movie information
- Social media and news monitoring

### 4.2 LemonNPie Review System
**Review Components:**
- LemonNPie rating (1-10 scale: 1-4 = Lemon 🍋, 5-6 = Neutral, 7-10 = Pie 🥧)
- Written review (min 50 characters for quality)
- Spoiler warnings and hidden content
- Review categories (Story, Acting, Cinematography, Production Quality, Cultural Authenticity)
- Helpfulness voting system
- Nollywood-specific tags (Low Budget Magic, Star Power, Cultural Impact, etc.)

**Review Features:**
- Rich text editor with formatting
- Media attachments (images, GIFs)
- Review templates for different Nollywood genres
- Draft saving functionality
- Edit history tracking
- Local language support for reviews

### 4.3 LemonNPie Rating & Recommendation Engine
**Rating Aggregation:**
- Overall LemonNPie score (Lemon vs Pie ratio)
- User rating average with regional breakdown
- Critic rating average (weighted)
- Distribution breakdown with visual indicators
- Trending scores within Nigerian markets

**Nollywood-Specific Recommendations:**
- Similar Nollywood movies suggestions
- Personalized recommendations based on Nigerian viewing preferences
- Genre-based recommendations (Nollywood Comedy, Drama, etc.)
- Actor/Director filmography suggestions
- Regional preference-based recommendations
- "If you liked this Hollywood movie, try this Nollywood film"

### 4.4 Search & Discovery
**Search Functionality:**
- Movie title search with autocomplete (English and local languages)
- Advanced filters (genre, year, rating, language, production state)
- Actor/director search (Nollywood celebrities)
- Review content search
- Production company search

**Nollywood Discovery Features:**
- Trending Nollywood movies
- New Nollywood releases
- Top-rated Nigerian films
- Genre-specific browsing (Nollywood Comedy, Epic Drama, etc.)
- "Rising Stars" - New Nollywood actors to watch
- "Nollywood Classics" - Timeless Nigerian films
- Regional cinema showcases (Lagos, Enugu, Kano productions)

## 5. User Interface Design

### 5.1 Design System
**Visual Identity:**
- Vibrant and cool color palette
- Modern, cinema-inspired aesthetics
- DaisyUI component library integration
- Responsive design for all devices

**Color Scheme:**
- Primary: Nollywood Gold (#FFD700)
- Secondary: Nigerian Green (#008751)
- Accent: Vibrant Orange (#FF6B35) 
- Lemon Indicator: Bright Yellow (#FFEB3B)
- Pie Indicator: Rich Brown (#8D4E2A)
- Background: Deep Navy (#1A1B2E) / Cream White (#FFF8E1)
- Success: Emerald Green (#10B981)
- Warning: Amber (#F59E0B)

### 5.2 Key Pages & Components

**Homepage:**
- Hero section with featured Nollywood movies
- "Latest Pies" - Top-rated new releases
- "Fresh Lemons" - Recent disappointments to avoid  
- Trending Nollywood reviews carousel
- "Nollywood Rising" - Upcoming releases
- Personalized recommendations (logged in users)
- "This Week in Nollywood" news section

**Movie Detail Page:**
- Movie poster and key Nollywood information
- LemonNPie score with visual indicators (🍋 or 🥧)
- Rating summary and distribution
- Review sections (Critics vs Users vs International viewers)
- Cast and crew information with Nollywood filmography links
- Similar Nollywood movies recommendations  
- Trailer and media gallery
- "Where to Watch" (Nigerian cinemas/streaming)

**Review Writing Interface:**
- Rich text editor with formatting options
- LemonNPie rating slider (visual feedback: Lemon 🍋 to Pie 🥧)
- Nollywood-specific category ratings (Production Quality, Cultural Authenticity, etc.)
- Spoiler warning toggle
- Preview functionality  
- Nollywood genre tagging system
- Local language support toggle

**User Profile:**
- Profile information and statistics
- Review history and ratings
- Watchlists and custom lists
- Following/followers
- Activity feed

## 6. Database Schema

### 6.1 Core Tables

**Users Table:**
```sql
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- user_type (guest, user, verified_critic)
- profile_picture
- bio
- verification_status
- created_at, updated_at
```

**Movies Table:**
```sql
- id (Primary Key)
- title
- local_title (Igbo/Yoruba/Hausa name if applicable)
- release_date
- runtime
- genre (JSON array)
- language (JSON array - English, Igbo, Yoruba, Hausa, Pidgin)
- director
- producer
- cast (JSON array)
- plot_summary
- poster_url
- trailer_url
- production_company
- filming_locations (JSON array)
- production_state
- box_office_ng (Nigerian box office)
- streaming_platforms (JSON array)
- awards (JSON array)
- created_at, updated_at
```

**Reviews Table:**
```sql
- id (Primary Key)
- user_id (Foreign Key)
- movie_id (Foreign Key)
- lemon_pie_rating (1-10, with Lemon/Pie categorization)
- review_text
- review_language (en, ig, yo, ha, pcm)
- spoiler_warning
- cultural_authenticity_rating
- production_quality_rating
- nollywood_tags (JSON array)
- is_published
- helpfulness_score
- created_at, updated_at
```

**Additional Tables:**
- Watchlists
- Review_Likes
- User_Follows
- Movie_Ratings_Aggregate
- Categories
- Movie_Categories

## 7. API Endpoints

### 7.1 Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile

### 7.2 Movies
- `GET /api/movies` - List movies with pagination
- `GET /api/movies/{id}` - Get movie details
- `GET /api/movies/search` - Search movies
- `GET /api/movies/trending` - Get trending movies
- `GET /api/movies/{id}/reviews` - Get movie reviews

### 7.3 Reviews
- `POST /api/reviews` - Create review
- `GET /api/reviews/{id}` - Get review details
- `PUT /api/reviews/{id}` - Update review
- `DELETE /api/reviews/{id}` - Delete review
- `POST /api/reviews/{id}/like` - Like/unlike review

### 7.4 Users
- `GET /api/users/{id}` - Get user profile
- `GET /api/users/{id}/reviews` - Get user reviews
- `POST /api/users/{id}/follow` - Follow/unfollow user
- `GET /api/users/{id}/watchlist` - Get user watchlist

## 8. Development Phases

### Phase 1: Frontend Foundation (Weeks 1-3)
**Frontend Development with Mock Nollywood Data:**
- Set up Vue.js project with DaisyUI
- Implement core UI components with Nollywood theming
- Create main pages with mock Nollywood movie data
- Implement responsive design for mobile-first Nigerian audience
- Set up routing and state management
- Integrate LemonNPie visual rating system

**Deliverables:**
- Functional frontend with Nollywood-focused design
- Mock data integration (popular Nollywood films)
- Responsive design implementation
- LemonNPie component library documentation

### Phase 2: Backend Development (Weeks 4-7)
**API and Database Implementation:**
- Set up Python backend (FastAPI)
- Design and implement PostgreSQL schema
- Create API endpoints
- Implement authentication system
- Set up data validation and error handling

**Deliverables:**
- Complete API implementation
- Database schema and migrations
- Authentication system
- API documentation

### Phase 3: Integration & Nollywood Features (Weeks 8-11)
**Frontend-Backend Integration:**
- Replace mock data with API calls
- Implement real-time features
- Add advanced search and filtering for Nollywood content
- Implement recommendation engine with Nigerian preferences
- User profile and review management
- Multi-language support for reviews
- Nollywood industry partnerships integration

**Deliverables:**
- Fully integrated application
- Nollywood-specific features implementation
- Multi-language support
- Performance optimization

### Phase 4: Polish & Launch (Weeks 12-14)
**Final Preparations:**
- User testing and bug fixes
- Performance optimization
- Security audit
- Documentation completion
- Deployment preparation

**Deliverables:**
- Production-ready application
- Complete documentation
- Deployment scripts
- User guides

## 9. Success Criteria

### Technical Success Criteria
- Page load times < 2 seconds
- 99.9% uptime
- Mobile responsiveness across all devices
- Accessibility compliance (WCAG 2.1)
- SEO optimization

### User Experience Success Criteria
- Intuitive navigation and user flows
- Engaging visual design
- Fast and accurate search results
- Smooth review writing experience
- Effective recommendation system

### Business Success Criteria
- User registration conversion rate > 15%
- Daily active users growth across Nigerian demographics
- High-quality Nollywood review content
- Low spam/fake review rate
- Positive user feedback scores
- Strong engagement from Nigerian diaspora
- Industry recognition from Nollywood stakeholders

## 10. Risk Assessment & Mitigation

### Technical Risks
- **Database Performance**: Implement proper indexing and query optimization
- **Scalability**: Design with horizontal scaling in mind
- **Security**: Implement comprehensive authentication and data validation

### Content Risks
- **Review Quality**: Implement moderation tools and community reporting
- **Spam/Fake Reviews**: User verification and behavioral analysis
- **Copyright Issues**: Proper attribution and fair use compliance

### Business Risks
- **User Acquisition**: Focus on unique value proposition and user experience
- **Content Moderation**: Develop clear community guidelines and enforcement
- **Competitive Differentiation**: Emphasize community features and critic integration

## 11. Future Enhancements

### Version 2.0 Features
- Mobile application (iOS/Android) with offline viewing
- Social features and user interactions
- Advanced recommendation algorithms
- Video reviews and content
- Nollywood industry API for distributors
- Integration with Nigerian cinema booking systems
- Nollywood news and gossip section
- Multi-language interface (Igbo, Yoruba, Hausa)

### Long-term Vision
- AI-powered review analysis with Nigerian context understanding
- Virtual reality Nollywood movie experiences
- Partnership with major Nollywood producers and distributors
- International expansion to African diaspora markets
- Premium subscription with exclusive Nollywood content
- Nollywood talent discovery and promotion platform

---

**Document Version**: 1.0  
**Last Updated**: July 26, 2025  
**Next Review**: August 26, 2025