require([
    "esri/config",
    "esri/Map",
    "esri/views/MapView",
    "esri/layers/GraphicsLayer",
    "esri/layers/WebTileLayer",
    "esri/Graphic"
], function (esriConfig, Map, MapView, GraphicsLayer, WebTileLayer, Graphic) {
    esriConfig.apiKey = "AAPTaSf9ochmxM7ErZsLf33_ONA..vnTKu2JDoLP4ozSYZ6SWXutNdvzUaD11QTTkWBV7d7N33r16kAlMZQSOeWcajTiCs6FiPkBIOuFQNCyCNJ4GuWAM2eID5cE_kTeKpLnSOa2bjcn6PCTqxce9HpxgH4tkG_IxlurLPWv42BJxeUl5S1ywN_GneYqnvyeeqFG1cgL-zf8BIrrOamHrQF_UyGyic2OqIpvr2mZQkHhY5laEUhEmuFZDPpuawHmE7-RDSCDHMXl0Oal-fEQ.AT1_LbeIav5l";

    const map = new Map({
        basemap: "arcgis-dark-gray"
    });

    const view = new MapView({
        container: "viewDiv",
        map: map,
        center: [-111.789, 43.826],
        zoom: 9,
        constraints: {
            minZoom: 0,
            maxZoom: 19
        }
    })

    const graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);

    const cloudsLayer = new WebTileLayer({
        urlTemplate: "https://tile.openweathermap.org/map/clouds_new/{level}/{col}/{row}.png?appid=e78738478133c7598b94f856ad537606",
        opacity: 1,
        blendMode: "screen",
        title: "Cloud coverage"
    });
    const tempLayer = new WebTileLayer({
        urlTemplate: "https://tile.openweathermap.org/map/temp_new/{level}/{col}/{row}.png?appid=e78738478133c7598b94f856ad537606",
        opacity: 0.35,
        title: "Temperature"
    });

    const windLayer = new WebTileLayer({
        urlTemplate: "https://tile.openweathermap.org/map/wind_new/{level}/{col}/{row}.png?appid=e78738478133c7598b94f856ad537606",
        opacity: 1,
        blendMode: "screen",
        title: "Wind"
    });
    
    map.addMany([tempLayer, windLayer, cloudsLayer]);

    cloudsLayer.when(
        function () {
            console.log("Cloud coverage layer loaded.");
        },
        function (error) {
            console.error("Cloud coverage layer failed to load:", error);
        }
    );

    windLayer.when(
        function () {
            console.log("Wind layer loaded.");
        },
        function (error) {
            console.error("Wind layer failed to load:", error);
        }
    );
});

// Next step - making each layer toggleable and adding labels to specific geographic points for temperature, wind speeds, precipitation that turn on and off with the toggles as well. 