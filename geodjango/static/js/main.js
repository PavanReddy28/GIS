// --------------------Form Validation ----------------------------------------
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

//------------------------------------Base Layer IMplementation----------------------------------

const baselayerOSM = new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible:true,
    baselayer: true,
    title: 'openStreetMapStandard'
    });

const openStreetMapStamenlayer = new ol.layer.Tile({
    source: new ol.source.OSM({
        url:'https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg'
    }),
    visible:false,
    baselayer: true,
    title: 'openStreetMapStamenlayer'
    });

const OSMStamenLayer = new ol.layer.Tile({
    source: new ol.source.OSM({
        url:'https://stamen-tiles.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg'
    }),
    visible:false,
    baselayer: true,
    title: 'OSMStamenWaterLayer'
    });

const baseLayerGroup = new ol.layer.Group({
    layers: [ baselayerOSM, OSMStamenLayer, openStreetMapStamenlayer ]
})

// ---------------------------------Layer Switcher Functionality - Base Maps-----------------------------

var triggerMap = document.querySelectorAll('#baseLayers > a')
triggerMap.forEach((baseLayerElement) => {
    baseLayerElement.addEventListener('click', function (event) {
        let link = this.href;
        let value;
        for(let val=link.length-1; val>=0; val--)
        {
            if(link.charAt(val)==='/')
            {
                value = link.slice(val+1);
                break;
            }
        }
        
        baseLayerGroup.getLayers().forEach((element, index, array)=>{
            let baseLayerTitle = element.get('title');
            element.setVisible(baseLayerTitle===value);
        })
    })
});
    
//------------------------------WMS functionality-------------------------------

var triggerWMS = document.querySelectorAll('#wmsLayers > a > input[type=checkbox]')
const wmsLayers = new ol.layer.Group({
    title: 'Overlay',
    fold: 'open',
    combine: false,
    layers: [],
})
console.log(triggerWMS);

// ---------------------------------Layer Switcher Functionality-WMS-----------------------------
triggerWMS.forEach((wmsLayerElement) => {
    console.log(wmsLayerElement.value);
    var wmsLayer = new ol.layer.Tile({
        title:wmsLayerElement.value,
        source: new ol.source.TileWMS({
            url: 'https://127.0.0.1:8085/geoserver/App/wms',
            params: {'LAYERS': 'App:'+wmsLayerElement.value, 'VERSION':'1.1.0', 'TILED':true},
            serverType: 'geoserver',
            projection:'ESP:32643',
            opacity: 0.5,
        })
        // new ol.source.TileWMS({
        //     url:'http://127.0.0.1:8085/geoserver/App/wms?service=WMS&version=1.1.0&request=GetMap&layers=App%3AHyderabad&bbox=799980.0%2C1890240.0%2C909780.0%2C2000040.0&width=768&height=768&srs=EPSG%3A32643&styles=&format=application%2Fopenlayers3'
        // })
    });
    wmsLayers.getLayers().push(wmsLayer);
});

triggerWMS.forEach((wmsLayerElement)=>{
    wmsLayerElement.addEventListener('change', (event) => {
        console.log(this.value);
        
    })
})

/*
extent: [636757.681558, 6351042.69913, 728716.389785, 6478379.8966],
wmsLayerElement.addEventListener('change', function (event) {
    console.log(this.value)    
    map.addlayer(wmsLayer);
})
*/

// -------------------------------------Original Map Function-----------------------------
var view = new ol.View({
    center: ol.proj.fromLonLat([78.96, 20.59]),
    zoom: 4,
    enableRotation: false
});

var map = new ol.Map({
    target: 'map',
    layers: [],
    render: 'canvas',
    view: view,
    controls: ol.control.defaults({ attributionOptions: { collapsible: false }}).extend([
        new ol.control.Zoom(),
        new ol.control.ZoomSlider(),
        new ol.control.Rotate(),
        new ol.control.ScaleLine(),
        new ol.control.MousePosition({
            coordinateFormat: ol.coordinate.createStringXY(4),
            projection: 'EPSG:4326'
        })
    ]),
    layers: [baseLayerGroup, wmsLayers],
});

/*
interactions: ol.interaction.defaults().extend([
            new ol.interaction.Select({
                layers: [baselayers, toplayers]
            })
        ])
*/