import CanvasPainter from './canvas-painter.js'

var pad = CanvasPainter(document.querySelector('#pad'))

var canvas = document.querySelector('#pad')

document.querySelector('.js-save').addEventListener('click', () => {
  var pngUrl = canvas.toDataURL()
  console.log(pngUrl)
})

// document.querySelector('.js-clear').addEventListener('click', () => {
//   console.log('hehe')
  
//   pad.clear()
// })

document.querySelector('.js-rec').addEventListener('click', () => {
  $.post('/upload', {
    img: canvas.toDataURL()
  })
})
