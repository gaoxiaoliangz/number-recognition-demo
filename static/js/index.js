// set our baseURL reference path
SystemJS.config({
  baseURL: '../static/js',
  // packages: {
  //   hello: {
  //     main: './hello.js',
  //     defaultExtension: 'js'
  //   },
  // },
  transpilerRuntime: false,
  // map: {
  //   'plugin-traceur': '../node_modules/systemjs-plugin-traceur/plugin-traceur.js',
  //   'traceur': '../node_modules/traceur/bin/traceur.js',
  //   'traceur-runtime': '../node_modules/traceur/bin/traceur-runtime.js'
  // },
  map: {
    'plugin-traceur': 'vendor/plugin-traceur.js',
    'traceur': 'vendor/traceur.js',
    'traceur-runtime': 'vendor/traceur-runtime.js'
  },
  meta: {
    'traceur': {
      format: 'global',
      exports: 'traceur',
      scriptLoad: false
    },
    'traceur-runtime': {
      format: 'global',
      exports: '$traceurRuntime'
    }
  },
  transpiler: 'plugin-traceur',
  transpilerRuntime: false
});

// loads /js/main.js
SystemJS.import('main2.js');
