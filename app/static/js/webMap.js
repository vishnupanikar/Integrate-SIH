      require([
        "esri/config",
        "esri/Map",
        "esri/WebMap",
        "esri/views/MapView",
        "esri/portal/Portal",
        "esri/layers/FeatureLayer",
        "esri/widgets/FeatureTable",
        "esri/layers/CSVLayer",
        "esri/renderers/SimpleRenderer",
        "esri/symbols/SimpleMarkerSymbol",
        "esri/core/urlUtils",

        "esri/widgets/BasemapGallery",
        "esri/widgets/BasemapToggle",
        "esri/widgets/Locate",
        "esri/widgets/Search",
        "esri/widgets/CoordinateConversion",
        "esri/widgets/LayerList",
        "esri/widgets/Legend",
        "esri/widgets/Expand",
        "dojo/domReady!"
      ],
      function (
            esriConfig,
            Map,
            WebMap,
            MapView,
            Portal,
            FeatureLayer,
            FeatureTable,
            CSVLayer,
            SimpleRenderer,
            SimpleMarkerSymbol,
            urlUtils,
            BasemapGallery,
            BasemapToggle,
            Locate,
            Search,
            CoordinateConversion,
            LayerList,
            Legend,
            Expand){
//PART01:
                let RiverTracingWebMapId = "bee4f67960a040c79aad67e1810b70d4";
                if (window.location.href.indexOf("?id=") > 0) {
                  RiverTracingWebMapId = window.location.href.split("?id=")[1];
                }
                var map = new WebMap({
                  portalItem: {
                    id: RiverTracingWebMapId
                  }
                });
                var view = new MapView({
                  map: map,
                  container: "viewDiv",
                  //center: [78.9629 , 20.5937],
                  //zoom: 4
                });
                esriConfig.portalUrl = "https://mjzaid921pccoer.maps.arcgis.com";

//PART02:
                view.ui.add("logoDiv", "bottom-left");
//PART03:
                var searchWidget = new Search({
                  view: view
                });
                view.ui.add(searchWidget, {
                  position: "top-right"
                });
//PART04:
                var locateBtn = new Locate({
                  view: view
                });
                view.ui.add(locateBtn, {
                  position: "top-left"
                });
//PART05:
                view.ui.add(
                  [
                    new Expand({
                      content: new Legend({
                        view: view
                      }),
                      view: view,
                      group: "top-left"
                    }),
                    new Expand({
                      content: new LayerList({
                        view: view
                      }),
                      view: view,
                      group: "top-left"
                    }),
                    new Expand({
                      content: new BasemapGallery({
                        view: view
                      }),
                      view: view,
                      expandIconClass: "esri-icon-basemap",
                      group: "top-left"
                    }),
                    new Expand({
                      content: new BasemapToggle({
                          view: view,
                          nextBasemap: "hybrid"
                      }),
                      view: view,
                      expandIconClass: "esri-icon-media",
                      group: "top-left"
                    }),
                    new Expand({
                    content:new CoordinateConversion({
                      view: view
                    }),
                    view: view,
                      expandIconClass: "esri-icon-experimental",
                      group: "top-left"
                    })
                  ],
                  "top-left"
                );
//PART06:
                var layer = new FeatureLayer({
                    url: "https://services.arcgis.com/fzIHTcK9TqzWXLVL/arcgis/rest/services/layer_pointsriverfront/FeatureServer/0"
                });
                map.layers.add(layer);
//PART07:
                const url ="/static/surveyData.csv";
                const csvLayer = new CSVLayer({
                title: "Survey Data",
                  url: url,
                  copyright: "mjzaid921pccoer"
                });
                map.layers.add(csvLayer);
            }
      );
/*
<div id="viewDiv"></div>
<div id="logoDiv" class="esri-widget">Team HEXA_BYTE</div>
<!--"":"f48c3220d0e1404ebbf6707c54d5d2fe",
    "River Tracing WebMap":"bee4f67960a040c79aad67e1810b70d4",
    "WebMap_WaterBodies_Topographic":"23bc5f282ec848adb1ee2610d2408e51"
-->
*/