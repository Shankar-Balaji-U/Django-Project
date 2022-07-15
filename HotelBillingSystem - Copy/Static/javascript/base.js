/*
Breakpoint			Class infix			Dimensions
X-Small				None				<576px
Small				sm					≥576px
Medium				md					≥768px
Large				lg					≥992px
Extra				large xl			≥1200px
Extra extra			large xxl			≥1400px

576 > width < 768 && width >= 576 width < 992 && width >= 768 width < 1200 && width >= 992 width < 1400 && width >= 1200 width >= 1400

*/

// need to attach jQuery

const mobileInit = 0.6, tabletInit = 0.86, deskInit = 1;

const mobileView = `width=device-width, initial-scale=${mobileInit}, maximum-scale=5.0, minimum-scale=${mobileInit}, user-scalable=yes`;
const tabletView = `width=device-width, initial-scale=${tabletInit}, maximum-scale=2.5, minimum-scale=${tabletInit}, user-scalable=yes`;
const deskView = `width=device-width, initial-scale=${deskInit}, maximum-scale=1`;
const S = 576, M = 768, L = 992, EL = 1200, EXL = 1400;     // viewport sizes

const changeMetaTag = function() {
	var vw = screen.width;
	if(S > vw) {
		$("meta[name=viewport]").attr("content", mobileView);		// lesser than 576
	}
	if(vw < M && vw >= S) {
		$("meta[name=viewport]").attr("content", mobileView);		// lesser than 768 and greater than 576
	}
	if(vw < L && vw >= M) {
		$("meta[name=viewport]").attr("content", tabletView);		// lesser than 992 and greater than 768
	}
	if(vw < EL && vw >= L) {
		$("meta[name=viewport]").attr("content", tabletView);		// lesser than 1200 and greater than 992
	}
	if(vw < EXL && vw >= EL) {
		$("meta[name=viewport]").attr("content", deskView);		// lesser than 1400 and greater than 1200
	}
	if(vw >= EXL) {
		$("meta[name=viewport]").attr("content", deskView);		// greater than 1400
	}
}
// $(window).on("load resize", changeMetaTag);









var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (e) {
	return new bootstrap.Tooltip(e)
});

const getCurrentTheme = function() {
	const t = window.matchMedia("(prefers-color-scheme: dark)");
	if (t.matches) {
		return 'dark';
	} else {
		return 'light';
	}
}
console.log("My current theme: " + getCurrentTheme());
