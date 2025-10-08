import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import LemonPieRating from './LemonPieRating.vue'

describe('LemonPieRating', () => {
  it('renders correctly with default props', () => {
    const wrapper = mount(LemonPieRating, {
      props: {
        rating: 3.5
      }
    })
    
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('.rounded-full').exists()).toBe(true)
  })

  it('displays lemon emoji for low ratings', () => {
    const wrapper = mount(LemonPieRating, {
      props: {
        rating: 3
      }
    })
    
    expect(wrapper.text()).toContain('🍋')
  })

  it('displays pie emoji for high ratings', () => {
    const wrapper = mount(LemonPieRating, {
      props: {
        rating: 8
      }
    })
    
    expect(wrapper.text()).toContain('🥧')
  })

  it('displays neutral emoji for medium ratings', () => {
    const wrapper = mount(LemonPieRating, {
      props: {
        rating: 5.5
      }
    })
    
    expect(wrapper.text()).toContain('😐')
  })

  it('shows rating text when showText is true', () => {
    const wrapper = mount(LemonPieRating, {
      props: {
        rating: 3.5,
        showText: true
      }
    })
    
    expect(wrapper.text()).toContain('3.5')
    expect(wrapper.text()).toContain('Lemon')
  })

  it('hides rating text when showText is false', () => {
    const wrapper = mount(LemonPieRating, {
      props: {
        rating: 3.5,
        showText: false
      }
    })
    
    expect(wrapper.text()).toContain('3.5')
    expect(wrapper.text()).not.toContain('Lemon')
  })

  it('applies correct size classes', () => {
    const wrapper = mount(LemonPieRating, {
      props: {
        rating: 3,
        size: 'lg'
      }
    })
    
    expect(wrapper.find('.w-16').exists()).toBe(true)
  })

  it('is interactive when interactive prop is true', () => {
    const wrapper = mount(LemonPieRating, {
      props: {
        rating: 3,
        interactive: true
      }
    })
    
    const ratingElement = wrapper.find('.rounded-full')
    expect(ratingElement.classes()).toContain('cursor-pointer')
  })

  it('emits ratingChange event when clicked in interactive mode', async () => {
    const wrapper = mount(LemonPieRating, {
      props: {
        rating: 3,
        interactive: true
      }
    })
    
    const ratingElement = wrapper.find('.rounded-full')
    await ratingElement.trigger('click')
    expect(wrapper.emitted('ratingChange')).toBeTruthy()
    expect(wrapper.emitted('ratingChange')?.[0]).toEqual([3])
  })
})