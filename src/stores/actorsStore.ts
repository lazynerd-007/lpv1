import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Actor {
  id: string
  name: string
  age: number
  image: string
  popularity: number
  movieCount: number
  biography?: string
  birthPlace?: string
  knownFor?: string[]
}

const mockActors: Actor[] = [
  {
    id: '1',
    name: 'Katherina LaNasa',
    age: 58,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20elegant%20blonde%20actress%20with%20short%20hair%20and%20earrings&image_size=square',
    popularity: 950000,
    movieCount: 45,
    biography: 'American actress and former ballet dancer',
    birthPlace: 'New Orleans, Louisiana',
    knownFor: ['Big Love', 'Dexter', 'The Campaign']
  },
  {
    id: '2',
    name: 'Gary Oldman',
    age: 67,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=distinguished%20older%20male%20actor%20with%20glasses%20and%20beard%20professional%20headshot&image_size=square',
    popularity: 1200000,
    movieCount: 78,
    biography: 'English actor and filmmaker',
    birthPlace: 'New Cross, London',
    knownFor: ['The Dark Knight', 'Harry Potter', 'Darkest Hour']
  },
  {
    id: '3',
    name: 'Jenna Ortega',
    age: 22,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=young%20latina%20actress%20with%20dark%20hair%20professional%20headshot%20portrait&image_size=square',
    popularity: 1800000,
    movieCount: 25,
    biography: 'American actress',
    birthPlace: 'Coachella Valley, California',
    knownFor: ['Wednesday', 'Scream', 'You']
  },
  {
    id: '4',
    name: 'Jackie Chan',
    age: 71,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=famous%20asian%20martial%20arts%20actor%20smiling%20professional%20headshot&image_size=square',
    popularity: 2100000,
    movieCount: 150,
    biography: 'Hong Kong martial artist and actor',
    birthPlace: 'Hong Kong',
    knownFor: ['Rush Hour', 'Drunken Master', 'Police Story']
  },
  {
    id: '5',
    name: 'Sae Bom',
    age: 40,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=korean%20actress%20with%20long%20dark%20hair%20elegant%20professional%20headshot&image_size=square',
    popularity: 850000,
    movieCount: 32,
    biography: 'South Korean actress',
    birthPlace: 'Seoul, South Korea',
    knownFor: ['Happiness', 'Secret Love Affair', 'Misty']
  },
  {
    id: '6',
    name: 'Frank Welker',
    age: 79,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=elderly%20male%20voice%20actor%20smiling%20professional%20headshot&image_size=square',
    popularity: 750000,
    movieCount: 200,
    biography: 'American voice actor',
    birthPlace: 'Denver, Colorado',
    knownFor: ['Scooby-Doo', 'Transformers', 'Garfield']
  },
  {
    id: '7',
    name: 'Kim Ji-ah',
    age: 27,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=young%20korean%20actress%20with%20colorful%20hair%20modern%20professional%20headshot&image_size=square',
    popularity: 920000,
    movieCount: 18,
    biography: 'South Korean actress and model',
    birthPlace: 'Busan, South Korea',
    knownFor: ['The Kingdom', 'Sweet Home', 'My Name']
  },
  {
    id: '8',
    name: 'Dolph Lundgren',
    age: 67,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=muscular%20blonde%20action%20actor%20professional%20headshot%20portrait&image_size=square',
    popularity: 680000,
    movieCount: 65,
    biography: 'Swedish actor and martial artist',
    birthPlace: 'Spånga, Sweden',
    knownFor: ['Rocky IV', 'The Expendables', 'Universal Soldier']
  },
  {
    id: '9',
    name: 'Jesse Williams',
    age: 43,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=handsome%20african%20american%20actor%20with%20beard%20professional%20headshot&image_size=square',
    popularity: 1100000,
    movieCount: 28,
    biography: 'American actor and activist',
    birthPlace: 'Chicago, Illinois',
    knownFor: ["Grey's Anatomy", 'The Butler', 'Detroit']
  },
  {
    id: '10',
    name: 'Kazuhiko Inoue',
    age: 71,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=japanese%20voice%20actor%20elderly%20man%20professional%20headshot&image_size=square',
    popularity: 580000,
    movieCount: 180,
    biography: 'Japanese voice actor',
    birthPlace: 'Yokohama, Japan',
    knownFor: ['Naruto', 'JoJo\'s Bizarre Adventure', 'Captain Tsubasa']
  },
  {
    id: '11',
    name: 'Kandi Burruss',
    age: 49,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=african%20american%20singer%20actress%20with%20glamorous%20makeup%20professional%20headshot&image_size=square',
    popularity: 720000,
    movieCount: 15,
    biography: 'American singer and actress',
    birthPlace: 'College Park, Georgia',
    knownFor: ['Real Housewives of Atlanta', 'Xscape', 'The Chi']
  },
  {
    id: '12',
    name: 'All the Old Knives',
    age: 35,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=mysterious%20ensemble%20cast%20thriller%20movie%20poster%20style%20portrait&image_size=square',
    popularity: 450000,
    movieCount: 8,
    biography: 'Ensemble cast from thriller film',
    birthPlace: 'Various',
    knownFor: ['All the Old Knives', 'Spy Thriller Genre']
  }
]

// Additional actors for pagination
const additionalActors: Actor[] = [
  {
    id: '13',
    name: 'Lupita Nyong\'o',
    age: 41,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=elegant%20african%20actress%20with%20short%20hair%20professional%20headshot&image_size=square',
    popularity: 1300000,
    movieCount: 22,
    biography: 'Kenyan-Mexican actress',
    birthPlace: 'Mexico City, Mexico',
    knownFor: ['12 Years a Slave', 'Black Panther', 'Us']
  },
  {
    id: '14',
    name: 'Michael B. Jordan',
    age: 38,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=handsome%20african%20american%20actor%20athletic%20build%20professional%20headshot&image_size=square',
    popularity: 1600000,
    movieCount: 35,
    biography: 'American actor and producer',
    birthPlace: 'Santa Ana, California',
    knownFor: ['Black Panther', 'Creed', 'Fruitvale Station']
  },
  {
    id: '15',
    name: 'Zendaya',
    age: 28,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=young%20mixed%20race%20actress%20with%20curly%20hair%20professional%20headshot&image_size=square',
    popularity: 2200000,
    movieCount: 20,
    biography: 'American actress and singer',
    birthPlace: 'Oakland, California',
    knownFor: ['Spider-Man', 'Euphoria', 'Dune']
  },
  {
    id: '16',
    name: 'Ryan Gosling',
    age: 44,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=blonde%20male%20actor%20with%20blue%20eyes%20professional%20headshot&image_size=square',
    popularity: 1400000,
    movieCount: 42,
    biography: 'Canadian actor',
    birthPlace: 'London, Ontario',
    knownFor: ['La La Land', 'Blade Runner 2049', 'The Notebook']
  }
]

export const useActorsStore = defineStore('actors', () => {
  const actors = ref<Actor[]>([])
  const currentPage = ref(0)
  const itemsPerPage = 12
  const totalActors = mockActors.length + additionalActors.length

  const loadInitialActors = () => {
    actors.value = mockActors.slice(0, itemsPerPage)
    currentPage.value = 1
  }

  const loadMoreActors = async (): Promise<boolean> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const startIndex = currentPage.value * itemsPerPage
    const endIndex = startIndex + itemsPerPage
    
    const allActors = [...mockActors, ...additionalActors]
    const newActors = allActors.slice(startIndex, endIndex)
    
    if (newActors.length > 0) {
      actors.value.push(...newActors)
      currentPage.value++
      return true
    }
    
    return false
  }

  const getActorById = (id: string): Actor | undefined => {
    return actors.value.find(actor => actor.id === id)
  }

  const searchActors = (query: string): Actor[] => {
    if (!query.trim()) return actors.value
    
    const lowercaseQuery = query.toLowerCase()
    return actors.value.filter(actor => 
      actor.name.toLowerCase().includes(lowercaseQuery) ||
      actor.knownFor?.some(work => work.toLowerCase().includes(lowercaseQuery))
    )
  }

  return {
    actors,
    currentPage,
    totalActors,
    loadInitialActors,
    loadMoreActors,
    getActorById,
    searchActors
  }
})