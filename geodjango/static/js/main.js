//---------------------------Toast-----------------------------------------

var bt_toast = document.getElementById("toast_btn")
if(bt_toast)
{
    bt_toast.addEventListener("click", (ev)=>{
        document.getElementById("toast_a").classList.remove("show")
    })
}

// --------------------Upload Form Validation ----------------------------------------
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.need-validation')
  
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


//--------------------------------register functions--------------------------------------
var register_m = document.getElementById("register_modal")
if(register_m)
{
    register_m.addEventListener("click", (event)=>{
        var offcan = document.getElementById("user_login")
        offcan.classList.replace("show", "hide")
    })
}

var register_f = document.getElementById("register")
if(register_f)
{
    register_f.addEventListener("submit", (event)=>{
        if(document.getElementById('id_password1').value != document.getElementById('id_password2').value)
        {
            event.preventDefault()
            event.stopPropagation()
            var alert = document.getElementById("alert-box-register")
            alert.style['display'] = 'block';
        }
    })
}

//-----------------------------------------Uploading Raster Layer -------------------------------
function onFormSubmit(event){

    event.preventDefault();
    var myOffcanvas = document.getElementById('upload');
    myOffcanvas.classList.replace("show", "hide")

    var formData=new FormData();
    formData.append("csrfmiddlewaretoken", document.getElementsByName('csrfmiddlewaretoken')[0].value)
    formData.append("mapName",document.getElementById("mName").value);
    formData.append("desc",document.getElementById("desc").value);
    formData.append("c_ramp",document.getElementById("cRamp").value);
    formData.append("raster",document.getElementById("raster").files[0]);
    
    document.getElementById("d_mapName").innerHTML = "Name : " + document.getElementById("mName").value;
    document.getElementById("d_desc").innerHTML = "Description : " + document.getElementById("desc").value;
    document.getElementById("d_cRamp").innerHTML = "Color Ramp : " + document.getElementById("cRamp").value;

    console.log(formData);

    var xhr=new XMLHttpRequest();
    xhr.open("POST","http://127.0.0.1:8000/upload",true);
    xhr.upload.addEventListener("progress", (ev) => {
        if(ev.lengthComputable){
             var percentage=(ev.loaded/ev.total*100|0);
             document.getElementById("progress_bar").style["width"]=""+percentage+"%";
             document.getElementById("progress_bar").innerHTML=""+percentage+"%";
             document.getElementById("progress_text").innerHTML="Uploaded : "+parseInt(ev.loaded/1000000)+"/"+parseInt(ev.total/1000000)+" MB";
             console.log("Uploaded : "+ev.loaded);
             console.log("TOTAL : "+ev.total);
             console.log(percentage);
        }

        var btn = document.getElementById("abort")
        btn.addEventListener('click', ()=> {
            document.getElementById("success_button").style["display"] = "block";
            document.getElementById("progress_bar").classList.add("bg-danger");
            document.getElementById("abort_button").style["display"] = "none";
            document.getElementById("progress_bar").innerHTML=""  
            xhr.abort()
            // setTimeout(()=>{
            //     document.getElementById("mName").innerHTML = "";
            //     document.getElementById("desc").innerHTML = "";
            //     document.getElementById("cRamp").innerHTML = "";
            //     document.getElementById("raster").innerHTML = "";
            // }, 2000)
        })
     });
    xhr.upload.addEventListener("load", (ev) => {
        console.log("Page is loaded")
        document.getElementById("abort_button").style["display"] = "none";
        document.getElementById("success_button").style["display"] = "block";
        document.getElementById("alert-box-content").innerHTML = "Successfully Uploaded";
        document.getElementById("alert-box-dialog").style["display"] = "block"; 
        document.getElementById("progress_bar").classList.remove("bg-danger");
        document.getElementById("progress_bar").innerHTML=""  
        document.getElementById("progress_text").innerHTML=""
    });
    xhr.upload.addEventListener("error", (ev)=>{

    });
    xhr.upload.addEventListener("abort", (ev)=>{
        document.getElementById("mName").innerHTML = "";
        document.getElementById("desc").innerHTML = "";
        document.getElementById("cRamp").innerHTML = "";
        document.getElementById("raster").innerHTML = "";
    });

    xhr.send(formData);

}

//--------------------------Search - GET and POST----------------------------------------

function searchSubmit(event){

    event.preventDefault();

    var spin = document.getElementById("spin")
    var search = document.getElementById("sea").value
    var list = document.getElementById("search_layers")
    list.innerHTML = ''

    var formData1 = new FormData();
    formData1.append("csrfmiddlewaretoken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
    formData1.append("search", search);

    var xhr = new XMLHttpRequest();
    var search_req = new XMLHttpRequest();

    xhr.open("POST", "http://127.0.0.1:8000/search", true)
    search_req.open("GET", "http://127.0.0.1:8000/search", true)
    
    xhr.upload.addEventListener("progress", (oEvent)=> {
        spin.style["display"] = "block"
    });
    xhr.upload.addEventListener("load", (evt) => {
        search_req.send()
        search_req.addEventListener("load", (evt) => {
            var data = JSON.parse(search_req.response)
            spin.style["display"] = "none"
            if(data.length===0)
            {
                list.innerHTML = `
                <h5 class="text-muted" style="margin:2vh;">None Found.</h5>
                `
            }
            else
            {
                list.innerHTML = data.map((e) => 
                    `
                    <a class="list-group-item list-group-item-action">
                    <span data-bs-toggle="collapse" id="span-wms-search" data-bs-target="#${e.color_ramps}0" aria-expanded="true" aria-controls="collapseExample">
                        <div class="d-flex w-100 justify-content-between" id="check">
                        <input class="form-check-input me-1" type="checkbox" value="${e.name}">
                        <h5 class="mb-1">${e.name}</h5>
                        <small> ${e.uploaded_date} </small>
                        </div>
                        <div class="collapse" id="${e.color_ramps}0">
                        <p class="mb-1">${e.description}</p>
                        <small>Color Map : ${e.color_ramps}</small>
                        </div>
                    </span>
                    </a>
                    `
                    ).join('\n')
                

                var triggerSearchWMS = document.querySelectorAll('#search_layers > a > #span-wms-search > #check > input[type=checkbox]')
                const wmsSearchLayers = new ol.layer.Group({
                    title: 'Overlay',
                    fold: 'open',
                    combine: false,
                    layers: [],
                })
                console.log(triggerSearchWMS);

                // ---------------------------------Layer Switcher Functionality-WMS-----------------------------
                triggerSearchWMS.forEach((wmsLayerElement) => {
                    console.log(wmsLayerElement.value);
                    sourc = new ol.source.TileWMS({
                        url: 'http://127.0.0.1:8085/geoserver/App/wms',
                        params: {'LAYERS': 'App:'+wmsLayerElement.value, 'VERSION':'1.1.0', 'TILED':true},
                        serverType: 'geoserver',
                        projection:'ESP:32643',
                        opacity: 0.5,
                    })
                    console.log('WMS Methods', sourc.getSouce().getExtent())
                    var wmsLayer = new ol.layer.Tile({
                        title: wmsLayerElement.value,
                        visible:false,
                        source: sourc
                    });
                    wmsSearchLayers.getLayers().push(wmsLayer);
                });

                map.addLayer(wmsSearchLayers)

                triggerSearchWMS.forEach((wmsLayerElement)=>{
                    wmsLayerElement.addEventListener('change', (event) => {
                        wmsLayerElementValue = wmsLayerElement.value;
                        wmsSearchLayers.getLayers().forEach((element, index, array)=>{
                            console.log("Before", wmsLayerElementValue, element.get('title'), element.get('visible'));
                            let wmsLayerTitle = element.get('title');
                            if(wmsLayerTitle === wmsLayerElementValue)
                            {
                                element.setVisible(!element.get('visible'));
                            }
                            console.log("After", wmsLayerElementValue, element.get('title'), element.get('visible'));
                        })       
                        
                    })
                })
            }

        });
    });
    xhr.send(formData1)
}


//------------------------------------Base Layer IMplementation----------------------------------

const worldbasemap = new ol.layer.Tile({
    source: new ol.source.XYZ({
        url:'http://server.arcgisonline.com/ArcGIS/rest/services/ESRI_StreetMap_World_2D/MapServer/tile/{z}/{y}/{x}.pbf',
        maxZoom: 20,
        attributions: 'Esri, HERE, Garmin, FAO, NOAA, USGS, © OpenStreetMap contributors, and the GIS User Community',
        projection: 'EPSG:4326',
        tileSize: 512, // the tile size supported by the ArcGIS tile service
        maxResolution: 180 / 512, // Esri's tile grid fits 180 degrees on one 512 px tile
        wrapX: true,
    }),
    visible:false,
    baselayer: true,
    title: 'worldbasemap'
    });

const openStreetMapStamenlayer = new ol.layer.Tile({
    source: new ol.source.OSM({
        url:'https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg',
    }),
    visible:false,
    baselayer: true,
    title: 'openStreetMapStamenlayer'
    });

const OSM = new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible:false,
    baselayer: true,
    title: 'OSM'
    });

const aerial = new ol.layer.Tile({
    source: new ol.source.XYZ({
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        maxZoom: 20,
        attributions: 'Esri, HERE, Garmin, FAO, NOAA, USGS, © OpenStreetMap contributors, and the GIS User Community',
    }),
    visible: true,
    baselayer:true,
    title:'aerial',
    });
    

const baseLayerGroup = new ol.layer.Group({
    layers: [ worldbasemap, OSM, openStreetMapStamenlayer, aerial ]
})

// ---------------------------------Layer Switcher Functionality - Base Maps-----------------------------

var triggerMap = document.querySelectorAll('#baseLayers > a')
triggerMap.forEach((baseLayerElement) => {
    baseLayerElement.addEventListener('click', function (event) {
        let link = this.href;
        console.log(link)
        let value;
        for(let val=link.length-1; val>=0; val--)
        {
            if(link.charAt(val)==='/')
            {
                value = link.slice(val+1);
                console.log(value)
                break;
            }
        }
        
        baseLayerGroup.getLayers().forEach((element, index, array)=>{
            let baseLayerTitle = element.get('title');
            console.log(value, baseLayerTitle, baseLayerTitle===value, element)
            element.setVisible(baseLayerTitle===value);
        })
    })
});
    
//------------------------------WMS functionality-------------------------------

var triggerWMS = document.querySelectorAll('#wmsLayers > a > #span-wms> #check > input[type=checkbox]')
const wmsLayers = new ol.layer.Group({
    title: 'Overlay',
    fold: 'open',
    combine: false,
    layers: [],
})
console.log(triggerWMS);

// ---------------------------------Layer Switcher Functionality-WMS-----------------------------


var base_url = 'http://127.0.0.1:8085/geoserver/App/wms?'
var parser = new ol.format.WMSCapabilities();
var result;
fetch('http://127.0.0.1:8085/geoserver/App/wms?SERVICE=WMS&VERSION=1.1.0&REQUEST=GetCapabilities').then((response) => {
    console.log('Response ',response)
    text =  response.text();
}).then((text)=>{
    result = parser.read(text);
})

triggerWMS.forEach((wmsLayerElement) => {

    var extent_3857;
    //------------------------------XML HTTP Request-------------------------------------------

    // var xhr1 = new XMLHttpRequest();
    // xhr1.addEventListener("load", (response) => {
    //     console.log('Response ',response)
    //     return response.text();
    // }).then((text) => {
    //         var result = parser.read(text);
    //         console.log(result)
    //         var extent = result.Capability.Layer.Layer.find(l => l.Name === wmsLayerElement.value).EX_GeographicBoundingBox;
    //         console.log(extent)
            // extent_3857 = ol.proj.transformExtent(extent, 'EPSG:4326', 'EPSG:3857')
    // });
    // xhr1.open("GET", CORS_PREFIX + base_url + "SERVICE=WMS&VERSION=1.1.0&REQUEST=GetCapabilities")    
    // xhr1.addEventListener("progress", (oEvent)=> {
    // });    
    // xhr1.send()

    //------------------------------------------------------------------

    //---------------------------------------_FETCH API -----------------------------------------
    // Parse WMS Capabilities to retrieve layer exten
    console.log(result)
    if(result)
    {
        var extent = result.Capability.Layer.Layer.find(l => l.Name === wmsLayerElement.value).EX_GeographicBoundingBox;
        console.log(extent)
        extent_3857 = ol.proj.transformExtent(extent, 'EPSG:4326', 'EPSG:3857')
    }  

    console.log(wmsLayerElement.value);
    var source1 = new ol.source.TileWMS({
        url: 'http://127.0.0.1:8085/geoserver/App/wms',
        params: {'LAYERS': 'App:'+wmsLayerElement.value, 'VERSION':'1.1.0', 'TILED':true},
        serverType: 'geoserver',
        projection:'ESP:32643',
        opacity: 0.5,
    });
    var wmsLayer = new ol.layer.Tile({
        title: wmsLayerElement.value,
        visible:false,
        source: source1,
        extent:extent_3857,
    });
    console.log('WMS Methods', wmsLayer.getExtent(), wmsLayer.getSource())
    wmsLayers.getLayers().push(wmsLayer);
});

triggerWMS.forEach((wmsLayerElement)=>{
    wmsLayerElement.addEventListener('change', (event) => {
        wmsLayerElementValue = wmsLayerElement.value;
        wmsLayers.getLayers().forEach((element, index, array)=>{
            console.log("Before", wmsLayerElementValue, element.get('title'), element.get('visible'));
            let wmsLayerTitle = element.get('title');
            if(wmsLayerTitle === wmsLayerElementValue)
            {
                element.setVisible(!element.get('visible'));
                if(element.getExtent())
                {
                    var layerExtent = element.getExtent();
                    if (layerExtent) {
                        map.getView().fit(layerExtent);
                    }
                }
            }
            console.log("After", wmsLayerElementValue, element.get('title'), element.get('visible'));
        })       
        
    })
})

// -------------------------------------WMS Cluster Layers--------------------------------
//------------------------------WMS Cluster functionality-------------------------------

var triggerClusterWMS = document.querySelectorAll('#wmsClusterLayers > a > #span-wms-cluster > #check > input[type=checkbox]')
const wmsClusterLayers = new ol.layer.Group({
    title: 'Overlay',
    fold: 'open',
    combine: false,
    layers: [],
})
console.log(triggerClusterWMS);

// ---------------------------------Layer Switcher Cluster Functionality-WMS-----------------------------
triggerClusterWMS.forEach((wmsLayerElement) => {
    console.log(wmsLayerElement.value);
    var wmsLayer = new ol.layer.Tile({
        title: wmsLayerElement.value,
        visible:false,
        source: new ol.source.TileWMS({
            url: 'http://127.0.0.1:8085/geoserver/App/wms',
            params: {'LAYERS': 'App:'+wmsLayerElement.value, 'VERSION':'1.1.0', 'TILED':true},
            serverType: 'geoserver',
            projection:'ESP:32643',
            opacity: 0.5,
        })
    });
    wmsLayers.getLayers().push(wmsLayer);
});

triggerClusterWMS.forEach((wmsLayerElement)=>{
    wmsLayerElement.addEventListener('change', (event) => {
        wmsLayerElementValue = wmsLayerElement.value;
        wmsLayers.getLayers().forEach((element, index, array)=>{
            console.log("Before", wmsLayerElementValue, element.get('title'), element.get('visible'));
            let wmsLayerTitle = element.get('title');
            if(wmsLayerTitle === wmsLayerElementValue)
            {
                element.setVisible(!element.get('visible'));
            }
            console.log("After", wmsLayerElementValue, element.get('title'), element.get('visible'));
        })       
        
    })
})

// -------------------------------------WMS Change Layers--------------------------------
//------------------------------WMS Change functionality-------------------------------

var triggerChangeWMS = document.querySelectorAll('#wmsChangeLayers > a > #span-wms-change > #check > input[type=checkbox]')
const wmsChangeLayers = new ol.layer.Group({
    title: 'Overlay',
    fold: 'open',
    combine: false,
    layers: [],
})
console.log(triggerChangeWMS);

// ---------------------------------Layer Switcher Functionality-WMS-----------------------------
triggerChangeWMS.forEach((wmsLayerElement) => {
    console.log(wmsLayerElement.value);
    var wmsLayer = new ol.layer.Tile({
        title: wmsLayerElement.value,
        visible:false,
        source: new ol.source.TileWMS({
            url: 'http://127.0.0.1:8085/geoserver/App/wms',
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

triggerChangeWMS.forEach((wmsLayerElement)=>{
    wmsLayerElement.addEventListener('change', (event) => {
        wmsLayerElementValue = wmsLayerElement.value;
        wmsLayers.getLayers().forEach((element, index, array)=>{
            console.log("Before", wmsLayerElementValue, element.get('title'), element.get('visible'));
            let wmsLayerTitle = element.get('title');
            if(wmsLayerTitle === wmsLayerElementValue)
            {
                element.setVisible(!element.get('visible'));
            }
            console.log("After", wmsLayerElementValue, element.get('title'), element.get('visible'));
        })       
        
    })
})


// -------------------------------------Original Map Function-----------------------------

// var obj = new OpenLayers.Format.WMSCapabilities().read(response.responseText);
// var capability = obj.capability;
// for (var i=0, len=capability.layers.length; i<len; i++) {
//     var layerObj = capability.layers[i];
//     if (layerObj.name === myLayerName) {
//         map.zoomToExtent(OpenLayers.Bounds.fromArray(layerObj.llbbox));
//         break;
//     }
// }

var view = new ol.View({
    center: ol.proj.fromLonLat([78.96, 20.59]),
    zoom: 3,
});

const mousePositionControl = new ol.control.MousePosition({
    coordinateFormat: ol.coordinate.createStringXY(2),
    projection: 'EPSG:4326',
    className: 'custom-mouse-position',
    target: document.getElementById('mouse-position'),
  });

var map = new ol.Map({
    target: 'map',
    layers: [],
    render: 'canvas',
    view: view,
    controls: ol.control.defaults({ attributionOptions: { collapsible: true }}).extend([
        new ol.control.Zoom(),
        new ol.control.ZoomSlider(),
        new ol.control.ScaleLine(),
        new ol.control.FullScreen(),
        mousePositionControl
    ]),
    interactions: ol.interaction.defaults().extend([
        new ol.interaction.DragRotateAndZoom(),
    ]),
    layers: [baseLayerGroup, wmsLayers, wmsClusterLayers, wmsChangeLayers],
});