var mr=new Object(khtml.maplib);
var map;
let mindex = {}
//let mindex2 = []


function initMap(){
	console.log('initialising Map ...');
	map = new mr.Map(document.getElementById('map'));
	var center = new mr.LatLng(0,0);  //latitude, longitude
	map.centerAndZoom(new mr.LatLng(35, 25),2.5); //1.5 = zoomlevel
	
	/*
	let myLatlng = new mr.LatLng(50.875311,0.351563);
	let standard = new mr.overlay.Marker({
		position: myLatlng, 
		map: map,
		title:'ghjg'
	});*/

	// testmarker with GeoCoLD Pin - moveable
	//marker = geocoldMarker('test', 51.875311, 0.351563);
	//let marker2 = geocoldMarker('test', 50.875311, 0.351563);

	
	console.log('successfully initialised!');
};


let guidGenerator = function () {
    let S4 = function() {
       return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    };
    return ("m"+S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
};


let plotter = function (item) {
	if (item['type'] == 'place'){
		let geo_obj = new Geo(item);
		geo_obj.registerToDict(mindex)
		//geo_obj.registerToArray(mindex2);
		geo_obj.setMarker();
		//geo_obj.setEntry('#identified tbody');
		geo_obj.setListItem('#id-places')
	} else {
			console.log('create an entry for unknown Entity "' + item['uri'] + '"')
			setUnknown(item);
		};
	};


let setUnknown = function (entity) {
	let uri = entity['uri'];
	$('#unknown tbody').append('<tr><td><a href="'+uri+'">'+uri+'</a> <sub>(class: <a href="' + entity['cls'] + '">' + entity['cls'] + '</a>)</sub></td></tr>');
};


let test = function() {
	let obj = {
		'label' : 'Kuhberg',
		'lat':	51.3,
		'long': 9.4,
	};
	let kuh = new Geo(obj);
	kuh.registerToDict(mindex);
	kuh.setMarker();
	kuh.setEntry('#identified tbody');
	//marker2 = geocoldMarker('test', 50.875311, 0.351563);
};


// naive and just for testing;-)
$(document).on( 'click', '.marker-button', function() {
	//console.log('test')
	let marker_id = '#' + $(this).attr('data-marker'); 
	console.log( marker_id );
	$(marker_id).toggle(400);

});

/*****************************/
/*		Markers				 */
/*****************************/
let standardMarker = function (label, lat, long) {
	let myLatlng = new mr.LatLng(lat,long);
	let standard = new mr.overlay.Marker({
		position: myLatlng, 
		map: map,
		title:label
	});
	return standard;
};


let geocoldMarker = function (label, lat, long) {
	let myLatlng = new mr.LatLng(lat,long);
	
	// defines icon
	let image = new mr.overlay.MarkerImage(
	  "/static/img/marker.png",
	  //"/static/img/marker_shadow.png",
	  {width: 20,height: 32}, //marker.png
	  //{width: 40,height: 30}, //marker_shadow.png
	  {x: 0,y:0},
	  //{x:11,y:28} //marker_shadow.png
	  {x:10,y:33} //marker.png
	);

	// defines shadow
	let shadow = new mr.overlay.MarkerImage(
	  'img/shadow.png',
	  {width:34,height:20},
	  {x:0,y:0},
	  {x:10,y:20}
	);
	
	// defines shape	
	let shape = {
	  coord: [14,0,15,1,16,2,17,3,18,4,19,5,19,6,19,7,19,8,19,9,19,10,19,11,19,12,19,13,19,14,18,15,17,16,16,17,15,18,13,19,5,19,4,18,2,17,2,16,1,15,0,14,0,13,0,12,0,11,0,10,0,9,0,8,0,7,0,6,0,5,1,4,2,3,2,2,4,1,5,0,14,0],
	  type: 'poly'
	};

	// construct marker
	let marker = new mr.overlay.Marker({
	  draggable: true,
	  raiseOnDrag: true,
	  icon: image,
	  //shadow: shadow,
	  //shape: shape,
	  map: map,
	  position: myLatlng,
	  title: label
	});
	return marker;
};


let customMarker = function(label, lat, long, stuff) {
	let custom = new mr.overlay.Marker({
		position: new mr.LatLng(lat,long),
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
		//draggable: true,
		title: label,
		map: map
	});
	return custom;
}   


/*****************************
#		Classes				 #
******************************

- Geo(): a GEOCOLD JavaScript Geo-Object-Representation
- Loading(): Geocold Loading-Bar refreshing the request status

******************************/

function Geo(obj){
	console.log('create Geo-Object "' + obj['label'] + '" and plott it to map')
	this.key = guidGenerator()
	this.uri = obj['uri'];
	this.label = obj['label'];
	this.lat = obj['lat'];
	this.long = obj['long'];
	this.marker = false

	this.registerToArray = function (array) {
		array.push(this);
	};

	this.registerToDict = function (dict) {
		console.log('register "' + this.label + '" to Dict-Index')
		dict[this.key] = this;
	};

	this.deleteMarker = function () {
		if (this.marker != false) {
			console.log('delete "' + this.label + '" from map')
			this.marker.destroy();
			this.marker = false;
			console.log(this)
		} else {
			console.log('no marker for "' + this.label + '" to delete')
		};
	};

	this.setMarker = function() {
		if (this.marker == false) {
			console.log('plott "' + this.label + '" to map')
			this.marker = standardMarker(this.label, this.lat, this.long);
			//this.marker = geocoldMarker(this.label, this.lat, this.long);
			this.marker.marker.setAttribute('id', this.key)
		} else {
			console.log('a marker for "' + this.label + '" already exists on map')
		};
		console.log(this)
	};

	this.setEntry = function(element) {
		console.log('create an entry for Place "' + this.label + '"')
		let long = this.marker.position.longitude;
		let lat = this.marker.position.latitude;
		$(element).append('<tr><td><a href="'+this.key+'">'+this.label+'</a></td><td><a href="'+this.uri+'">'+this.uri+'</a></td><td>'+long+', '+lat+'</td></tr>');
	};

	this.setListItem = function (element_id) {
		let item = document.createElement('li')
		item.setAttribute('class', 'list-group-item');
		let label = '<span style="margin-right: 20px;"><strong>' + this.label + '</strong></span> <i class="fa fa-home" aria-hidden="true"></i>: <span><a href="' + this.uri + '">' + this.uri + '</a></span>';
		$(item).append(label);

		let subList = document.createElement('ul')
		subList.setAttribute('class', 'list-unstyled');
		subList.setAttribute('style', 'margin-top:10px;')
		
		/*
		let uri_list = document.createElement('li');
		let uri_icon = '<i class="fa fa-home" aria-hidden="true" style="margin-right: 10px"></i>';
		$(uri_list).append(uri_icon);
		let uri_text = '<span><a href="' + this.uri + '">' + this.uri + '</a></span>';
		$(uri_list).append(uri_text)
		*/

		let coor_list = document.createElement('li');
		let coor_icon = '<i class="fa fa-map-marker marker-button" data-marker="' + this.key + '" aria-hidden="true" style="color: #64B2CC; margin-right:5px; font-size: 17px;"></i> ';
		$(coor_list).append(coor_icon);
		let long = this.marker.position.longitude;
		let lat = this.marker.position.latitude;
		let coor_text = lat + ' (latitude), ' + long + ' (longitude)';
		//let coor_ref = '<button class="marker-button" data-marker="' + this.key + '">' + this.key + '</button>'
		$(coor_list).append(coor_text)
		//$(coor_list).append(coor_ref)

		//$(subList).append(uri_list)
		$(subList).append(coor_list)

		$(item).append(subList);
		$(element_id).append(item);
	};
};


function Loading(total){
	this.n = 1;
	this.total = total
	this.bar = '#gc-lookup'
	this.current = 0;

	this.create_bar = function(parent) {
		let par_div = document.createElement('div');
		$(par_div).attr('class', 'progress');
		$(par_div).css('height', '3px');
		$(par_div).append('<div id="gc-lookup" class="progress-bar progress-bar-warning" role="progressbar" style="width: 0%;color: black;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">0%</div>');
		$(parent).append(par_div);
	};

	this.refresh = function() {
		// Kehrwert mal 100 
		this.current = (this.n / this.total) * 100;
		console.log(this.current + ' % done');
		this.process();
		this.n += 1;
	};

	this.process = function () {
		let percentage = Math.round(this.current) + '%';
		$(this.bar).css('width', percentage);
		$(this.bar).text(this.n + ' / ' + this.total + ' done (' + percentage + ')');
		if (this.current == 100) {
			$(this.bar).removeClass('progress-bar-warning');
			$(this.bar).addClass('progress-bar-success'); 
			console.log(this.current);
			//this.kill();
		};
	};

	this.kill = function () {
		$(this.bar).remove();
	};
}; 