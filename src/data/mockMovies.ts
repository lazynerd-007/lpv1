export interface Movie {
  id: string;
  title: string;
  localTitle?: string;
  releaseDate: string;
  year?: number;
  runtime: number;
  genre: string[];
  language: string[];
  director: string;
  producer: string;
  cast: string[];
  plotSummary: string;
  posterUrl: string;
  poster?: string;
  trailerUrl?: string;
  productionCompany: string;
  filmingLocations: string[];
  productionState: string;
  boxOfficeNG?: string;
  streamingPlatforms: string[];
  awards: string[];
  lemonPieRating: number;
  userRating: number;
  criticRating: number;
  reviewCount: number;
}

export interface TVShow {
  id: string;
  title: string;
  localTitle?: string;
  releaseDate: string;
  seasons: number;
  episodes: number;
  genre: string[];
  language: string[];
  creator: string;
  producer: string;
  cast: string[];
  plotSummary: string;
  posterUrl: string;
  trailerUrl?: string;
  productionCompany: string;
  filmingLocations: string[];
  productionState: string;
  streamingPlatforms: string[];
  awards: string[];
  lemonPieRating: number;
  userRating: number;
  criticRating: number;
  reviewCount: number;
  status: 'ongoing' | 'completed' | 'cancelled';
}

export interface Review {
  id: string;
  userId: string;
  movieId: string;
  userName: string;
  userAvatar: string;
  lemonPieRating: number;
  reviewText: string;
  reviewLanguage: string;
  spoilerWarning: boolean;
  culturalAuthenticityRating: number;
  productionQualityRating: number;
  nollywoodTags: string[];
  helpfulnessScore: number;
  createdAt: string;
  isVerifiedCritic: boolean;
}

export const mockMovies: Movie[] = [
  {
    id: '1',
    title: 'The Wedding Party 2',
    localTitle: 'Ọgbakọ Igbeyawo 2',
    releaseDate: '2017-12-15',
    runtime: 98,
    genre: ['Comedy', 'Romance'],
    language: ['English', 'Yoruba'],
    director: 'Niyi Akinmolayan',
    producer: 'Mo Abudu',
    cast: ['Adesua Etomi', 'Banky Wellington', 'RMD', 'Sola Sobowale'],
    plotSummary: 'Nonso continues his romance with Deirdre, the bridesmaid from London. While on a dinner date, Nonso proposes to Deirdre by accident and sets off a chain of events too powerful to stop.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20wedding%20comedy%20movie%20poster%20with%20elegant%20couple%20in%20traditional%20attire%20vibrant%20colors&image_size=portrait_4_3',
    trailerUrl: 'https://youtube.com/watch?v=example1',
    productionCompany: 'EbonyLife Films',
    filmingLocations: ['Lagos', 'London'],
    productionState: 'Lagos',
    boxOfficeNG: '₦450 million',
    streamingPlatforms: ['Netflix', 'Prime Video'],
    awards: ['AMVCA Best Comedy'],
    lemonPieRating: 8.2,
    userRating: 8.5,
    criticRating: 7.8,
    reviewCount: 1247
  },
  {
    id: '2',
    title: 'King of Boys',
    localTitle: 'Ọba Awọn Ọmọkunrin',
    releaseDate: '2018-10-26',
    runtime: 170,
    genre: ['Crime', 'Drama', 'Thriller'],
    language: ['English', 'Yoruba'],
    director: 'Kemi Adetiba',
    producer: 'Kemi Adetiba',
    cast: ['Sola Sobowale', 'Adesua Etomi', 'Reminisce', 'Jide Kosoko'],
    plotSummary: 'A businesswoman who doubles as a crime boss must choose between her family and her empire when her political ambitions are threatened.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Powerful%20Nigerian%20woman%20crime%20boss%20movie%20poster%20dark%20dramatic%20lighting%20urban%20Lagos%20backdrop&image_size=portrait_4_3',
    productionCompany: 'Kemi Adetiba Visuals',
    filmingLocations: ['Lagos', 'Ibadan'],
    productionState: 'Lagos',
    boxOfficeNG: '₦245 million',
    streamingPlatforms: ['Netflix'],
    awards: ['AMVCA Best Director', 'AMAA Best Actress'],
    lemonPieRating: 9.1,
    userRating: 9.3,
    criticRating: 8.9,
    reviewCount: 2156
  },
  {
    id: '3',
    title: 'Merry Men',
    releaseDate: '2018-09-28',
    runtime: 106,
    genre: ['Action', 'Comedy'],
    language: ['English'],
    director: 'Toka McBaror',
    producer: 'AY Makun',
    cast: ['AY Makun', 'Falz', 'Jim Iyke', 'Ramsey Nouah'],
    plotSummary: 'Four men have stopped robbing the rich to give to the poor and now are focusing on running their businesses.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Four%20Nigerian%20men%20action%20comedy%20movie%20poster%20modern%20Lagos%20skyline%20stylish%20suits&image_size=portrait_4_3',
    productionCompany: 'AY.COM',
    filmingLocations: ['Lagos', 'Abuja'],
    productionState: 'Lagos',
    boxOfficeNG: '₦180 million',
    streamingPlatforms: ['Netflix', 'IROKOtv'],
    awards: [],
    lemonPieRating: 6.8,
    userRating: 7.2,
    criticRating: 6.4,
    reviewCount: 892
  },
  {
    id: '4',
    title: 'Sugar Rush',
    releaseDate: '2019-12-25',
    runtime: 119,
    genre: ['Comedy', 'Crime'],
    language: ['English'],
    director: 'Kayode Kasum',
    producer: 'Jade Osiberu',
    cast: ['Bisola Aiyeola', 'Adesua Etomi', 'Bimbo Ademoye', 'Williams Uchemba'],
    plotSummary: 'Three sisters accidentally discover a huge sum of money and must evade dangerous criminals who want it back.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Three%20Nigerian%20sisters%20comedy%20crime%20movie%20poster%20colorful%20money%20bags%20Lagos%20setting&image_size=portrait_4_3',
    productionCompany: 'Greoh Studios',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦175 million',
    streamingPlatforms: ['Prime Video'],
    awards: [],
    lemonPieRating: 3.2,
    userRating: 4.1,
    criticRating: 2.8,
    reviewCount: 567
  },
  {
    id: '5',
    title: 'Living in Bondage: Breaking Free',
    releaseDate: '2019-11-08',
    runtime: 111,
    genre: ['Drama', 'Thriller'],
    language: ['English', 'Igbo'],
    director: 'Ramsey Nouah',
    producer: 'Steve Gukas',
    cast: ['Ramsey Nouah', 'Kanayo O. Kanayo', 'Enyinna Nwigwe', 'Nancy Isime'],
    plotSummary: 'The sequel to the classic Nollywood film follows Nnamdi, son of Andy Okeke, as he searches for the truth about his father\'s mysterious past.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20thriller%20drama%20movie%20poster%20mystical%20dark%20atmosphere%20traditional%20meets%20modern&image_size=portrait_4_3',
    productionCompany: 'Filmtrique Productions',
    filmingLocations: ['Lagos', 'Enugu'],
    productionState: 'Lagos',
    boxOfficeNG: '₦143 million',
    streamingPlatforms: ['Netflix'],
    awards: ['AMVCA Best Director'],
    lemonPieRating: 8.7,
    userRating: 8.9,
    criticRating: 8.5,
    reviewCount: 1834
  }
];

export const mockReviews: Review[] = [
  {
    id: '1',
    userId: '1',
    movieId: '2',
    userName: 'Adunni Lagos',
    userAvatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20woman%20profile%20picture%20professional%20headshot&image_size=square',
    lemonPieRating: 9,
    reviewText: 'Sola Sobowale delivered an absolutely phenomenal performance as Eniola Salami. This movie redefined what Nollywood can achieve in terms of storytelling and cinematography. The political intrigue and family dynamics were masterfully woven together.',
    reviewLanguage: 'en',
    spoilerWarning: false,
    culturalAuthenticityRating: 9,
    productionQualityRating: 9,
    nollywoodTags: ['Star Power', 'Cultural Impact', 'Political Drama'],
    helpfulnessScore: 156,
    createdAt: '2024-01-15T10:30:00Z',
    isVerifiedCritic: true
  },
  {
    id: '2',
    userId: '2',
    movieId: '1',
    userName: 'Emeka Nollywood',
    userAvatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20man%20profile%20picture%20casual%20friendly&image_size=square',
    lemonPieRating: 8,
    reviewText: 'The Wedding Party 2 maintained the charm of the original while expanding the story beautifully. The London scenes added a nice international flavor while keeping the Nigerian heart intact.',
    reviewLanguage: 'en',
    spoilerWarning: false,
    culturalAuthenticityRating: 8,
    productionQualityRating: 8,
    nollywoodTags: ['Comedy Gold', 'Romance', 'International Appeal'],
    helpfulnessScore: 89,
    createdAt: '2024-01-10T14:20:00Z',
    isVerifiedCritic: false
  },
  {
    id: '3',
    userId: '3',
    movieId: '4',
    userName: 'Kemi Reviews',
    userAvatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20woman%20profile%20picture%20critic%20glasses&image_size=square',
    lemonPieRating: 3,
    reviewText: 'Sugar Rush had potential but fell flat with predictable plot twists and inconsistent character development. The comedy felt forced and the crime elements were poorly executed. Expected much more from this cast.',
    reviewLanguage: 'en',
    spoilerWarning: true,
    culturalAuthenticityRating: 5,
    productionQualityRating: 4,
    nollywoodTags: ['Disappointing', 'Wasted Potential'],
    helpfulnessScore: 67,
    createdAt: '2024-01-08T16:45:00Z',
    isVerifiedCritic: true
  }
];

export const getMoviesByRating = (minRating: number, maxRating: number) => {
  return mockMovies.filter(movie => movie.lemonPieRating >= minRating && movie.lemonPieRating <= maxRating);
};

export const getPieMovies = () => getMoviesByRating(7, 10);
export const getLemonMovies = () => getMoviesByRating(1, 4);
export const getTrendingMovies = () => mockMovies.sort((a, b) => b.reviewCount - a.reviewCount).slice(0, 3);
export const getFeaturedMovie = () => mockMovies.find(movie => movie.id === '2'); // King of Boys as featured

export const getReviewsForMovie = (movieId: string) => {
  return mockReviews.filter(review => review.movieId === movieId);
};

export const getMovieById = (id: string) => {
  return mockMovies.find(movie => movie.id === id);
};

export const mockTVShows: TVShow[] = [
  {
    id: 'tv1',
    title: 'The Late Show with Stephen Colbert',
    releaseDate: '2015-09-08',
    seasons: 9,
    episodes: 1800,
    genre: ['Talk Show', 'Comedy'],
    language: ['English'],
    creator: 'Stephen Colbert',
    producer: 'CBS Studios',
    cast: ['Stephen Colbert', 'Jon Batiste', 'Louis Cato'],
    plotSummary: 'Stephen Colbert brings his signature satire and comedy to The Late Show as he talks with an eclectic mix of guests about the most relevant and pressing issues.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Stephen%20Colbert%20late%20night%20talk%20show%20poster%20professional%20studio%20setting&image_size=portrait_4_3',
    productionCompany: 'CBS Studios',
    filmingLocations: ['New York City'],
    productionState: 'New York',
    streamingPlatforms: ['Paramount+', 'CBS'],
    awards: ['Emmy Awards'],
    lemonPieRating: 6.5,
    userRating: 7.2,
    criticRating: 6.8,
    reviewCount: 892,
    status: 'ongoing'
  },
  {
    id: 'tv2',
    title: 'The Tonight Show Starring Jimmy Fallon',
    releaseDate: '2014-02-17',
    seasons: 11,
    episodes: 2200,
    genre: ['Talk Show', 'Comedy', 'Variety'],
    language: ['English'],
    creator: 'Jimmy Fallon',
    producer: 'NBC Studios',
    cast: ['Jimmy Fallon', 'The Roots', 'Steve Higgins'],
    plotSummary: 'Jimmy Fallon hosts the Tonight Show with celebrity interviews, musical performances, and comedy sketches.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Jimmy%20Fallon%20tonight%20show%20poster%20colorful%20studio%20entertainment&image_size=portrait_4_3',
    productionCompany: 'NBC Studios',
    filmingLocations: ['New York City'],
    productionState: 'New York',
    streamingPlatforms: ['Peacock', 'NBC'],
    awards: ['People\'s Choice Awards'],
    lemonPieRating: 5.8,
    userRating: 6.5,
    criticRating: 5.2,
    reviewCount: 1156,
    status: 'ongoing'
  },
  {
    id: 'tv3',
    title: 'Grey\'s Anatomy',
    releaseDate: '2005-03-27',
    seasons: 20,
    episodes: 420,
    genre: ['Medical Drama', 'Romance'],
    language: ['English'],
    creator: 'Shonda Rhimes',
    producer: 'ABC Studios',
    cast: ['Ellen Pompeo', 'Sandra Oh', 'Katherine Heigl', 'Patrick Dempsey'],
    plotSummary: 'A medical drama centered on the personal and professional lives of surgical interns and their supervisors.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Medical%20drama%20TV%20show%20poster%20hospital%20setting%20diverse%20cast&image_size=portrait_4_3',
    productionCompany: 'ABC Studios',
    filmingLocations: ['Seattle', 'Los Angeles'],
    productionState: 'Washington',
    streamingPlatforms: ['Netflix', 'Hulu', 'ABC'],
    awards: ['Golden Globe', 'Emmy Awards'],
    lemonPieRating: 8.2,
    userRating: 8.7,
    criticRating: 7.9,
    reviewCount: 3245,
    status: 'ongoing'
  },
  {
    id: 'tv4',
    title: 'Law & Order: Special Victims Unit',
    releaseDate: '1999-09-20',
    seasons: 25,
    episodes: 550,
    genre: ['Crime Drama', 'Police Procedural'],
    language: ['English'],
    creator: 'Dick Wolf',
    producer: 'NBC Studios',
    cast: ['Mariska Hargitay', 'Ice-T', 'Kelli Giddish', 'Peter Scanavino'],
    plotSummary: 'The dedicated detectives of the Special Victims Unit investigate sexually related crimes in New York City.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Police%20procedural%20crime%20drama%20TV%20poster%20NYC%20law%20enforcement&image_size=portrait_4_3',
    productionCompany: 'NBC Studios',
    filmingLocations: ['New York City'],
    productionState: 'New York',
    streamingPlatforms: ['Peacock', 'Hulu', 'NBC'],
    awards: ['Emmy Awards', 'SAG Awards'],
    lemonPieRating: 8.0,
    userRating: 8.3,
    criticRating: 7.8,
    reviewCount: 2890,
    status: 'ongoing'
  },
  {
    id: 'tv5',
    title: 'Watch What Happens Live with Andy Cohen',
    releaseDate: '2009-07-16',
    seasons: 21,
    episodes: 2100,
    genre: ['Talk Show', 'Entertainment'],
    language: ['English'],
    creator: 'Andy Cohen',
    producer: 'Bravo',
    cast: ['Andy Cohen'],
    plotSummary: 'Andy Cohen hosts this late-night talk show featuring celebrity guests, games, and pop culture discussions.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Andy%20Cohen%20late%20night%20talk%20show%20colorful%20studio%20entertainment&image_size=portrait_4_3',
    productionCompany: 'Bravo',
    filmingLocations: ['New York City'],
    productionState: 'New York',
    streamingPlatforms: ['Peacock', 'Bravo'],
    awards: [],
    lemonPieRating: 5.1,
    userRating: 5.8,
    criticRating: 4.9,
    reviewCount: 756,
    status: 'ongoing'
  },
  {
    id: 'tv6',
    title: 'Good Mythical Morning',
    releaseDate: '2012-01-09',
    seasons: 25,
    episodes: 2500,
    genre: ['Comedy', 'Talk Show', 'Food'],
    language: ['English'],
    creator: 'Rhett McLaughlin, Link Neal',
    producer: 'Mythical Entertainment',
    cast: ['Rhett McLaughlin', 'Link Neal'],
    plotSummary: 'Rhett and Link host this daily comedy talk show featuring taste tests, experiments, and celebrity guests.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Comedy%20morning%20show%20two%20hosts%20colorful%20studio%20food%20experiments&image_size=portrait_4_3',
    productionCompany: 'Mythical Entertainment',
    filmingLocations: ['Los Angeles'],
    productionState: 'California',
    streamingPlatforms: ['YouTube', 'YouTube TV'],
    awards: ['Streamy Awards'],
    lemonPieRating: 7.0,
    userRating: 7.8,
    criticRating: 6.5,
    reviewCount: 1234,
    status: 'ongoing'
  }
];

export const getTrendingTVShows = () => {
  return mockTVShows.sort((a, b) => b.reviewCount - a.reviewCount).slice(0, 6);
};

export const getTrendingReviews = () => {
  return mockReviews.sort((a, b) => b.helpfulnessScore - a.helpfulnessScore).slice(0, 3);
};