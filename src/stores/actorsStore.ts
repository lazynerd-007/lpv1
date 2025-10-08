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
  // Nigerian Nollywood Actors
  {
    id: 'nig-1',
    name: 'Adesua Etomi',
    age: 36,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=beautiful%20nigerian%20actress%20adesua%20etomi%20professional%20headshot%20elegant%20smile&image_size=square',
    popularity: 1800000,
    movieCount: 25,
    biography: 'Nigerian actress and model known for her versatile roles in Nollywood films. She has won multiple awards including the Africa Magic Viewers Choice Award for Best Actress.',
    birthPlace: 'Owerri, Imo State, Nigeria',
    knownFor: ['The Wedding Party', 'King of Boys', 'Sugar Rush']
  },
  {
    id: 'nig-2',
    name: 'Banky Wellington',
    age: 43,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=handsome%20nigerian%20actor%20banky%20wellington%20professional%20headshot%20charming%20smile&image_size=square',
    popularity: 1600000,
    movieCount: 18,
    biography: 'Nigerian-American singer, rapper, actor, and politician. Known for his music career and transition into acting with notable Nollywood performances.',
    birthPlace: 'New York, USA (Nigerian parents)',
    knownFor: ['The Wedding Party', 'Up North', 'Sugar Rush']
  },
  {
    id: 'nig-3',
    name: 'Richard Mofe-Damijo',
    age: 62,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=distinguished%20nigerian%20actor%20richard%20mofe%20damijo%20professional%20headshot%20gray%20beard&image_size=square',
    popularity: 2200000,
    movieCount: 85,
    biography: 'Veteran Nigerian actor, writer, producer, and lawyer. One of the most respected figures in Nollywood with a career spanning over three decades.',
    birthPlace: 'Aladja, Delta State, Nigeria',
    knownFor: ['The Wedding Party', 'Dinner', 'Diamond Ring']
  },
  {
    id: 'nig-4',
    name: 'Sola Sobowale',
    age: 59,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=powerful%20nigerian%20actress%20sola%20sobowale%20professional%20headshot%20regal%20expression&image_size=square',
    popularity: 2000000,
    movieCount: 65,
    biography: 'Veteran Nigerian actress known for her powerful performances and commanding screen presence. She has become an icon in Nollywood cinema.',
    birthPlace: 'Ondo State, Nigeria',
    knownFor: ['King of Boys', 'The Wedding Party', 'Ohun Oko Mi']
  },
  {
    id: 'nig-5',
    name: 'Kemi Adetiba',
    age: 44,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20female%20director%20kemi%20adetiba%20professional%20headshot%20confident%20expression&image_size=square',
    popularity: 1400000,
    movieCount: 12,
    biography: 'Nigerian filmmaker, television director, and music video director. Known for directing some of the most successful Nollywood films.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['King of Boys', 'The Wedding Party', 'King of Boys: The Return of the King']
  },
  {
    id: 'nig-6',
    name: 'Reminisce',
    age: 43,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20rapper%20actor%20reminisce%20professional%20headshot%20serious%20expression&image_size=square',
    popularity: 1300000,
    movieCount: 8,
    biography: 'Nigerian rapper, singer, songwriter, and actor. Known for his indigenous rap style and transition into acting.',
    birthPlace: 'Kaduna, Nigeria',
    knownFor: ['King of Boys', 'Makanaki', 'Omo Ibadan']
  },
  {
    id: 'nig-7',
    name: 'Jide Kosoko',
    age: 70,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=veteran%20nigerian%20actor%20jide%20kosoko%20professional%20headshot%20wise%20expression&image_size=square',
    popularity: 1900000,
    movieCount: 120,
    biography: 'Veteran Nigerian actor, director, and producer. One of the pioneers of Nollywood with over four decades in the entertainment industry.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['King of Boys', 'Saworoide', 'Agogo Eewo']
  },
  {
    id: 'nig-8',
    name: 'AY Makun',
    age: 53,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20comedian%20actor%20ay%20makun%20professional%20headshot%20cheerful%20smile&image_size=square',
    popularity: 1700000,
    movieCount: 22,
    biography: 'Nigerian comedian, actor, radio and TV presenter, writer, and film producer. Known for his comedy shows and Nollywood productions.',
    birthPlace: 'Warri, Delta State, Nigeria',
    knownFor: ['Merry Men', '30 Days in Atlanta', 'A Trip to Jamaica']
  },
  {
    id: 'nig-9',
    name: 'Falz',
    age: 34,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20rapper%20actor%20falz%20professional%20headshot%20stylish%20look&image_size=square',
    popularity: 1500000,
    movieCount: 15,
    biography: 'Nigerian rapper, songwriter, and actor. Known for his unique style of music and impressive acting performances in Nollywood.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['Merry Men', 'New Money', 'Quam\'s Money']
  },
  {
    id: 'nig-10',
    name: 'Jim Iyke',
    age: 47,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=handsome%20nigerian%20actor%20jim%20iyke%20professional%20headshot%20confident%20look&image_size=square',
    popularity: 1800000,
    movieCount: 75,
    biography: 'Nigerian actor and entrepreneur. One of the highest-paid actors in Nollywood and known for his versatile acting skills.',
    birthPlace: 'Libreville, Gabon (Nigerian parents)',
    knownFor: ['Merry Men', 'Last Flight to Abuja', 'American Driver']
  },
  {
    id: 'nig-11',
    name: 'Ramsey Nouah',
    age: 55,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20actor%20director%20ramsey%20nouah%20professional%20headshot%20distinguished%20look&image_size=square',
    popularity: 2100000,
    movieCount: 95,
    biography: 'Nigerian actor and director. Often referred to as the "Lover Boy" of Nollywood, he has been a leading figure in the industry for decades.',
    birthPlace: 'Edo State, Nigeria',
    knownFor: ['Merry Men', 'Living in Bondage: Breaking Free', 'The Figurine']
  },
  {
    id: 'nig-12',
    name: 'Bisola Aiyeola',
    age: 38,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=beautiful%20nigerian%20actress%20bisola%20aiyeola%20professional%20headshot%20bright%20smile&image_size=square',
    popularity: 1400000,
    movieCount: 28,
    biography: 'Nigerian actress, singer, and MC. Known for her vibrant personality and excellent acting performances in both film and television.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['Sugar Rush', 'Skinny Girl in Transit', 'This Lady Called Life']
  },
  {
    id: 'nig-13',
    name: 'Bimbo Ademoye',
    age: 32,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=young%20beautiful%20nigerian%20actress%20bimbo%20ademoye%20professional%20headshot%20sweet%20smile&image_size=square',
    popularity: 1200000,
    movieCount: 20,
    biography: 'Nigerian actress known for her roles in romantic comedies and dramas. She has quickly become one of the most sought-after young actresses in Nollywood.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['Sugar Rush', 'Breaded Life', 'Dear Affy']
  },
  {
    id: 'nig-14',
    name: 'Williams Uchemba',
    age: 31,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=young%20nigerian%20actor%20williams%20uchemba%20professional%20headshot%20friendly%20smile&image_size=square',
    popularity: 1100000,
    movieCount: 35,
    biography: 'Nigerian actor, comedian, and philanthropist. Started as a child actor and has grown to become one of the prominent figures in Nollywood.',
    birthPlace: 'Abia State, Nigeria',
    knownFor: ['Sugar Rush', 'Merry Men 2', 'The Smart Money Woman']
  },
  {
    id: 'nig-15',
    name: 'Kanayo O. Kanayo',
    age: 62,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=veteran%20nigerian%20actor%20kanayo%20o%20kanayo%20professional%20headshot%20serious%20expression&image_size=square',
    popularity: 2000000,
    movieCount: 110,
    biography: 'Veteran Nigerian actor and lawyer. One of the pioneers of Nollywood and known for his powerful performances in dramatic roles.',
    birthPlace: 'Mbaise, Imo State, Nigeria',
    knownFor: ['Living in Bondage', 'Living in Bondage: Breaking Free', 'Lionheart']
  },
  {
    id: 'nig-16',
    name: 'Enyinna Nwigwe',
    age: 42,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20actor%20enyinna%20nwigwe%20professional%20headshot%20confident%20expression&image_size=square',
    popularity: 1300000,
    movieCount: 45,
    biography: 'Nigerian actor known for his versatile performances in both Nollywood and international productions.',
    birthPlace: 'Imo State, Nigeria',
    knownFor: ['Living in Bondage: Breaking Free', 'Black November', 'The Mirror Boy']
  },
  {
    id: 'nig-17',
    name: 'Nancy Isime',
    age: 32,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=beautiful%20nigerian%20actress%20nancy%20isime%20professional%20headshot%20glamorous%20look&image_size=square',
    popularity: 1600000,
    movieCount: 25,
    biography: 'Nigerian actress, model, and media personality. Known for her beauty and excellent acting skills in contemporary Nollywood films.',
    birthPlace: 'Edo State, Nigeria',
    knownFor: ['Living in Bondage: Breaking Free', 'Hire a Woman', 'The Millions']
  },
  {
    id: 'nig-18',
    name: 'Toyin Abraham',
    age: 42,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20actress%20toyin%20abraham%20professional%20headshot%20warm%20smile&image_size=square',
    popularity: 1700000,
    movieCount: 55,
    biography: 'Nigerian actress and filmmaker. Known for her roles in both Yoruba and English language films.',
    birthPlace: 'Auchi, Edo State, Nigeria',
    knownFor: ['Elevator Baby', 'The Ghost and the Tout', 'Ijakumo']
  },
  {
    id: 'nig-19',
    name: 'Funke Akindele',
    age: 47,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20actress%20funke%20akindele%20professional%20headshot%20cheerful%20expression&image_size=square',
    popularity: 2300000,
    movieCount: 70,
    biography: 'Nigerian actress, filmmaker, and producer. One of the most successful actresses in Nollywood with numerous awards and accolades.',
    birthPlace: 'Ikorodu, Lagos State, Nigeria',
    knownFor: ['Jenifa', 'Battle on Buka Street', 'Omo Ghetto']
  },
  {
    id: 'nig-20',
    name: 'Ini Edo',
    age: 42,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=beautiful%20nigerian%20actress%20ini%20edo%20professional%20headshot%20elegant%20pose&image_size=square',
    popularity: 1900000,
    movieCount: 80,
    biography: 'Nigerian actress and producer. One of the most prominent figures in Nollywood with a career spanning over two decades.',
    birthPlace: 'Akwa Ibom State, Nigeria',
    knownFor: ['World Apart', 'I\'ll Take My Chances', 'Shanty Town']
  },
  {
    id: 'nig-21',
    name: 'Mercy Johnson',
    age: 40,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20actress%20mercy%20johnson%20professional%20headshot%20bright%20smile&image_size=square',
    popularity: 2100000,
    movieCount: 90,
    biography: 'Nigerian actress known for her versatility and ability to interpret roles perfectly. One of the most celebrated actresses in Nollywood.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['Dumebi the Dirty Girl', 'The Maid', 'Heart of a Fighter']
  },
  {
    id: 'nig-22',
    name: 'Genevieve Nnaji',
    age: 45,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=elegant%20nigerian%20actress%20genevieve%20nnaji%20professional%20headshot%20sophisticated%20look&image_size=square',
    popularity: 2500000,
    movieCount: 85,
    biography: 'Nigerian actress, producer, and director. One of the highest-paid actresses in Nollywood and a global ambassador for Nigerian cinema.',
    birthPlace: 'Mbaise, Imo State, Nigeria',
    knownFor: ['Lionheart', 'Half of a Yellow Sun', 'Road to Yesterday']
  },
  {
    id: 'nig-23',
    name: 'Omotola Jalade Ekeinde',
    age: 46,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20actress%20omotola%20jalade%20professional%20headshot%20regal%20expression&image_size=square',
    popularity: 2400000,
    movieCount: 95,
    biography: 'Nigerian actress, singer, philanthropist, and former model. One of the most influential people in Africa and a Nollywood legend.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['Mortal Inheritance', 'Blood Sisters', 'Alter Ego']
  },
  {
    id: 'nig-24',
    name: 'Chidi Mokeme',
    age: 52,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=handsome%20nigerian%20actor%20chidi%20mokeme%20professional%20headshot%20confident%20look&image_size=square',
    popularity: 1800000,
    movieCount: 65,
    biography: 'Nigerian actor and former model. Known for his roles in action and drama films in Nollywood.',
    birthPlace: 'Anambra State, Nigeria',
    knownFor: ['76', 'Shanty Town', 'Critical Assignment']
  },
  {
    id: 'nig-25',
    name: 'Tana Adelana',
    age: 35,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20actress%20tana%20adelana%20professional%20headshot%20modern%20style&image_size=square',
    popularity: 950000,
    movieCount: 18,
    biography: 'Nigerian actress and model known for her roles in contemporary Nollywood productions.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['The Set Up', 'Quam\'s Money', 'Progressive Tailors Club']
  },
  {
    id: 'nig-26',
    name: 'Deyemi Okanlawon',
    age: 41,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20actor%20deyemi%20okanlawon%20professional%20headshot%20serious%20expression&image_size=square',
    popularity: 1200000,
    movieCount: 30,
    biography: 'Nigerian actor known for his intense performances and versatility in both film and television.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['October 1', 'Gidi Blues', 'Blood Sisters']
  },
  {
    id: 'nig-27',
    name: 'Timini Egbuson',
    age: 36,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=young%20handsome%20nigerian%20actor%20timini%20egbuson%20professional%20headshot%20charming%20smile&image_size=square',
    popularity: 1300000,
    movieCount: 25,
    biography: 'Nigerian actor known for his roles in romantic comedies and contemporary Nollywood films.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['The Arbitration', 'Elevator Baby', 'Tinsel']
  },
  {
    id: 'nig-28',
    name: 'Beverly Osu',
    age: 33,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=beautiful%20nigerian%20actress%20beverly%20osu%20professional%20headshot%20glamorous%20look&image_size=square',
    popularity: 1100000,
    movieCount: 20,
    biography: 'Nigerian actress, model, and video vixen. Known for her beauty and acting skills in Nollywood productions.',
    birthPlace: 'Edo State, Nigeria',
    knownFor: ['Okafor\'s Law', 'The Arbitration', 'Isoken']
  },
  {
    id: 'nig-29',
    name: 'Shaffy Bello',
    age: 54,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=elegant%20nigerian%20actress%20shaffy%20bello%20professional%20headshot%20sophisticated%20expression&image_size=square',
    popularity: 1600000,
    movieCount: 40,
    biography: 'Nigerian actress and singer. Known for her powerful performances and elegant screen presence.',
    birthPlace: 'Lagos, Nigeria',
    knownFor: ['Your Excellency', 'Elevator Baby', 'Tinsel']
  },
  {
    id: 'nig-30',
    name: 'Kate Henshaw',
    age: 53,
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigerian%20actress%20kate%20henshaw%20professional%20headshot%20confident%20expression&image_size=square',
    popularity: 1800000,
    movieCount: 75,
    biography: 'Nigerian actress and fitness enthusiast. One of the veteran actresses in Nollywood with numerous awards.',
    birthPlace: 'Cross River State, Nigeria',
    knownFor: ['When the Heart Lies', 'Stronger than Pain', 'The Arbitration']
  },

  // International Actors (keeping some for diversity)
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

  const addActor = (actor: Actor) => {
    actors.value.push(actor)
  }

  return {
    actors,
    currentPage,
    totalActors,
    loadInitialActors,
    loadMoreActors,
    getActorById,
    searchActors,
    addActor
  }
})