var mr=new Object(khtml.maplib);
var map;


function initGeoCoLD(){
	map=new mr.Map(document.getElementById("map"));  //dom element
	
	var center=new mr.LatLng(0,0);  //latitude, longitude
	map.centerAndZoom(new mr.LatLng(35, 25),2.5); //1.5 = zoomlevel
	
	// define position
	var point = new mr.LatLng(50.875311, 0.351563);
	// define icon
	var image = new mr.overlay.MarkerImage(
	  'img/image.png',
	  {width: 20,height: 20},
	  {x: 0,y:0},
	  {x:10,y:20}
	);
	// define shadow
	var shadow = new mr.overlay.MarkerImage(
	  'img/shadow.png',
	  {width:34,height:20},
	  {x:0,y:0},
	  {x:10,y:20}
	);
	
    /*
		// static marker on Mt. Uluru/Australia
	var myLatlng = new mr.LatLng(51.61667,9.93333);
	var marker2 = new mr.overlay.Marker({
        position: myLatlng, 
        map: map,
        title:"static marker on Mt. Uluru/Australia"
    });
    */
    
    		// Test
	var myLatlng = new mr.LatLng(-20.363882,20.044922);
	var marker2 = new mr.overlay.Marker({
        position: myLatlng, 
        map: map,
        title:"uninteressanter Ort zu Testzwecken"
    });
	
	
	// define shape
/*	var shape = {
	  coord: [14,0,15,1,16,2,17,3,18,4,19,5,19,6,19,7,19,8,19,9,19,10,19,11,19,12,19,13,19,14,18,15,17,16,16,17,15,18,13,19,5,19,4,18,2,17,2,16,1,15,0,14,0,13,0,12,0,11,0,10,0,9,0,8,0,7,0,6,0,5,1,4,2,3,2,2,4,1,5,0,14,0],
	  type: 'poly'
	};
	*/

// moveable marker
/*	var marker = new mr.overlay.Marker({
	  draggable: true,
	  raiseOnDrag: true,
	  icon: image,
	  shadow: shadow,
	  shape: shape,
	  map: map,
	  position: point,
	  title: "moveable marker"
	});
	*/
	
	
	// moveable custom marker with shadow
/*	var marker3 = new mr.overlay.Marker({
			position: new mr.LatLng(center),
			icon: {
				url: "http://maps.gstatic.com/intl/de_de/mapfiles/ms/micons/red-pushpin.png",
				size: {width:26,height:32},
				origin: {x:0,y:0},
				anchor: {
					x:"-10px",
					y:"-32px"
				}
			},
			shadow: {
				url: "http://maps.gstatic.com/intl/de_de/mapfiles/ms/micons/pushpin_shadow.png",
				size: {
					width:"40px",
					height:"32px"
				},
				origin: {x: 0,y: 0},
				anchor: {x: 0,y: -32}
			},
			draggable: true,
			title: "moveable marker",
			map: map
		});
*/
	
	/*
	//DOM-element as marker
	var p=document.createElement("span");
	p.innerHTML="Hello World!";
	var marker4 = new mr.overlay.Marker({
		position: new mr.LatLng(center),
		//icon:{
		//	url:p
		//},
		//raiseOnDrag: false,
		map: map, 
		title:"DOM-element"
	});
	map.addOverlay(marker4);
	//marker4.makeMoveable(); 
	*/
	/*
	// another DOM-element marker with css-styles
	var div=document.createElement("div");
	var marker5 = new mr.overlay.Marker({position: new mr.LatLng(-20,-20), icon:div, raiseOnDrag: false, title: "DOM-element"});
	map.addOverlay(marker5);
	div.style.height = "20px";
	div.style.width = "20px";
	div.style.backgroundColor="red";
	//marker5.makeMoveable();
	*/
}


let test = function() {
	
	var myLatlng = new mr.LatLng(51.3,9.4);
		var marker2 = new mr.overlay.Marker({
			position: myLatlng, 
			map: map,
			title:"Kuhberg"
		});
	
	let par = $('body area').parent()
	console.log(par)
}


let plottResponse = function (list) {
    for ($i = 0; $i < list.length; $i++){
        let geo_mark = list[$i]
        setMarker(geo_mark);
		
		let par = $('body area').parent().last()
		let marker_id = par.attr('id')
		par.parent().attr('data-id', marker_id)
		//console.log(par.parent().attr('data-id'))
		
		setEntry('#identified tbody', geo_mark, marker_id);
		//console.log(par.parent('div'))
    };
}


let setMarker = function (place) {
        let label = place['label']
        let long = place['coordinates']['long']
        let lat = place['coordinates']['lat']
        /*
        console.log('Label: ' + place['label'])
        console.log('Long.: ' + place['coordinates']['long'])
        console.log('Lat. : ' + place['coordinates']['lat'])
        */
        var myLatlng = new mr.LatLng(lat,long);
		var marker2 = new mr.overlay.Marker({
			position: myLatlng, 
			map: map,
			title:label
		});
}


let setEntry = function (element, place, mark_id) {
	let uri = place['uri']
	let label = place['label']
	let long = place['coordinates']['long']
	let lat = place['coordinates']['lat']
	$(element).append('<tr><td><a href="'+mark_id+'" data-mark="'+mark_id+'">'+label+'</a></td><td>'+uri+'</td><td>'+long+', '+lat+'</td></tr>');
}
