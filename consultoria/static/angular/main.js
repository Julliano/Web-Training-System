(function() {
	'use strict';

	angular.module('consultoria', [ 'ngRoute', 'ui.bootstrap', 'ui.router', 'ui-notification', 'ui.mask', 'duScroll', 'textAngular', 'checklist-model', 'angular-bind-html-compile', 'ngAnimate', 'angular-loading-bar', 'ngSanitize'])

	.config([ '$stateProvider', '$urlRouterProvider' , '$provide', '$uibTooltipProvider', 'cfpLoadingBarProvider', config ])

	/* @ngInject */
	.run(function($http, $rootScope) {
		init();

		function init() {
			$rootScope.submitPromise = { message:"Aguarde..." };
		}
	});

	/* @ngInject */
	function config($stateProvider, $urlRouterProvider, $provide, $uibTooltipProvider, cfpLoadingBarProvider) {
		
		var session = function(LoginService, $stateParams, $state) {
			return LoginService.logged().then(function(response) {				
				return response;
			}, function(response) {
				$state.go("index.start");
				return false;
			});
		};
		
		var duvida = function(DuvidaService, $stateParams) {
			return DuvidaService.buscar($stateParams.id);
		};

		var form = function(FormService, $stateParams) {
			return FormService.buscar($stateParams.id);
		};
		
		var treino = function(TreinoService, $stateParams) {
			return TreinoService.buscar($stateParams.id);
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
		$urlRouterProvider.when('/app/', '/app/treinos');

		// Application routes
		$stateProvider.state('index', {
			url : '/index',
			controller : 'PresentationController',
			controllerAs : 'PresentCtrl',
			templateUrl : '/templates/presentation/base.html',
		}).state('index.start', {
			url : '/start',
			templateUrl : '/templates/presentation/start.html',
			controller : 'StartController',
			controllerAs : 'StartCtrl'
		}).state('cadastrar', {
			url : '/novoUsuario',
			templateUrl : '/templates/app/cadastrar.html',
			controller : 'CadastrarController',
			controllerAs : 'CadastrarCtrl'
		}).state('recuperarSenha', {
			url : '/recuperarSenha',
			templateUrl : '/templates/app/recuperar.html',
			controller : 'RecuperarSenhaController',
			controllerAs : 'RecSenhaCtrl'
		}).state('emailRecuperar', {
			url : '/emailRecuperacao',
			templateUrl : '/templates/app/emailRecuperar.html',
			controller : 'RecuperarEmailController',
			controllerAs : 'RecEmailCtrl'
		}).state('app', {
			url : '/app',
			templateUrl : '/app/cliente/base.html',
			resolve : {
				LoginService : "LoginService",
				session : session
			}
		}).state('app.compra1', {
			url : '/compra-consultoria-1mes',
			templateUrl : '/app/cliente/compraTreinamento1.html',
			controller : 'ComprarController',
			controllerAs : 'CompraCtrl'
		}).state('app.compra3', {
			url : '/compra-consultoria-3meses',
			templateUrl : '/app/cliente/compraTreinamento3.html',
			controller : 'ComprarController',
			controllerAs : 'CompraCtrl'
		}).state('app.planos', {
			url : '/planos',
			templateUrl : '/app/cliente/planos.html',
			controller : 'ClientePlanoController',
			controllerAs : 'CliPlanoCtrl'
		}).state('app.treinos', {
			url : '/treinos',
			templateUrl : '/app/cliente/treinos.html',
			controller : 'ClienteTreinoController',
			controllerAs : 'CliTreinoCtrl'
		}).state('app.treino', {
			url : '/treino/:id',
			templateUrl : '/app/cliente/treino.html',
			controller : 'AcessarTreinoController',
			controllerAs : 'AceTreinoCtrl',
			resolve : {
				treino : treino
			}
		}).state('app.biset', {
			url : '/Biset',
			templateUrl : '/app/treinos/biset.html'
		}).state('app.dropset', {
			url : '/Dropset',
			templateUrl : '/app/treinos/dropset.html'
		}).state('app.circuito', {
			url : '/Circuito',
			templateUrl : '/app/treinos/circuito.html'
		}).state('app.metabolico', {
			url : '/Metabolico',
			templateUrl : '/app/treinos/metabolico.html'
		}).state('app.oclusao', {
			url : '/Oclusao',
			templateUrl : '/app/treinos/oclusaoVascular.html'
		}).state('app.piramidalDes', {
			url : '/PiramidalDecrescente',
			templateUrl : '/app/treinos/piramidalDecrescente.html'
		}).state('app.tensional', {
			url : '/Tensional',
			templateUrl : '/app/treinos/tensional.html'
		}).state('app.triset', {
			url : '/Triset',
			templateUrl : '/app/treinos/triset.html'
		}).state('app.duvidas', {
			url : '/duvidas',
			templateUrl : '/app/cliente/duvidas.html',
			controller : 'ClienteDuvidaController',
			controllerAs : 'CliDuvidaCtrl'
		}).state('app.duvida', {
			url : '/duvida/:id',
			templateUrl : '/app/cliente/duvida.html',
			controller : 'ClienteDuvidaUnitariaController',
			controllerAs : 'DuvidaUniCtrl',
			resolve : {
				duvida : duvida
			}
		}).state('app.faq', {
			url : '/duvidasFrequentes',
			templateUrl : '/app/cliente/faq.html'
		}).state('app.conta', {
			url : '/conta',
			templateUrl : '/app/cliente/conta.html',
			controller : 'ClienteContaController',
			controllerAs : 'CliContaCtrl'
		}).state('app.formulario', {
			url : '/formulario/:id',
			templateUrl : '/app/cliente/formulario.html',
			controller : 'ClienteFormularioController',
			controllerAs : 'CliFormCtrl',
			resolve : {
				form : form
			}
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
			controllerAs : 'UsuarioAdmCtrl'
		}).state('admin.treinos', {
			url : '/treinos',
			templateUrl : '/app/admin/treinos.html',
			controller : 'TreinoAdminController',
			controllerAs : 'TreinoAdmCtrl'
		}).state('admin.treino', {
			url : '/treino/:id',
			templateUrl : '/app/admin/treino.html',
			controller : 'LiberarTreinoAdminController',
			controllerAs : 'LibeTreinoAdmCtrl',
			resolve : {
				treino : treino
			}
		}).state('admin.planos', {
			url : '/planos',
			templateUrl : '/app/admin/planos.html',
			controller : 'PlanoAdminController',
			controllerAs : 'PlanoAdmCtrl'
		}).state('admin.duvidas', {
			url : '/duvidas',
			templateUrl : '/app/admin/duvidas.html',
			controller : 'DuvidaAdminController',
			controllerAs : 'DuvidaAdmCtrl'
		}).state('admin.duvida', {
			url : '/duvida/:id',
			templateUrl : '/app/cliente/duvida.html',
			controller : 'AdminDuvidaUnitariaController',
			controllerAs : 'DuvidaUniCtrl',
			resolve : {
				duvida : duvida
			}
		}).state('admin.modelos', {
			url : '/modelos',
			templateUrl : '/app/admin/modelos.html',
			controller : 'ModeloAdminController',
			controllerAs : 'ModeloAdmCtrl'
		});
	}

})();
