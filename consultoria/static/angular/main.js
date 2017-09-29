(function() {
	'use strict';

	angular.module('consultoria', [ 'ngRoute', 'ui.bootstrap', 'ui.router', 'ui-notification', 'ui.mask', 'duScroll' ])

	.config([ '$stateProvider', '$urlRouterProvider' , '$provide', '$uibTooltipProvider', config ])

	.run(function($http, $rootScope) {
		init();

		function init() {
			$rootScope.submitPromise = { message:"Aguarde..." };
		}
	});

	function config($stateProvider, $urlRouterProvider, $provide, $uibTooltipProvider) {
		
		var session = function(LoginService, $stateParams, $state) {
			return LoginService.logged().then(function(response) {				
				return response;
				$state.go("app.conta");
			}, function(response) {
				console.log(response)
				return false;
			});
		};
		
		$provide.decorator('$state', function($delegate, $rootScope) {
		    $rootScope.$on('$stateChangeStart', function(event, state, params, from, fromParams) {
		    	$delegate.next = state;
		    	$delegate.toParams = params;
		    	$delegate.from = from;
		    	$delegate.fromParams = fromParams;
		    });
		    
		    return $delegate;
		 });
		
		// For unmatched routes
		$urlRouterProvider.otherwise('/index/start');
//		$urlRouterProvider.when('/app/', '/app/conta');

		// Application routes
		$stateProvider.state('index', {
			url : '/index',
			controller : 'PresentationController',
			controllerAs : 'PresentCtrl',
			templateUrl : '/templates/presentation/base.html',
		}).state('index.start', {
			url : '/start',
			templateUrl : '/templates/presentation/start.html'
		}).state('app', {
			url : '/app',
			templateUrl : '/app/cliente/base.html',
			resolve : {
				LoginService : "LoginService",
				session : session
			}
		}).state('app.planos', {
			url : '/planos',
			templateUrl : '/app/cliente/planos.html',
			controller : 'ClientePlanoController',
			controllerAs : 'CliPlanCtrl'
		}).state('app.treinos', {
			url : '/treinos',
			templateUrl : '/app/cliente/treinos.html',
			controller : 'ClienteTreinoController',
			controllerAs : 'CliTreCtrl'
		}).state('app.duvidas', {
			url : '/duvidas',
			templateUrl : '/app/cliente/duvidas.html',
			controller : 'ClienteDuvidaController',
			controllerAs : 'CliDuvidaCtrl'
		}).state('app.conta', {
			url : '/conta',
			templateUrl : '/app/cliente/conta.html',
			controller : 'ClienteContaController',
			controllerAs : 'CliContaCtrl'
		}).state('admin', {
			url : '/admin',
			templateUrl : '/app/admin/base.html',
			resolve : {
				session : session
			}
		}).state('admin.usuarios', {
			url : '/usuarios',
			templateUrl : '/app/admin/usuarios.html',
			controller : 'AdminUsuarioController',
			controllerAs : 'UsuarioCtrl'
		});
	}

})();
