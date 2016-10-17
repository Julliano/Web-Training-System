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
			}, function(response) {
				$state.go("index.signin");
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
		//$urlRouterProvider.when('/app/operacoes', '/app/consultar');

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
				session : session
			}
		}).state('app.consultar', {
			url : '/consultar',
			templateUrl : '/app/cliente/consultar.html',
			controller : 'ClienteConsultaController',
			controllerAs : 'CliConCtrl'
			/*resolve : {
				operacoes : operacoes
			}*/
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
		}).state('admin.consultar', {
			url : '/consultar',
			templateUrl : '/app/admin/consultar.html',
			controller : 'ConsultarController',
			controllerAs : 'ConsultaCtrl'
		}).state('admin.usuarios', {
			url : '/usuarios',
			templateUrl : '/app/admin/usuarios.html',
			controller : 'AdminUsuarioController',
			controllerAs : 'UsuarioCtrl'
		});
	}

})();
