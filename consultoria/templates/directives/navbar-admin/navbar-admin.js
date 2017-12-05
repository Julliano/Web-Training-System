;(function() {
	"use strict";

	/**
	 * @desc diretiva de base para o navbar
	 * @example <navbar></navbar>
	 */

	angular.module("consultoria").directive("navbarAdmin", NavbarAdmin)

	function NavbarAdmin() {
		return {
			restrict : "E",
			replace : true,
			templateUrl : "/templates/directives/navbar-admin/navbar-admin.html",
			controller : "NavbarController",
			controllerAs : "NavbarCtrl"
		}
	}

})();
