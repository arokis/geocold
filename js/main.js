/*
function foo(url, callback) {
    httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === 4) { // request is done
            if (httpRequest.status === 200) { // successfully
                callback(httpRequest.responseText); // we're calling our method
            }
        }
    };
    httpRequest.open('GET', url, true);
    httpRequest.send();
}*/
/*
foo('http://sws.geonames.org/2813436/about.rdf', function (result) {
    console.log(result);
    document.body.innerHTML = result;
});
*/

var data = '<?xml version="1.0" encoding="UTF-8" standalone="no"?> \
    <rdf:RDF xmlns:cc="http://creativecommons.org/ns#" xmlns:dcterms="http://purl.org/dc/terms/" \
    xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:gn="http://www.geonames.org/ontology#" \
    xmlns:owl="http://www.w3.org/2002/07/owl#" \
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" \
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" \
    xmlns:wgs84_pos="http://www.w3.org/2003/01/geo/wgs84_pos#"> \
    <gn:Feature rdf:about="http://sws.geonames.org/2813436/"> \
        <rdfs:isDefinedBy rdf:resource="http://sws.geonames.org/2813436/about.rdf"/> \
        <gn:name>Weende</gn:name> \
        <gn:featureClass rdf:resource="http://www.geonames.org/ontology#P"/> \
        <gn:featureCode rdf:resource="http://www.geonames.org/ontology#P.PPL"/> \
        <gn:countryCode>DE</gn:countryCode> \
        <wgs84_pos:lat>51.56555</wgs84_pos:lat> \
        <wgs84_pos:long>9.93465</wgs84_pos:long> \
        <gn:parentFeature rdf:resource="http://sws.geonames.org/6557373/"/> \
        <gn:parentCountry rdf:resource="http://sws.geonames.org/2921044/"/> \
        <gn:parentADM1 rdf:resource="http://sws.geonames.org/2862926/"/> \
        <gn:parentADM3 rdf:resource="http://sws.geonames.org/3221013/"/> \
        <gn:parentADM4 rdf:resource="http://sws.geonames.org/6557373/"/> \
        <gn:nearbyFeatures rdf:resource="http://sws.geonames.org/2813436/nearby.rdf"/> \
        <gn:locationMap rdf:resource="http://www.geonames.org/2813436/weende.html"/> \
    </gn:Feature> \
    <foaf:Document rdf:about="http://sws.geonames.org/2813436/about.rdf"> \
        <foaf:primaryTopic rdf:resource="http://sws.geonames.org/2813436/"/> \
        <cc:license rdf:resource="http://creativecommons.org/licenses/by/3.0/"/> \
        <cc:attributionURL rdf:resource="http://sws.geonames.org/2813436/"/> \
        <cc:attributionName rdf:datatype="http://www.w3.org/2001/XMLSchema#string" \
            >GeoNames</cc:attributionName> \
        <dcterms:created rdf:datatype="http://www.w3.org/2001/XMLSchema#date" \
            >2006-01-15</dcterms:created> \
        <dcterms:modified rdf:datatype="http://www.w3.org/2001/XMLSchema#date" \
            >2015-09-04</dcterms:modified> \
    </foaf:Document> \
</rdf:RDF>';

/*
$.get("http://sws.geonames.org/2813436/about.rdf", function(data){
  console.log("Data: " + data.responseText);
});*/
let test = $.get("http://sws.geonames.org/2813436/about.rdf");
console.log(test.responseText);

