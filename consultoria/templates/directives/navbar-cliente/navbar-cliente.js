(function() {
	"use strict";

	/**
	 * @desc diretiva de base para o navbar
	 * @example <navbar-cliente></navbar-cliente>
	 */

	angular.module("consultoria").directive("navbarCliente", Navbar)

	function Navbar() {
		return {
			restrict : "E",
			replace : true,
			templateUrl : "/templates/directives/navbar-cliente/navbar-cliente.html",
			controller : "NavbarController",
			controllerAs : "NavbarCtrl"
		}
	}

})()
