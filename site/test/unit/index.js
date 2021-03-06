// Polyfill fn.bind() for PhantomJS
/* eslint-disable no-extend-native */
Function.prototype.bind = require('function-bind');

// require all test files (files that ends with .spec.js)
const testsContext = require.context('./specs', true, /\.spec$/);
testsContext.keys().forEach(testsContext);

// require all ui files except main.js for coverage.
// you can also change this to match only the subset of files that
// you want coverage for.
// const uiContext = require.context('ui', true, /^\.\/(?!main(\.js)?$)/);
const uiContext = require.context('ui', true, /^.*\.vue$/);
uiContext.keys().forEach(uiContext);
