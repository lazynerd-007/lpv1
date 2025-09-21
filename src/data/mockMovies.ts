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
  type?: 'movie' | 'series';
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
  type?: 'movie' | 'series';
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
    cast: ['Adesua Etomi as Deirdre', 'Banky Wellington as Nonso', 'Richard Mofe-Damijo as Chief Felix', 'Sola Sobowale as Mrs. Onwuka'],
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
    cast: ['Sola Sobowale as Alhaja Eniola Salami', 'Adesua Etomi as Kemi Salami', 'Reminisce as Makanaki', 'Jide Kosoko as Alhaji Salami'],
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
    cast: ['AY Makun as Ayo Alesinloye', 'Falz as Remi Martins', 'Jim Iyke as Amaju Abioritsegbemi', 'Ramsey Nouah as Anieto Obi'],
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
    cast: ['Bisola Aiyeola as Sola', 'Adesua Etomi as Susie', 'Bimbo Ademoye as Sugar', 'Williams Uchemba as TC'],
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
    cast: ['Ramsey Nouah as Richard Williams', 'Kanayo O. Kanayo as Chief Omego', 'Enyinna Nwigwe as Nnamdi Okeke', 'Nancy Isime as Nnamdi\'s Wife'],
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
  },
  {
    id: '6',
    title: 'Citation',
    releaseDate: '2020-11-06',
    runtime: 151,
    genre: ['Drama', 'Thriller'],
    language: ['English', 'Yoruba'],
    director: 'Kunle Afolayan',
    producer: 'Kunle Afolayan',
    cast: ['Temi Otedola', 'Jimmy Jean-Louis', 'Joke Silva', 'Sadiq Daba'],
    plotSummary: 'A bright student in Nigeria takes on the academic establishment when she reports a popular professor who tried to rape her.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20university%20drama%20movie%20poster%20serious%20academic%20setting%20young%20woman%20protagonist&image_size=portrait_4_3',
    productionCompany: 'Golden Effects Pictures',
    filmingLocations: ['Lagos', 'Cape Coast'],
    productionState: 'Lagos',
    boxOfficeNG: '₦89 million',
    streamingPlatforms: ['Netflix'],
    awards: ['AMAA Best Film'],
    lemonPieRating: 8.9,
    userRating: 9.1,
    criticRating: 8.7,
    reviewCount: 1456
  },
  {
    id: '7',
    title: 'Elevator Baby',
    releaseDate: '2019-09-13',
    runtime: 92,
    genre: ['Comedy', 'Drama'],
    language: ['English'],
    director: 'Akay Mason',
    producer: 'Niyi Akinmolayan',
    cast: ['Timini Egbuson', 'Toyin Abraham', 'Bimbo Ademoye', 'Broda Shaggi'],
    plotSummary: 'A chance encounter in a broken elevator between a pregnant woman and a young man leads to an unexpected friendship.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20comedy%20drama%20elevator%20setting%20pregnant%20woman%20young%20man%20heartwarming&image_size=portrait_4_3',
    productionCompany: 'Anthill Studios',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦67 million',
    streamingPlatforms: ['Netflix', 'Prime Video'],
    awards: [],
    lemonPieRating: 7.4,
    userRating: 7.8,
    criticRating: 7.1,
    reviewCount: 743
  },
  {
    id: '8',
    title: 'The Set Up',
    releaseDate: '2019-08-09',
    runtime: 90,
    genre: ['Action', 'Crime', 'Thriller'],
    language: ['English'],
    director: 'Niyi Akinmolayan',
    producer: 'Niyi Akinmolayan',
    cast: ['Adesua Etomi', 'Jim Iyke', 'Tina Mba', 'Kehinde Bankole'],
    plotSummary: 'A young woman gets more than she bargains for and is drawn into a web of deceit when she is hired by a socialite to assist with his scheme to marry a wealthy heiress.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20crime%20thriller%20movie%20poster%20dark%20urban%20setting%20deception%20mystery&image_size=portrait_4_3',
    productionCompany: 'Anthill Studios',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦54 million',
    streamingPlatforms: ['Netflix'],
    awards: [],
    lemonPieRating: 6.9,
    userRating: 7.3,
    criticRating: 6.5,
    reviewCount: 892
  },
  {
    id: '9',
    title: 'Omo Ghetto: The Saga',
    releaseDate: '2020-12-25',
    runtime: 110,
    genre: ['Comedy', 'Drama'],
    language: ['English', 'Yoruba'],
    director: 'Funke Akindele',
    producer: 'Funke Akindele',
    cast: ['Funke Akindele', 'Chioma Akpotha', 'Eniola Badmus', 'Bimbo Thomas'],
    plotSummary: 'Lefty, a notorious area girl, returns to her ghetto roots after discovering her true identity and must navigate between two worlds.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20comedy%20drama%20ghetto%20setting%20vibrant%20street%20life%20colorful%20characters&image_size=portrait_4_3',
    productionCompany: 'Scene One Productions',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦636 million',
    streamingPlatforms: ['Netflix'],
    awards: ['AMVCA Best Comedy'],
    lemonPieRating: 7.8,
    userRating: 8.2,
    criticRating: 7.5,
    reviewCount: 2134
  },
  {
    id: '10',
    title: 'Chief Daddy',
    releaseDate: '2018-12-14',
    runtime: 100,
    genre: ['Comedy', 'Drama'],
    language: ['English'],
    director: 'Niyi Akinmolayan',
    producer: 'Mo Abudu',
    cast: ['Funke Akindele', 'Joke Silva', 'Kate Henshaw', 'RMD'],
    plotSummary: 'The story of billionaire industrialist Chief Beecroft, a flamboyant benefactor to a large extended family of relatives, household staff and assorted mistresses.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20wealthy%20family%20comedy%20drama%20luxurious%20mansion%20ensemble%20cast&image_size=portrait_4_3',
    productionCompany: 'EbonyLife Films',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦387 million',
    streamingPlatforms: ['Netflix'],
    awards: [],
    lemonPieRating: 7.2,
    userRating: 7.6,
    criticRating: 6.8,
    reviewCount: 1567
  },
  {
    id: '11',
    title: 'Namaste Wahala',
    releaseDate: '2021-02-14',
    runtime: 108,
    genre: ['Romance', 'Comedy', 'Drama'],
    language: ['English', 'Hindi'],
    director: 'Hamisha Daryani Ahuja',
    producer: 'Hamisha Daryani Ahuja',
    cast: ['Ini Dima-Okojie', 'Ruslaan Mumtaz', 'Richard Mofe-Damijo', 'Joke Silva'],
    plotSummary: 'A Nigerian woman and an Indian man fall in love but struggle with cultural differences and family expectations.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20Indian%20cross%20cultural%20romance%20movie%20poster%20colorful%20traditional%20elements&image_size=portrait_4_3',
    productionCompany: 'Inkblot Productions',
    filmingLocations: ['Lagos', 'Mumbai'],
    productionState: 'Lagos',
    boxOfficeNG: '₦123 million',
    streamingPlatforms: ['Netflix'],
    awards: [],
    lemonPieRating: 6.8,
    userRating: 7.4,
    criticRating: 6.2,
    reviewCount: 934
  },
  {
    id: '12',
    title: 'Rattlesnake: The Ahanna Story',
    releaseDate: '2020-11-13',
    runtime: 104,
    genre: ['Crime', 'Drama', 'Thriller'],
    language: ['English', 'Igbo'],
    director: 'Ramsey Nouah',
    producer: 'Charles Okpaleke',
    cast: ['Stan Nze', 'Osas Ighodaro', 'Bucci Franklin', 'Emeka Nwagbaraocha'],
    plotSummary: 'Ahanna, a young man from the slums, becomes entangled in the world of crime and must fight to survive.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20crime%20thriller%20urban%20slums%20young%20man%20dangerous%20underworld&image_size=portrait_4_3',
    productionCompany: 'Play Network Studios',
    filmingLocations: ['Lagos', 'Onitsha'],
    productionState: 'Lagos',
    boxOfficeNG: '₦78 million',
    streamingPlatforms: ['Netflix'],
    awards: [],
    lemonPieRating: 7.1,
    userRating: 7.5,
    criticRating: 6.8,
    reviewCount: 1123
  },
  {
    id: '13',
    title: 'My Village People',
    releaseDate: '2021-06-11',
    runtime: 105,
    genre: ['Comedy', 'Fantasy'],
    language: ['English', 'Igbo'],
    director: 'Niyi Akinmolayan',
    producer: 'Funke Akindele',
    cast: ['Bovi Ugboma', 'Venita Akpofure', 'Amaechi Muonagor', 'Sophie Alakija'],
    plotSummary: 'A young man discovers his village people are plotting against his success in the city.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20comedy%20fantasy%20village%20people%20supernatural%20elements%20colorful&image_size=portrait_4_3',
    productionCompany: 'Anthill Studios',
    filmingLocations: ['Lagos', 'Enugu'],
    productionState: 'Lagos',
    boxOfficeNG: '₦45 million',
    streamingPlatforms: ['Prime Video'],
    awards: [],
    lemonPieRating: 2.8,
    userRating: 3.2,
    criticRating: 2.5,
    reviewCount: 423
  },
  {
    id: '14',
    title: 'Crazy People',
    releaseDate: '2018-03-16',
    runtime: 98,
    genre: ['Comedy'],
    language: ['English'],
    director: 'Biodun Stephen',
    producer: 'Biodun Stephen',
    cast: ['Alex Ekubo', 'Jim Iyke', 'Yvonne Jegede', 'IK Ogbonna'],
    plotSummary: 'Four friends embark on a chaotic adventure that tests their friendship.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20comedy%20four%20friends%20chaotic%20adventure%20bright%20colors&image_size=portrait_4_3',
    productionCompany: 'Biodun Stephen Productions',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦32 million',
    streamingPlatforms: ['IROKOtv'],
    awards: [],
    lemonPieRating: 3.1,
    userRating: 3.8,
    criticRating: 2.9,
    reviewCount: 312
  },
  {
    id: '15',
    title: 'Banana Island Ghost',
    releaseDate: '2017-08-04',
    runtime: 103,
    genre: ['Comedy', 'Romance', 'Fantasy'],
    language: ['English'],
    director: 'BB Sasore',
    producer: 'Biola Alabi',
    cast: ['Chigul', 'Patrick Diabuah', 'Akah Nnani', 'Saidi Balogun'],
    plotSummary: 'A ghost returns to earth to win back his girlfriend before moving on to the afterlife.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20ghost%20comedy%20romance%20supernatural%20Lagos%20island&image_size=portrait_4_3',
    productionCompany: 'Nemsia Films',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦28 million',
    streamingPlatforms: ['Netflix'],
    awards: [],
    lemonPieRating: 3.7,
    userRating: 4.2,
    criticRating: 3.4,
    reviewCount: 289
  },
  {
    id: '16',
    title: 'Isoken',
    releaseDate: '2017-06-16',
    runtime: 118,
    genre: ['Romance', 'Comedy', 'Drama'],
    language: ['English'],
    director: 'Jadesola Osiberu',
    producer: 'Jadesola Osiberu',
    cast: ['Dakore Egbuson-Akande', 'Joseph Benjamin', 'Funmi Holder', 'Tina Mba'],
    plotSummary: 'A successful woman faces pressure from family to get married before her younger sister.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20romance%20drama%20successful%20woman%20family%20pressure%20wedding&image_size=portrait_4_3',
    productionCompany: 'Greoh Studios',
    filmingLocations: ['Lagos', 'Benin City'],
    productionState: 'Lagos',
    boxOfficeNG: '₦41 million',
    streamingPlatforms: ['Netflix'],
    awards: [],
    lemonPieRating: 2.9,
    userRating: 3.5,
    criticRating: 2.7,
    reviewCount: 456
  },
  {
    id: '17',
    title: 'Hire a Man',
    releaseDate: '2017-12-15',
    runtime: 95,
    genre: ['Romance', 'Comedy'],
    language: ['English'],
    director: 'Niyi Akinmolayan',
    producer: 'Niyi Akinmolayan',
    cast: ['Nancy Isime', 'Alexx Ekubo', 'Bayray McNwizu', 'Mofe Duncan'],
    plotSummary: 'A woman hires a fake boyfriend to impress her family during the holidays.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20romantic%20comedy%20fake%20boyfriend%20family%20holidays%20festive&image_size=portrait_4_3',
    productionCompany: 'Anthill Studios',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦23 million',
    streamingPlatforms: ['IROKOtv'],
    awards: [],
    lemonPieRating: 3.4,
    userRating: 4.0,
    criticRating: 3.1,
    reviewCount: 234
  },
  {
    id: '18',
    title: 'Slow Country',
    releaseDate: '2022-09-23',
    runtime: 87,
    genre: ['Drama', 'Thriller'],
    language: ['English'],
    director: 'Biodun Stephen',
    producer: 'Biodun Stephen',
    cast: ['Tana Adelana', 'Kemi Lala Akindoju', 'Deyemi Okanlawon', 'Adunni Ade'],
    plotSummary: 'A woman returns to her hometown and uncovers dark secrets about her family.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20drama%20thriller%20small%20town%20dark%20secrets%20mysterious&image_size=portrait_4_3',
    productionCompany: 'Biodun Stephen Productions',
    filmingLocations: ['Ogun State'],
    productionState: 'Ogun',
    boxOfficeNG: '₦19 million',
    streamingPlatforms: ['Prime Video'],
    awards: [],
    lemonPieRating: 2.1,
    userRating: 2.8,
    criticRating: 1.9,
    reviewCount: 167
  },
  {
    id: '19',
    title: 'Bad Comments',
    releaseDate: '2021-11-05',
    runtime: 92,
    genre: ['Comedy', 'Drama'],
    language: ['English', 'Yoruba'],
    director: 'Ishaya Bako',
    producer: 'Ishaya Bako',
    cast: ['Timini Egbuson', 'Bimbo Ademoye', 'Toyin Abraham', 'Broda Shaggi'],
    plotSummary: 'A social media influencer faces backlash when old controversial posts resurface.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20social%20media%20influencer%20controversy%20phone%20screen%20drama&image_size=portrait_4_3',
    productionCompany: 'Bako Studios',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦15 million',
    streamingPlatforms: ['YouTube'],
    awards: [],
    lemonPieRating: 1.8,
    userRating: 2.3,
    criticRating: 1.5,
    reviewCount: 298
  },
  {
    id: '20',
    title: 'Village Headmaster Returns',
    releaseDate: '2020-08-14',
    runtime: 110,
    genre: ['Drama', 'Comedy'],
    language: ['English', 'Yoruba'],
    director: 'Tade Ogidan',
    producer: 'Tade Ogidan',
    cast: ['Jide Kosoko', 'Joke Silva', 'Olu Jacobs', 'Sola Sobowale'],
    plotSummary: 'A modern remake of the classic TV series fails to capture the original magic.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20village%20headmaster%20traditional%20setting%20disappointing%20remake&image_size=portrait_4_3',
    productionCompany: 'OGD Pictures',
    filmingLocations: ['Oyo State'],
    productionState: 'Oyo',
    boxOfficeNG: '₦12 million',
    streamingPlatforms: ['Africa Magic'],
    awards: [],
    lemonPieRating: 2.4,
    userRating: 2.9,
    criticRating: 2.1,
    reviewCount: 445
  },
  {
    id: '21',
    title: 'Lagos Traffic',
    releaseDate: '2019-12-20',
    runtime: 88,
    genre: ['Comedy'],
    language: ['English', 'Pidgin'],
    director: 'Kunle Afolayan',
    producer: 'Kunle Afolayan',
    cast: ['Ramsey Nouah', 'Rita Dominic', 'Chidi Mokeme', 'Genevieve Nnaji'],
    plotSummary: 'Multiple storylines intersect during a massive Lagos traffic jam, but the execution is chaotic.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Lagos%20traffic%20jam%20multiple%20cars%20chaotic%20Nigerian%20city&image_size=portrait_4_3',
    productionCompany: 'Golden Effects Pictures',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦18 million',
    streamingPlatforms: ['Netflix'],
    awards: [],
    lemonPieRating: 3.3,
    userRating: 3.7,
    criticRating: 3.0,
    reviewCount: 523
  },
  {
    id: '22',
    title: 'Fake Pastor',
    releaseDate: '2022-04-08',
    runtime: 95,
    genre: ['Drama', 'Thriller'],
    language: ['English'],
    director: 'Moses Inwang',
    producer: 'Moses Inwang',
    cast: ['Majid Michel', 'Yvonne Nelson', 'John Dumelo', 'Nadia Buari'],
    plotSummary: 'A con artist poses as a pastor to exploit a congregation, but the story lacks depth.',
    posterUrl: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20fake%20pastor%20church%20con%20artist%20religious%20drama&image_size=portrait_4_3',
    productionCompany: 'Royal Arts Academy',
    filmingLocations: ['Accra', 'Lagos'],
    productionState: 'Lagos',
    boxOfficeNG: '₦21 million',
    streamingPlatforms: ['IROKOtv'],
    awards: [],
    lemonPieRating: 2.6,
    userRating: 3.1,
    criticRating: 2.3,
    reviewCount: 367
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
export const getTrendingMovies = () => mockMovies.sort((a, b) => b.reviewCount - a.reviewCount).slice(0, 6);
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