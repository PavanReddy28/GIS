(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
    })()

baselayerOSM = new ol.layer.Tile({
    source: new ol.source.OSM()
    });

var map = new ol.Map({
    target: 'map',
    layers: [
        baselayerOSM,       
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([20.59, 78.96]),
        zoom: 4
    })
    });