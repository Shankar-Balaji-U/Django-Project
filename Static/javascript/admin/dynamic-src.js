function getViewportSize() {
	
	var vw = screen.width;
	const sm = 576, md = 768, lg = 992, xl = 1200;

	if(sm > vw) {
		return 'sm';
	}
	if(vw < md && vw >= sm) {
		return 'md';
	}
	if(vw < lg && vw >= md) {
		return 'lg';
	}
	if(vw < xl && vw >= lg) {
		return 'xl';
	}
	if(vw >= xl) {
		return 'xxl';
	}
}

function setViewportLocal(value) {
	localStorage.setItem("viewport-size", value);
}

function changeImageTagSrc() {
	let image_url; 
	const all_image_tag = document.getElementsByTagName('img');

	for(let i=0; i < all_image_tag.length; i++) {
		let raw_json = all_image_tag[i].dataset['src'];
		if(raw_json) {
			let json_data = JSON.parse(raw_json);
			image_url = json_data.og;
			switch (getViewportSize()) {
				case 'sm':
					image_url = json_data.sm;
					break;
				case 'md':
					image_url = json_data.md;
					break;
				case 'lg':
					image_url = json_data.lg;
					break;
			}
			all_image_tag[i].src = image_url;
		}
	}
}



window.addEventListener('resize', function(){
	setViewportLocal(getViewportSize());
	changeImageTagSrc()
});

window.addEventListener('DOMContentLoaded', (event) => {
    setViewportLocal(getViewportSize());
	changeImageTagSrc();
});