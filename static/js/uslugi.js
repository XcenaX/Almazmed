let sidebarCarets = document.querySelectorAll(
	".sidebar-menu__item .fa-caret-down"
);
Array.from(sidebarCarets).forEach((element, index) => {
	element.addEventListener(
		"click",
		() => {
			let dropdownContent = document.getElementsByClassName(
				"dropdown-link__content"
			);
			dropdownContent[index].style.display =
				dropdownContent[index].style.display === "block" ? "none" : "block";
			if (element.style.transform.includes("rotate(180deg)")) {
				element.style.transform = "translateY(-50%) rotate(0deg)";
			} else {
				element.style.transform = "translateY(-50%) rotate(180deg)";
			}
		},
		false
	);
});

let panelSubmenuIcons = document.getElementsByClassName("submenu-icon");

Array.from(panelSubmenuIcons).forEach((element, index) => {
	element.addEventListener(
		"click",
		() => {
			let dropdownContent = document.getElementsByClassName(
				"panel__item-submenu-list"
			);
			dropdownContent[index].style.display =
				dropdownContent[index].style.display === "grid" ? "none" : "grid";

			let chevron = document.querySelectorAll(".submenu-icon div");
			chevron[index].style.transform =
				chevron[index].style.transform === "rotate(180deg)"
					? "rotate(0deg)"
					: "rotate(180deg)";

			let span = element.querySelectorAll("span")[0];
			let spanHide = element.querySelector(".close-span");
			if (span.style.display === "none") {
				spanHide.style.display = "none";
				span.style.display = "block";
			} else {
				spanHide.style.display = "block";
				span.style.display = "none";
			}
		},
		false
	);
});
