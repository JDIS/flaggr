import VueI18n from '@/plugins/i18n'
import { SnackbarProgrammatic } from 'buefy'
import { SnackbarConfig } from 'buefy/types/components'

/**
 * Display an alert as a buefy Snackbar to the user
 * @param message Message to display
 * @param variables Variables to insert in vue-i18n message
 *                  https://kazupon.github.io/vue-i18n/guide/formatting.html#named-formatting
 * @param options SnackbarConfig options https://buefy.org/documentation/snackbar/
 */
export function sendAlertWithVariables(message: string, variables: object, options: object = {}) {
  const defaults: SnackbarConfig = {
    message: VueI18n.t(message, variables) as string,
    type: 'is-danger',
    position: 'is-bottom-right',
    queue: false
  }
  SnackbarProgrammatic.open({...defaults, ...options} as SnackbarConfig)
}

/**
 * Display an alert as a buefy Snackbar to the user
 * @param message Message to display
 * @param options SnackbarConfig options https://buefy.org/documentation/snackbar/
 */
export function sendAlert(message: string, options: object = {}) {
  sendAlertWithVariables(message, {}, options)
}
