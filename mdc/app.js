import * as mdc from 'material-components-web';

import {MDCRipple} from '@material/ripple';
import {MDCSelect} from '@material/select';
import {MDCTextField} from '@material/textfield';

const shippingForm = document.querySelector('#crane-shipping-form');
shippingForm.addEventListener('submit', (evt) => {
  evt.preventDefault();
  alert('Success!');
});

new MDCRipple(document.querySelector('.mdc-button'));
new MDCSelect(document.querySelector('.mdc-select'));

const textFieldElements = [].slice.call(document.querySelectorAll('.mdc-text-field'));
textFieldElements.forEach((textFieldEl) => {
  new MDCTextField(textFieldEl);
});

const iconButtonRipple = new MDCRipple(document.querySelector('.mdc-icon-button'));
iconButtonRipple.unbounded = true;

// const surface = document.querySelector('.abc');
// const ripple = new MDCRipple(surface);