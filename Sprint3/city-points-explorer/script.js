require([
  "esri/config",
  "esri/Map",
  "esri/views/MapView",
  "esri/layers/GraphicsLayer",
  "esri/Graphic"
], function (esriConfig, Map, MapView, GraphicsLayer, Graphic) {
  esriConfig.apiKey = "AAPTaSf9ochmxM7ErZsLf33_ONA..vnTKu2JDoLP4ozSYZ6SWXutNdvzUaD11QTTkWBV7d7N33r16kAlMZQSOeWcajTiCs6FiPkBIOuFQNCyCNJ4GuWAM2eID5cE_kTeKpLnSOa2bjcn6PCTqxce9HpxgH4tkG_IxlurLPWv42BJxeUl5S1ywN_GneYqnvyeeqFG1cgL-zf8BIrrOamHrQF_UyGyic2OqIpvr2mZQkHhY5laEUhEmuFZDPpuawHmE7-RDSCDHMXl0Oal-fEQ.AT1_LbeIav5l";


  const map = new Map({
    // You can later change basemap to "arcgis-imagery" (satellite), "arcgis-streets", etc.
    basemap: "arcgis-topographic"
  });

  const view = new MapView({
    container: "viewDiv",
    map: map,
    center: [-111.789, 43.826],
    zoom: 11
  });
  
  const graphicsLayer = new GraphicsLayer();
  map.add(graphicsLayer);

  // This will define how each marker looks. Later, for radar, you might use colors to represent intensity.
  const markerSymbol = {
    type: "simple-marker",
    color: [0, 122, 255, 0.9],
    outline: {
        color: [255, 255, 255, 0.9],
        width: 1
    },
    size: 8
  };
  
  const popupTemplate = {
    title: "{Name}",
    content: `
        <b>Type:</b> {Type}<br/>
        <b>Description:</b> {Description}
    `
  };
  
  // This is your “attribute store”
  // Each object holds marker info (requirement #3).
  // Later, for radar, these attributes might be: intensity, stormId, timestamp, etc.
  const cityPoints = [
    {name: "Point 1", type: "Park", description: "Small neighborhood park.", lon: -111.789, lat: 43.826},
    {name: "Point 2", type: "School", description: "Elementary school.", lon: -111.80, lat: 43.83},
    {name: "Point 3", type: "Library", description: "City library.", lon: -111.78, lat: 43.82},
    { name: "Point 4", type: "Store", description: "Local grocery store.", lon: -111.79, lat: 43.825 },
    { name: "Point 5", type: "Park", description: "Large city park.", lon: -111.81, lat: 43.828 },
    { name: "Point 6", type: "Cafe", description: "Popular coffee shop.", lon: -111.782, lat: 43.821 },
    { name: "Point 7", type: "Gym", description: "Community gym.", lon: -111.795, lat: 43.829 },
    { name: "Point 8", type: "Hospital", description: "Regional hospital.", lon: -111.805, lat: 43.824 },
    { name: "Point 9", type: "School", description: "High school.", lon: -111.792, lat: 43.832 },
    { name: "Point 10", type: "Park", description: "Dog-friendly park.", lon: -111.787, lat: 43.818 },
    { name: "Point 11", type: "Store", description: "Hardware store.", lon: -111.783, lat: 43.827 },
    { name: "Point 12", type: "Office", description: "Office building.", lon: -111.799, lat: 43.822 },
    { name: "Point 13", type: "Restaurant", description: "Family restaurant.", lon: -111.784, lat: 43.819 },
    { name: "Point 14", type: "Park", description: "Playground park.", lon: -111.796, lat: 43.817 },
    { name: "Point 15", type: "Store", description: "Bookstore.", lon: -111.788, lat: 43.823 },
    { name: "Point 16", type: "School", description: "Middle school.", lon: -111.802, lat: 43.831 },
    { name: "Point 17", type: "Library", description: "Branch library.", lon: -111.781, lat: 43.824 },
    { name: "Point 18", type: "Cafe", description: "Quiet study cafe.", lon: -111.793, lat: 43.820 },
    { name: "Point 19", type: "Gym", description: "Fitness center.", lon: -111.797, lat: 43.826 },
    { name: "Point 20", type: "Park", description: "Trailhead park.", lon: -111.806, lat: 43.829 }
  ]

  cityPoints.forEach(function (pt) {
    const pointGeometry = {
        type: "point",
        longitude: pt.lon,
        latitude: pt.lat
    };

    const attributes = {
        Name: pt.name,
        Type: pt.type,
        Description: pt.description
    };

    const graphic = new Graphic({
        geometry: pointGeometry,
        symbol: markerSymbol,
        attributes: attributes,
        popupTemplate: popupTemplate
    });
  
    graphicsLayer.add(graphic);
  });
});