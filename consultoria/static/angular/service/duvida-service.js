;(function() {
	"use strict";

	angular.module("consultoria").service("DuvidaService", DuvidaService)

	DuvidaService.$inject = ['$rootScope', '$http', '$q', '$state', 'Notification'];

	function DuvidaService($rootScope, $http, $q, $state, Notification) {
		var _observers = [];
		var service = {
			buscar : buscar,
			listar : listar,
			totalDuvidas : totalDuvidas,
			listarAdmin : listarAdmin
		};

		return service;

		function listar() {
			return $http.get("/duvidas/").then(function(response) {
				return response.data;
			})
		}

		function listarAdmin() {
			return $http.get("/admin/duvidas/").then(function(response) {
				return response.data;
			})
		}
		
		function totalDuvidas() {
			return $http.get("/totalDuvidas/").then(function(response) {
				return response.data;
			})
		}
				
		function buscar(id) {
			var deferred = $q.defer()
			$http.get('/duvidas/' + id).then(function(response) {
				deferred.resolve(response.data);
			}, function() {
				Notification.error("Erro ao consultar dúvida")
				deferred.reject();
			})
			return deferred.promise;
		}

	}

})();