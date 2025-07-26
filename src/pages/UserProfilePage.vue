<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50">
    <!-- Profile Header -->
    <div class="bg-gradient-to-r from-yellow-400 to-orange-500 py-16">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row items-center gap-8">
          <!-- Profile Picture -->
          <div class="avatar">
            <div class="w-32 h-32 rounded-full bg-white shadow-lg flex items-center justify-center">
              <User class="w-16 h-16 text-gray-600" />
            </div>
          </div>
          
          <!-- Profile Info -->
          <div class="text-center md:text-left text-white">
            <h1 class="text-4xl font-bold mb-2">{{ user.name }}</h1>
            <p class="text-xl text-yellow-100 mb-4">{{ user.bio || 'Nollywood Movie Enthusiast' }}</p>
            <div class="flex flex-wrap justify-center md:justify-start gap-4 text-sm">
              <div class="flex items-center gap-2">
                <Calendar class="w-4 h-4" />
                <span>Joined {{ formatDate(user.joinDate) }}</span>
              </div>
              <div class="flex items-center gap-2">
                <MapPin class="w-4 h-4" />
                <span>{{ user.location || 'Nigeria' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="card bg-white shadow-lg">
          <div class="card-body text-center">
            <div class="text-3xl font-bold text-primary">{{ userStats.totalReviews }}</div>
            <div class="text-gray-600">Reviews Written</div>
          </div>
        </div>
        <div class="card bg-white shadow-lg">
          <div class="card-body text-center">
            <div class="text-3xl font-bold text-success">{{ userStats.averageRating.toFixed(1) }}</div>
            <div class="text-gray-600">Average Rating</div>
          </div>
        </div>
        <div class="card bg-white shadow-lg">
          <div class="card-body text-center">
            <div class="text-3xl font-bold text-warning">{{ userStats.totalLikes }}</div>
            <div class="text-gray-600">Likes Received</div>
          </div>
        </div>
        <div class="card bg-white shadow-lg">
          <div class="card-body text-center">
            <div class="text-3xl font-bold text-info">{{ userStats.moviesWatched }}</div>
            <div class="text-gray-600">Movies Watched</div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tabs tabs-boxed bg-white shadow-lg mb-8">
        <button 
          @click="activeTab = 'reviews'"
          :class="['tab tab-lg', activeTab === 'reviews' ? 'tab-active' : '']"
        >
          <MessageSquare class="w-4 h-4 mr-2" />
          My Reviews
        </button>
        <button 
          @click="activeTab = 'watchlist'"
          :class="['tab tab-lg', activeTab === 'watchlist' ? 'tab-active' : '']"
        >
          <Bookmark class="w-4 h-4 mr-2" />
          Watchlist
        </button>
        <button 
          @click="activeTab = 'favorites'"
          :class="['tab tab-lg', activeTab === 'favorites' ? 'tab-active' : '']"
        >
          <Heart class="w-4 h-4 mr-2" />
          Favorites
        </button>
        <button 
          @click="activeTab = 'settings'"
          :class="['tab tab-lg', activeTab === 'settings' ? 'tab-active' : '']"
        >
          <Settings class="w-4 h-4 mr-2" />
          Settings
        </button>
      </div>

      <!-- Tab Content -->
      <div class="min-h-96">
        <!-- Reviews Tab -->
        <div v-if="activeTab === 'reviews'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">My Reviews ({{ userReviews.length }})</h2>
            <router-link to="/write-review" class="btn btn-primary">
              <Plus class="w-4 h-4 mr-2" />
              Write New Review
            </router-link>
          </div>
          
          <div v-if="userReviews.length > 0" class="space-y-6">
            <div 
              v-for="review in userReviews" 
              :key="review.id"
              class="card bg-white shadow-lg hover:shadow-xl transition-shadow duration-200"
            >
              <div class="card-body">
                <div class="flex justify-between items-start mb-4">
                  <div class="flex-1">
                    <h3 class="card-title text-xl mb-2">{{ review.title }}</h3>
                    <div class="flex items-center gap-4 mb-2">
                      <router-link 
                        :to="`/movie/${review.movieId}`" 
                        class="text-primary hover:underline font-semibold"
                      >
                        {{ getMovieTitle(review.movieId) }}
                      </router-link>
                      <LemonPieRating :rating="review.rating" size="sm" />
                    </div>
                    <div class="text-sm text-gray-500 mb-3">
                      {{ formatDate(review.date) }}
                    </div>
                  </div>
                  <div class="dropdown dropdown-end">
                    <label tabindex="0" class="btn btn-ghost btn-sm">
                      <MoreVertical class="w-4 h-4" />
                    </label>
                    <ul tabindex="0" class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
                      <li><a @click="editReview(review)"><Edit class="w-4 h-4" />Edit</a></li>
                      <li><a @click="deleteReview(review.id)" class="text-error"><Trash2 class="w-4 h-4" />Delete</a></li>
                    </ul>
                  </div>
                </div>
                
                <p class="text-gray-700 mb-4">{{ review.content }}</p>
                
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-4 text-sm text-gray-500">
                    <span class="flex items-center gap-1">
                      <ThumbsUp class="w-4 h-4" />
                      {{ review.likes }}
                    </span>
                    <span class="flex items-center gap-1">
                      <ThumbsDown class="w-4 h-4" />
                      {{ review.dislikes }}
                    </span>
                    <span v-if="review.containsSpoilers" class="badge badge-warning badge-sm">
                      Contains Spoilers
                    </span>
                  </div>
                  <router-link 
                    :to="`/movie/${review.movieId}`" 
                    class="btn btn-outline btn-sm"
                  >
                    View Movie
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-16">
            <div class="text-6xl mb-4">📝</div>
            <h3 class="text-2xl font-bold text-gray-700 mb-2">No reviews yet</h3>
            <p class="text-gray-500 mb-6">Start sharing your thoughts on Nollywood movies!</p>
            <router-link to="/write-review" class="btn btn-primary">
              Write Your First Review
            </router-link>
          </div>
        </div>

        <!-- Watchlist Tab -->
        <div v-if="activeTab === 'watchlist'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">My Watchlist ({{ watchlist.length }})</h2>
            <router-link to="/browse" class="btn btn-primary">
              <Plus class="w-4 h-4 mr-2" />
              Add Movies
            </router-link>
          </div>
          
          <div v-if="watchlist.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div 
              v-for="movie in watchlist" 
              :key="movie.id"
              class="card bg-white shadow-lg hover:shadow-xl transition-shadow duration-200"
            >
              <figure class="relative">
                <img :src="movie.poster" :alt="movie.title" class="w-full h-64 object-cover" />
                <button 
                  @click="removeFromWatchlist(movie.id)"
                  class="btn btn-circle btn-sm btn-error absolute top-2 right-2"
                >
                  <X class="w-4 h-4" />
                </button>
              </figure>
              <div class="card-body p-4">
                <h3 class="card-title text-lg">{{ movie.title }}</h3>
                <p class="text-sm text-gray-600">{{ movie.year }} • {{ movie.genre }}</p>
                <div class="card-actions justify-end mt-4">
                  <router-link :to="`/movie/${movie.id}`" class="btn btn-primary btn-sm">
                    View Details
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-16">
            <div class="text-6xl mb-4">🎬</div>
            <h3 class="text-2xl font-bold text-gray-700 mb-2">Your watchlist is empty</h3>
            <p class="text-gray-500 mb-6">Add movies you want to watch later!</p>
            <router-link to="/browse" class="btn btn-primary">
              Browse Movies
            </router-link>
          </div>
        </div>

        <!-- Favorites Tab -->
        <div v-if="activeTab === 'favorites'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">My Favorites ({{ favorites.length }})</h2>
          </div>
          
          <div v-if="favorites.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <MovieCard 
              v-for="movie in favorites" 
              :key="movie.id" 
              :movie="movie"
              class="transform hover:scale-105 transition-transform duration-200"
            />
          </div>
          
          <div v-else class="text-center py-16">
            <div class="text-6xl mb-4">❤️</div>
            <h3 class="text-2xl font-bold text-gray-700 mb-2">No favorites yet</h3>
            <p class="text-gray-500 mb-6">Mark movies as favorites to see them here!</p>
            <router-link to="/browse" class="btn btn-primary">
              Discover Movies
            </router-link>
          </div>
        </div>

        <!-- Settings Tab -->
        <div v-if="activeTab === 'settings'">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Account Settings</h2>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Profile Settings -->
            <div class="card bg-white shadow-lg">
              <div class="card-body">
                <h3 class="card-title mb-4">Profile Information</h3>
                <form @submit.prevent="updateProfile">
                  <div class="form-control mb-4">
                    <label class="label">
                      <span class="label-text">Display Name</span>
                    </label>
                    <input 
                      v-model="profileForm.name" 
                      type="text" 
                      class="input input-bordered" 
                      required
                    />
                  </div>
                  
                  <div class="form-control mb-4">
                    <label class="label">
                      <span class="label-text">Bio</span>
                    </label>
                    <textarea 
                      v-model="profileForm.bio" 
                      class="textarea textarea-bordered" 
                      placeholder="Tell us about yourself..."
                    ></textarea>
                  </div>
                  
                  <div class="form-control mb-4">
                    <label class="label">
                      <span class="label-text">Location</span>
                    </label>
                    <input 
                      v-model="profileForm.location" 
                      type="text" 
                      class="input input-bordered" 
                      placeholder="e.g., Lagos, Nigeria"
                    />
                  </div>
                  
                  <button type="submit" class="btn btn-primary">
                    Update Profile
                  </button>
                </form>
              </div>
            </div>
            
            <!-- Preferences -->
            <div class="card bg-white shadow-lg">
              <div class="card-body">
                <h3 class="card-title mb-4">Preferences</h3>
                
                <div class="form-control mb-4">
                  <label class="cursor-pointer label">
                    <span class="label-text">Email Notifications</span>
                    <input v-model="preferences.emailNotifications" type="checkbox" class="toggle toggle-primary" />
                  </label>
                </div>
                
                <div class="form-control mb-4">
                  <label class="cursor-pointer label">
                    <span class="label-text">Show Profile Publicly</span>
                    <input v-model="preferences.publicProfile" type="checkbox" class="toggle toggle-primary" />
                  </label>
                </div>
                
                <div class="form-control mb-4">
                  <label class="label">
                    <span class="label-text">Preferred Language</span>
                  </label>
                  <select v-model="preferences.language" class="select select-bordered">
                    <option value="en">English</option>
                    <option value="yo">Yoruba</option>
                    <option value="ig">Igbo</option>
                    <option value="ha">Hausa</option>
                  </select>
                </div>
                
                <button @click="updatePreferences" class="btn btn-primary">
                  Save Preferences
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Additional custom styles if needed */
</style>