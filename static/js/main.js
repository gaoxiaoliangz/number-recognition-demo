import CanvasPainter from './canvas-painter.js'

var canvas = document.querySelector('#canvas')
var painter = CanvasPainter(canvas)

$('.js-rec').click(() => {
  $.post('/recog', {
    img: canvas.toDataURL()
  }, data => {
    $('.result')[0].innerHTML = `Number is ${data.num}`
  })
})
