import { ref, onMounted, onUnmounted } from 'vue'

export interface AccessibilityOptions {
  announceChanges?: boolean
  trapFocus?: boolean
  restoreFocus?: boolean
}

export function useAccessibility(options: AccessibilityOptions = {}) {
  const {
    announceChanges = true,
    trapFocus = false,
    restoreFocus = true
  } = options

  const previouslyFocusedElement = ref<HTMLElement | null>(null)
  const trapContainer = ref<HTMLElement | null>(null)

  // Screen reader announcements
  const announceToScreenReader = (message: string, priority: 'polite' | 'assertive' = 'polite') => {
    if (!announceChanges) return

    const announcement = document.createElement('div')
    announcement.setAttribute('aria-live', priority)
    announcement.setAttribute('aria-atomic', 'true')
    announcement.className = 'sr-only'
    announcement.textContent = message
    document.body.appendChild(announcement)

    setTimeout(() => {
      if (document.body.contains(announcement)) {
        document.body.removeChild(announcement)
      }
    }, 1000)
  }

  // Focus management
  const saveFocus = () => {
    previouslyFocusedElement.value = document.activeElement as HTMLElement
  }

  const restorePreviousFocus = () => {
    if (restoreFocus && previouslyFocusedElement.value) {
      previouslyFocusedElement.value.focus()
      previouslyFocusedElement.value = null
    }
  }

  const focusFirstElement = (container: HTMLElement) => {
    const focusableElements = getFocusableElements(container)
    if (focusableElements.length > 0) {
      focusableElements[0].focus()
    }
  }

  const focusLastElement = (container: HTMLElement) => {
    const focusableElements = getFocusableElements(container)
    if (focusableElements.length > 0) {
      focusableElements[focusableElements.length - 1].focus()
    }
  }

  // Get all focusable elements within a container
  const getFocusableElements = (container: HTMLElement): HTMLElement[] => {
    const focusableSelectors = [
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      'a[href]',
      '[tabindex]:not([tabindex="-1"])',
      '[contenteditable="true"]'
    ].join(', ')

    return Array.from(container.querySelectorAll(focusableSelectors)) as HTMLElement[]
  }

  // Focus trap for modals and dropdowns
  const handleFocusTrap = (event: KeyboardEvent) => {
    if (!trapFocus || !trapContainer.value) return

    const focusableElements = getFocusableElements(trapContainer.value)
    if (focusableElements.length === 0) return

    const firstElement = focusableElements[0]
    const lastElement = focusableElements[focusableElements.length - 1]

    if (event.key === 'Tab') {
      if (event.shiftKey) {
        // Shift + Tab
        if (document.activeElement === firstElement) {
          event.preventDefault()
          lastElement.focus()
        }
      } else {
        // Tab
        if (document.activeElement === lastElement) {
          event.preventDefault()
          firstElement.focus()
        }
      }
    }
  }

  // Keyboard navigation helpers
  const handleArrowNavigation = (
    event: KeyboardEvent,
    items: HTMLElement[],
    currentIndex: number,
    orientation: 'horizontal' | 'vertical' = 'vertical'
  ) => {
    let newIndex = currentIndex

    if (orientation === 'vertical') {
      if (event.key === 'ArrowDown') {
        event.preventDefault()
        newIndex = (currentIndex + 1) % items.length
      } else if (event.key === 'ArrowUp') {
        event.preventDefault()
        newIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1
      }
    } else {
      if (event.key === 'ArrowRight') {
        event.preventDefault()
        newIndex = (currentIndex + 1) % items.length
      } else if (event.key === 'ArrowLeft') {
        event.preventDefault()
        newIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1
      }
    }

    if (newIndex !== currentIndex && items[newIndex]) {
      items[newIndex].focus()
      return newIndex
    }

    return currentIndex
  }

  // Setup focus trap
  const setupFocusTrap = (container: HTMLElement) => {
    trapContainer.value = container
    saveFocus()
    focusFirstElement(container)
    document.addEventListener('keydown', handleFocusTrap)
  }

  // Remove focus trap
  const removeFocusTrap = () => {
    document.removeEventListener('keydown', handleFocusTrap)
    trapContainer.value = null
    restorePreviousFocus()
  }

  // Generate unique IDs for accessibility
  const generateId = (prefix = 'a11y') => {
    return `${prefix}-${Math.random().toString(36).substr(2, 9)}`
  }

  // Cleanup on unmount
  onUnmounted(() => {
    if (trapFocus) {
      removeFocusTrap()
    }
  })

  return {
    announceToScreenReader,
    saveFocus,
    restorePreviousFocus,
    focusFirstElement,
    focusLastElement,
    getFocusableElements,
    handleArrowNavigation,
    setupFocusTrap,
    removeFocusTrap,
    generateId
  }
}

// Screen reader only CSS class
export const srOnlyClass = 'sr-only'

// Add global styles for screen reader only content
if (typeof document !== 'undefined') {
  const style = document.createElement('style')
  style.textContent = `
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
  `
  document.head.appendChild(style)
}