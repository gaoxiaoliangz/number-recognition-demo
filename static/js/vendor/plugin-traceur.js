SystemJS._loader.loadedTranspilerRuntime = true;

define(function(require, exports, module) {
  var traceur = require('traceur');

  function prepend(a, b) {
    for (var p in b)
      if (!(p in a))
        a[p] = b[p];
    return a;
  }

  exports.translate = function(load) {
    var options = {
      modules: 'instantiate',
      script: false,
      sourceMaps: this.builder ? 'memory' : 'inline',
      filename: load.address,
      inputSourceMap: load.metadata.sourceMap,
      moduleName: false
    };

    if (load.metadata.traceurOptions)
      prepend(options, load.metadata.traceurOptions);

    if (this.traceurOptions)
      prepend(options, this.traceurOptions);

    var compiler = new traceur.Compiler(options);

    load.metadata.format = 'register';

    var transpiledSource = doTraceurCompile(load.source, compiler, options.filename);

    var usesRuntime = transpiledSource.match(/\$traceurRuntime/);

    if (this.builder) {
      // this should not be a global but Traceur gives us no choice!
      if (usesRuntime)
        transpiledSource = transpiledSource.replace('System.register(["', 'System.register(["traceur-runtime", "').replace('System.register([]', 'System.register(["traceur-runtime"]');
      load.metadata.sourceMap = JSON.parse(compiler.getSourceMap());
      return transpiledSource;
    }
    else {
      if (usesRuntime)
        load.metadata.deps.push('traceur-runtime');
      return '(function(__moduleName){' + transpiledSource + '\n})("' + load.name + '");\n//# sourceURL=' + load.address + '!transpiled';
    }
  };

  function doTraceurCompile(source, compiler, filename) {
    try {
      return compiler.compile(source, filename);
    }
    catch(e) {
      e.stack = e.stack || e.message;
      throw e;
    }
  }
});