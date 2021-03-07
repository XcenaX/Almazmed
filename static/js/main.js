$(document).ready(function () {
	console.log("jquery works!");
	$("#employers-carousel").lightSlider({
		loop: true,
		addClass: "employers-carousel",
		adaptiveHeight: true,
		keyPress: true,
		controls: true,
		prevHtml: '<i class="fas fa-chevron-left slider-control"></i>',
		nextHtml: '<i class="fas fa-chevron-right slider-control"></i>',
		onSliderLoad: function () {
			$("#employers-carousel").removeClass("cS-hidden");
		},
		responsive: [
			{
				breakpoint: 1200,
				settings: {
					item: 2,
					slideMove: 1,
					slideMargin: 6,
				},
			},
			{
				breakpoint: 568,
				settings: {
					item: 1,
					slideMove: 1,
				},
			},
		],
	});

	$("#news-carousel").lightSlider({
		loop: true,
		addClass: "news-carousel",
		adaptiveHeight: true,
		keyPress: true,
		controls: false,
		onSliderLoad: function () {
			$("#news-carousel").removeClass("cS-hidden");
		},
		responsive: [
			{
				breakpoint: 1200,
				settings: {
					item: 2,
					slideMove: 1,
					slideMargin: 6,
				},
			},
			{
				breakpoint: 768,
				settings: {
					item: 1,
					slideMove: 1,
				},
			},
		],
	});

	$("#addresses-carousel").lightSlider({
		loop: true,
		item: 1,
		addClass: "addresses-carousel",
		adaptiveHeight: true,
		keyPress: true,
		controls: false,
		onSliderLoad: function () {
			$("#addresses-carousel").removeClass("cS-hidden");
		},
	});

	$("#partners-carousel").lightSlider({
		loop: true,
		item: 4,
		addClass: "partners-carousel",
		adaptiveHeight: true,
		keyPress: true,
		controls: false,
		onSliderLoad: function () {
			$("#partners-carousel").removeClass("cS-hidden");
		},
		responsive: [
			{
				breakpoint: 1200,
				settings: {
					item: 3,
					slideMove: 1,
					slideMargin: 6,
				},
			},
			{
				breakpoint: 768,
				settings: {
					item: 2,
					slideMove: 1,
				},
			},
			{
				breakpoint: 568,
				settings: {
					item: 1,
					slideMove: 1,
				},
			},
		],
	});
});

$("#main-carousel").lightSlider({
	loop: true,
	item: 1,
	auto: true,
	pauseOnHover: true,
	pause: 4000,
	addClass: "main-carousel",
	prevHtml: '<i class="fas fa-chevron-left slider-control"></i>',
	nextHtml: '<i class="fas fa-chevron-right slider-control"></i>',
	adaptiveHeight: true,
	keyPress: true,
	controls: true,
	onSliderLoad: function () {
		$("#main-carousel").removeClass("cS-hidden");
	},
});

function switchAddressType() {
	let slider = document.getElementById("switch");
	let labels = document.getElementsByClassName("switch-label");
	let list = document.getElementsByClassName("address-section__cards-list")[0];
	let map = document.getElementById("map");
	let carousel = document.getElementById("addresses-carousel");
	let pager = document.querySelector(".addresses-carousel > .lSPager");

	if (slider.checked) {
		labels[0].style.color = "#78d1b6";
		labels[1].style.color = "#333";
		if (window.matchMedia("(max-width: 768px)").matches) {
			//carousel.style.display = "block";
			//pager.style.display = "block";
			list.style.display = "block";
		} else {
			list.style.display = "block";
		}
		map.style.display = "none";
	} else {
		labels[0].style.color = "#333";
		labels[1].style.color = "#78d1b6";
		if (window.matchMedia("(max-width: 768px)").matches) {
			//carousel.style.display = "none";
			//pager.style.display = "none";
			list.style.display = "none";
		} else {
			list.style.display = "none";
		}
		map.style.display = "block";
	}
}

function openMenuPage(clicked) {
	let page = document.getElementById("menu-page");
	if (clicked === "menu-page-button") {
		page.style.display = "grid";
	} else {
		page.style.display = "none";
	}
}

let carets = document.querySelectorAll(".menu-page-item .fa-caret-down");
Array.from(carets).forEach((element, index) => {
	element.addEventListener(
		"click",
		() => {
			let dropdownContent = document.getElementsByClassName("dropdown-content");
			dropdownContent[index].style.display =
				dropdownContent[index].style.display === "block" ? "none" : "block";
			element.style.transform =
				element.style.transform === "rotate(180deg)"
					? "rotate(0deg)"
					: "rotate(180deg)";
		},
		false
	);
});
// CALLBACK MODAL
let callbackModal = document.getElementById("callback-modal");
let closeCallbackModal = document.querySelector(
	"#callback-modal > .modal-content > .close-button"
);
let callbackBlocks = document.querySelectorAll(".callback-block > span");
let callbackButtons = document.querySelectorAll(".callback-button");

Array.from(callbackBlocks).forEach((el, index) => {
	el.addEventListener(
		"click",
		() => {
			callbackModal.style.display = "block";
		},
		false
	);
});
Array.from(callbackButtons).forEach((el, index) => {
	el.addEventListener(
		"click",
		() => {
			callbackModal.style.display = "block";
		},
		false
	);
});
closeCallbackModal.addEventListener(
	"click",
	() => {
		callbackModal.style.display = "none";
	},
	false
);

// ONLINE ORDER MODAL
let orderButtons = document.querySelectorAll(".online-order-button");
let orderModal = document.getElementById("online-order-modal");
let closeOrderModal = document.querySelector(
	"#online-order-modal > .modal-content > .close-button"
);

Array.from(orderButtons).forEach(element => {
	element.addEventListener(
		"click",
		() => {
			orderModal.style.display = "block";
		},
		false
	);
});

closeOrderModal.addEventListener(
	"click",
	() => {
		orderModal.style.display = "none";
	},
	false
);

let closeReceiptModal = document.querySelector("#receipt-modal .close-button");
let receiptButtons = document.querySelectorAll(".order-receipt");
let receiptModal = document.getElementById("receipt-modal");

Array.from(receiptButtons).forEach(element => {
	element.addEventListener(
		"click",
		() => {
			receiptModal.style.display = "block";
		},
		false
	);
});
closeReceiptModal.addEventListener(
	"click",
	() => {
		receiptModal.style.display = "none";
	},
	false
);

// FIXED NAVBAR
let navbar = document.getElementById("fixed-navbar");
let sticky = navbar.offsetTop;

function myFunction() {
	if (window.pageYOffset >= sticky) {
		navbar.classList.add("sticky");
	} else {
		navbar.classList.remove("sticky");
	}
}
// SEARCH MODAL
let searchIcons = document.getElementsByClassName("search-icon");
let searchModal = document.getElementById("search-modal");
let closeSearchModal = document.querySelector("#search-modal .close-button");

Array.from(searchIcons).forEach(element => {
	element.addEventListener(
		"click",
		() => {
			searchModal.style.display = "block";
		},
		false
	);
});
closeSearchModal.addEventListener(
	"click",
	() => {
		searchModal.style.display = "none";
	},
	false
);

// WINDOW ONCLICK
window.onclick = function (event) {
	if (event.target === callbackModal) {
		callbackModal.style.display = "none";
	} else if (event.target === orderModal) {
		orderModal.style.display = "none";
	} else if (event.target === receiptModal) {
		receiptModal.style.display = "none";
	} else if (event.target === searchModal) {
		searchModal.style.display = "none";
	}
};

// GO UP BUTTON
goUpButton = document.getElementById("go-up-button");

function scrollFunction() {
	if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
		goUpButton.style.display = "block";
	} else {
		goUpButton.style.display = "none";
	}
}
function goToTop() {
	document.body.scrollTop = 0; // For Safari
	document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

// Window onscroll
window.onscroll = function () {
	myFunction();
	scrollFunction();
};
