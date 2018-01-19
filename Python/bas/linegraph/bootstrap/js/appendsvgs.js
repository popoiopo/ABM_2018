d3.xml("svg/svg_floor1.svg", "image/svg+xml", function(error, xml) {
    if (error) throw error;
    console.log(xml);
    document.getElementById("heatmaps-floor-1").appendChild(xml.documentElement)
});

d3.xml("svg/svg_floor2.svg", "image/svg+xml", function(error, xml2) {
    if (error) throw error;
    console.log(xml2);
    document.getElementById("heatmaps-floor-2").appendChild(xml2.documentElement)
});

d3.xml("svg/svg_floor3.svg", "image/svg+xml", function(error, xml3) {
    if (error) throw error;
    console.log(xml3);
    document.getElementById("heatmaps-floor-3").appendChild(xml3.documentElement)
});
