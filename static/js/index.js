// set our baseURL reference path
SystemJS.config({
  baseURL: '../static/js',
  transpilerRuntime: false,
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
SystemJS.import('main.js');
