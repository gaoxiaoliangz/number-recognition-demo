var pad = CanvasPainter(document.querySelector('#pad'));

var store = {}

var Home = (children) => {
  return `
    <div class="home">${children}</div>
  `
}

var Container = (children) => {
  return `
    <div class="container">${children}</div>
  `
}

var Root = (children) => {
  return `
    <div class="root">${children}</div>
  `
}

var Button = (text, onClick) => {
  return `
    <button onclick="${onClick}" class="btn">${text}</button>
  `
}

var Page = (store) => Root(Container(Home(
  `
    <h1>this is home</h1>
    <p>you clicked ${store.count}</p>
    ${Button('change', 'store.count = store.count + 1;console.log(store);updateView()')}
  `
)))

function render(el, dom) {
  el.innerHTML = dom
}

// init
store.count = 1


function updateView() {
  render(document.querySelector('#root'), Page(store))
}

updateView()
