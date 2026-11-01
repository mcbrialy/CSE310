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
        zoom: 4,
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
        title: "Cloud coverage",
        refreshInterval: 10
    });
    const tempLayer = new WebTileLayer({
        urlTemplate: "https://tile.openweathermap.org/map/temp_new/{level}/{col}/{row}.png?appid=e78738478133c7598b94f856ad537606",
        opacity: 0.35,
        title: "Temperature",
        refreshInterval: 10
    });

    const windLayer = new WebTileLayer({
        urlTemplate: "https://tile.openweathermap.org/map/wind_new/{level}/{col}/{row}.png?appid=e78738478133c7598b94f856ad537606",
        opacity: 1,
        blendMode: "screen",
        title: "Wind",
        refreshInterval: 10
    });
    
    map.addMany([tempLayer, windLayer, cloudsLayer]);

    const weatherApiKey = "e78738478133c7598b94f856ad537606";

    // State, province, and territory capitals not included in the worldwide
    // country-capital dataset below.
    const regionalCapitals = [
        { name: "Montgomery", region: "Alabama", country: "United States", lat: 32.3777, lon: -86.3000, type: "U.S. state capital" },
        { name: "Juneau", region: "Alaska", country: "United States", lat: 58.3019, lon: -134.4197, type: "U.S. state capital" },
        { name: "Phoenix", region: "Arizona", country: "United States", lat: 33.4481, lon: -112.0969, type: "U.S. state capital" },
        { name: "Little Rock", region: "Arkansas", country: "United States", lat: 34.7466, lon: -92.2880, type: "U.S. state capital" },
        { name: "Sacramento", region: "California", country: "United States", lat: 38.5767, lon: -121.4944, type: "U.S. state capital" },
        { name: "Denver", region: "Colorado", country: "United States", lat: 39.7392, lon: -104.9903, type: "U.S. state capital" },
        { name: "Hartford", region: "Connecticut", country: "United States", lat: 41.7640, lon: -72.6822, type: "U.S. state capital" },
        { name: "Dover", region: "Delaware", country: "United States", lat: 39.1573, lon: -75.5197, type: "U.S. state capital" },
        { name: "Tallahassee", region: "Florida", country: "United States", lat: 30.4381, lon: -84.2813, type: "U.S. state capital" },
        { name: "Atlanta", region: "Georgia", country: "United States", lat: 33.7490, lon: -84.3880, type: "U.S. state capital" },
        { name: "Honolulu", region: "Hawaii", country: "United States", lat: 21.3070, lon: -157.8584, type: "U.S. state capital" },
        { name: "Boise", region: "Idaho", country: "United States", lat: 43.6178, lon: -116.1996, type: "U.S. state capital" },
        { name: "Springfield", region: "Illinois", country: "United States", lat: 39.7984, lon: -89.6540, type: "U.S. state capital" },
        { name: "Indianapolis", region: "Indiana", country: "United States", lat: 39.7686, lon: -86.1620, type: "U.S. state capital" },
        { name: "Des Moines", region: "Iowa", country: "United States", lat: 41.5911, lon: -93.6037, type: "U.S. state capital" },
        { name: "Topeka", region: "Kansas", country: "United States", lat: 39.0482, lon: -95.6778, type: "U.S. state capital" },
        { name: "Frankfort", region: "Kentucky", country: "United States", lat: 38.1867, lon: -84.8753, type: "U.S. state capital" },
        { name: "Baton Rouge", region: "Louisiana", country: "United States", lat: 30.4571, lon: -91.1874, type: "U.S. state capital" },
        { name: "Augusta", region: "Maine", country: "United States", lat: 44.3072, lon: -69.7817, type: "U.S. state capital" },
        { name: "Annapolis", region: "Maryland", country: "United States", lat: 38.9784, lon: -76.4922, type: "U.S. state capital" },
        { name: "Boston", region: "Massachusetts", country: "United States", lat: 42.3582, lon: -71.0637, type: "U.S. state capital" },
        { name: "Lansing", region: "Michigan", country: "United States", lat: 42.7336, lon: -84.5553, type: "U.S. state capital" },
        { name: "Saint Paul", region: "Minnesota", country: "United States", lat: 44.9551, lon: -93.1022, type: "U.S. state capital" },
        { name: "Jackson", region: "Mississippi", country: "United States", lat: 32.3038, lon: -90.1821, type: "U.S. state capital" },
        { name: "Jefferson City", region: "Missouri", country: "United States", lat: 38.5792, lon: -92.1729, type: "U.S. state capital" },
        { name: "Helena", region: "Montana", country: "United States", lat: 46.5858, lon: -112.0184, type: "U.S. state capital" },
        { name: "Lincoln", region: "Nebraska", country: "United States", lat: 40.8081, lon: -96.6997, type: "U.S. state capital" },
        { name: "Carson City", region: "Nevada", country: "United States", lat: 39.1639, lon: -119.7661, type: "U.S. state capital" },
        { name: "Concord", region: "New Hampshire", country: "United States", lat: 43.2069, lon: -71.5379, type: "U.S. state capital" },
        { name: "Trenton", region: "New Jersey", country: "United States", lat: 40.2206, lon: -74.7699, type: "U.S. state capital" },
        { name: "Santa Fe", region: "New Mexico", country: "United States", lat: 35.6822, lon: -105.9397, type: "U.S. state capital" },
        { name: "Albany", region: "New York", country: "United States", lat: 42.6528, lon: -73.7579, type: "U.S. state capital" },
        { name: "Raleigh", region: "North Carolina", country: "United States", lat: 35.7804, lon: -78.6391, type: "U.S. state capital" },
        { name: "Bismarck", region: "North Dakota", country: "United States", lat: 46.8209, lon: -100.7833, type: "U.S. state capital" },
        { name: "Columbus", region: "Ohio", country: "United States", lat: 39.9612, lon: -82.9988, type: "U.S. state capital" },
        { name: "Oklahoma City", region: "Oklahoma", country: "United States", lat: 35.4922, lon: -97.5033, type: "U.S. state capital" },
        { name: "Salem", region: "Oregon", country: "United States", lat: 44.9385, lon: -123.0304, type: "U.S. state capital" },
        { name: "Harrisburg", region: "Pennsylvania", country: "United States", lat: 40.2644, lon: -76.8836, type: "U.S. state capital" },
        { name: "Providence", region: "Rhode Island", country: "United States", lat: 41.8309, lon: -71.4149, type: "U.S. state capital" },
        { name: "Columbia", region: "South Carolina", country: "United States", lat: 34.0003, lon: -81.0332, type: "U.S. state capital" },
        { name: "Pierre", region: "South Dakota", country: "United States", lat: 44.3670, lon: -100.3464, type: "U.S. state capital" },
        { name: "Nashville", region: "Tennessee", country: "United States", lat: 36.1658, lon: -86.7842, type: "U.S. state capital" },
        { name: "Austin", region: "Texas", country: "United States", lat: 30.2747, lon: -97.7404, type: "U.S. state capital" },
        { name: "Salt Lake City", region: "Utah", country: "United States", lat: 40.7774, lon: -111.8882, type: "U.S. state capital" },
        { name: "Montpelier", region: "Vermont", country: "United States", lat: 44.2624, lon: -72.5805, type: "U.S. state capital" },
        { name: "Richmond", region: "Virginia", country: "United States", lat: 37.5389, lon: -77.4336, type: "U.S. state capital" },
        { name: "Olympia", region: "Washington", country: "United States", lat: 47.0358, lon: -122.9050, type: "U.S. state capital" },
        { name: "Charleston", region: "West Virginia", country: "United States", lat: 38.3362, lon: -81.6123, type: "U.S. state capital" },
        { name: "Madison", region: "Wisconsin", country: "United States", lat: 43.0747, lon: -89.3844, type: "U.S. state capital" },
        { name: "Cheyenne", region: "Wyoming", country: "United States", lat: 41.1403, lon: -104.8202, type: "U.S. state capital" },
        { name: "Victoria", region: "British Columbia", country: "Canada", lat: 48.4284, lon: -123.3656, type: "Canadian provincial capital" },
        { name: "Edmonton", region: "Alberta", country: "Canada", lat: 53.5461, lon: -113.4938, type: "Canadian provincial capital" },
        { name: "Regina", region: "Saskatchewan", country: "Canada", lat: 50.4452, lon: -104.6189, type: "Canadian provincial capital" },
        { name: "Winnipeg", region: "Manitoba", country: "Canada", lat: 49.8951, lon: -97.1384, type: "Canadian provincial capital" },
        { name: "Toronto", region: "Ontario", country: "Canada", lat: 43.6532, lon: -79.3832, type: "Canadian provincial capital" },
        { name: "Quebec City", region: "Quebec", country: "Canada", lat: 46.8139, lon: -71.2080, type: "Canadian provincial capital" },
        { name: "Fredericton", region: "New Brunswick", country: "Canada", lat: 45.9636, lon: -66.6431, type: "Canadian provincial capital" },
        { name: "Halifax", region: "Nova Scotia", country: "Canada", lat: 44.6488, lon: -63.5752, type: "Canadian provincial capital" },
        { name: "Charlottetown", region: "Prince Edward Island", country: "Canada", lat: 46.2382, lon: -63.1311, type: "Canadian provincial capital" },
        { name: "St. John's", region: "Newfoundland and Labrador", country: "Canada", lat: 47.5615, lon: -52.7126, type: "Canadian provincial capital" },
        { name: "Yellowknife", region: "Northwest Territories", country: "Canada", lat: 62.4540, lon: -114.3718, type: "Canadian territorial capital" },
        { name: "Iqaluit", region: "Nunavut", country: "Canada", lat: 63.7467, lon: -68.5170, type: "Canadian territorial capital" },
        { name: "Whitehorse", region: "Yukon", country: "Canada", lat: 60.7212, lon: -135.0568, type: "Canadian territorial capital" }
    ];

    const worldCapitalsUrl =
        "https://raw.githubusercontent.com/mledoze/countries/master/countries.json";
    const worldCapitalsFallbackUrl =
        "https://cdn.jsdelivr.net/gh/mledoze/countries@master/countries.json";

    async function loadCities() {
        let countries;
        for (const dataUrl of [worldCapitalsUrl, worldCapitalsFallbackUrl]) {
            try {
                const response = await fetch(dataUrl);
                if (!response.ok) {
                    throw new Error(`Capital dataset request failed: ${response.status}`);
                }
                countries = await response.json();
                break;
            } catch (error) {
                console.warn(`Could not load capital data from ${dataUrl}.`, error);
            }
        }

        // Keep the map usable when an external data host is unavailable.
        if (!countries) {
            console.warn("Using the U.S. and Canadian regional-capital list as a fallback.");
            return regionalCapitals;
        }

        const northAmericanSubregions = [
            "North America",
            "Northern America",
            "Central America",
            "Caribbean"
        ];

        const worldCapitals = countries
            .filter(country =>
                country.capital?.length &&
                country.latlng?.length === 2 &&
                northAmericanSubregions.includes(country.subregion)
            )
            .map(country => ({
                name: country.capital[0],
                country: country.name.common,
                region: country.region,
                lat: country.latlng[0],
                lon: country.latlng[1],
                type: "country capital"
            }));

        // Use the native JavaScript Map; the ArcGIS Map class is also named Map.
        const uniqueCities = new globalThis.Map();
        [...regionalCapitals, ...worldCapitals].forEach(city => {
            const key = `${city.name}|${city.lat}|${city.lon}`;
            uniqueCities.set(key, city);
        });
        return [...uniqueCities.values()];
    }

    let cities = [];

    function degreesToCompass(degrees) {
        const directions = [
            "N", "NNE", "NE", "ENE",
            "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW",
            "W", "WNW", "NW", "NNW"
        ];

        return directions[Math.round(degrees / 22.5) % 16];
    }

    function createTemperatureBubbleSymbol(temperature) {
        // The SVG tail ends at the city coordinate while the bubble sits above it.
        const bubbleSvg = `
            <svg xmlns="http://www.w3.org/2000/svg" width="76" height="48" viewBox="0 0 76 48">
                <path d="M12 2h52a10 10 0 0 1 10 10v14a10 10 0 0 1-10 10H43L38 46l-5-10H12A10 10 0 0 1 2 26V12A10 10 0 0 1 12 2Z"
                      fill="#1d3557" stroke="#ffffff" stroke-width="2"/>
                <text x="38" y="21" text-anchor="middle" dominant-baseline="middle"
                      fill="#ffffff" font-family="Arial, sans-serif" font-size="14" font-weight="700">
                    ${temperature}
                </text>
            </svg>`;

        return {
            type: "picture-marker",
            url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(bubbleSvg)}`,
            width: 38,
            height: 24,
            // Move the bubble up so the SVG tail tip is at the city location.
            yoffset: 12
        };
    }

    // OpenWeather rate-limits the free weather endpoint. Queue requests and
    // keep them below the usual 60-requests-per-minute limit.
    const weatherRequestInterval = 1100;
    let lastWeatherRequestAt = 0;
    let weatherRequestQueue = Promise.resolve();

    function requestWeather(url) {
        const request = weatherRequestQueue.then(async () => {
            const elapsed = Date.now() - lastWeatherRequestAt;
            if (elapsed < weatherRequestInterval) {
                await new Promise(resolve =>
                    setTimeout(resolve, weatherRequestInterval - elapsed)
                );
            }

            lastWeatherRequestAt = Date.now();
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Weather request failed: ${response.status}`);
            }
            return response.json();
        });

        // Keep later requests running even if one request fails.
        weatherRequestQueue = request.catch(() => undefined);
        return request;
    }

    async function updateTemperatureMarkers() {
        if (cities.length === 0) {
            // Seed the list immediately so regional markers remain available even
            // if the worldwide dataset is temporarily unreachable.
            cities = [...regionalCapitals];
            cities = await loadCities();
            console.log(`Loaded ${cities.length} capital cities.`);
        }

        const graphics = await Promise.all(
            cities.map(async city => {
                try {
                const url =
                    `https://api.openweathermap.org/data/2.5/weather` +
                    `?lat=${city.lat}&lon=${city.lon}` +
                    `&units=imperial&appid=${weatherApiKey}`;

                const weather = await requestWeather(url);

                return new Graphic({
                    geometry: {
                        type: "point",
                        longitude: city.lon,
                        latitude: city.lat
                    },
                    symbol: createTemperatureBubbleSymbol(`${Math.round(weather.main.temp)}°F`),
                    attributes: {
                        City: city.name,
                        Country: city.country,
                        Region: city.region,
                        CapitalType: city.type,
                        Temperature: `${Math.round(weather.main.temp)}°F`,
                        Conditions: weather.weather[0].description,
                        WindSpeed: `${Math.round(weather.wind.speed)} mph `,
                        WindDirection: `${Math.round(weather.wind.deg)}° (${degreesToCompass(weather.wind.deg)})`
                    },
                    popupTemplate: {
                        title: "{City}",
                        content: `
                            <b>Country:</b> {Country}<br>
                            <b>Region:</b> {Region}<br>
                            <b>Type:</b> {CapitalType}<br>
                            <b>Temperature:</b> {Temperature}<br>
                            <b>Conditions:</b> {Conditions}<br>
                            <b>Wind speed:</b> {WindSpeed}<br>
                            <b>Wind Direction:</b> {WindDirection}
                        `
                    }
                });
                } catch (error) {
                    console.warn(`Could not load weather for ${city.name}.`, error);
                    return null;
                }
            })
        );

    graphicsLayer.removeAll();
    graphicsLayer.addMany(graphics.filter(Boolean));
}

updateTemperatureMarkers();

// With hundreds of capital cities, refreshing every six hours stays within
// the typical free-tier daily request allowance.
setInterval(updateTemperatureMarkers, 21600000);

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

// Next step - making each layer toggleable and adding labels to specific geographic points for temperature, wind speeds, precipitation that turn on and off with the toggles as well. Add a key on the bottom that shows what colors mean which temperatures (may be obsolete, actually, due to temperature markers) 
// Worldwide country-capital coordinates are loaded from the maintained dataset above.
