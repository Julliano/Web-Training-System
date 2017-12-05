;(function() {
	"use sctrict";

	angular.module("consultoria").directive("sfCpf", sfCpf);

	sfCpf.$inject = [];

	/** @ngInject */
	function sfCpf() {
		return {
			restrict : "A",
			require : 'ngModel',
			link : function(scope, elm, attrs, ctrl) {
				ctrl.$validators.cpf = function(modelValue, viewValue) {

					if (ctrl.$isEmpty(modelValue)) {
						return true
					}

					var soma;
					var resto;
					var i = 0;
					soma = 0;

					if (modelValue.length != 11 || modelValue == "00000000000"
							|| modelValue == "11111111111"
							|| modelValue == "22222222222"
							|| modelValue == "33333333333"
							|| modelValue == "44444444444"
							|| modelValue == "55555555555"
							|| modelValue == "66666666666"
							|| modelValue == "77777777777"
							|| modelValue == "88888888888"
							|| modelValue == "99999999999") {
						return false;
					}
					for (i = 1; i <= 9; i++) {
						soma = soma + parseInt(modelValue.substring(i - 1, i))
								* (11 - i);
					}

					resto = soma % 11;

					if (resto == 10 || resto == 11 || resto < 2) {
						resto = 0;
					} else {
						resto = 11 - resto;
					}

					if (resto != parseInt(modelValue.substring(9, 10))) {
						return false;
					}

					soma = 0;

					for (i = 1; i <= 10; i++) {
						soma = soma + parseInt(modelValue.substring(i - 1, i))
								* (12 - i);
					}
					resto = soma % 11 < 2 ? 0 : 11 - soma % 11;

					if (resto != parseInt(modelValue.substring(10, 11))) {
						return false;
					}
					return true;
				}
			}
		}

	}

})();

(function() {
	"use sctrict";

	angular.module("consultoria").directive("sfCnpj", sfCnpj);

	sfCnpj.$inject = [];

	/** @ngInject */
	function sfCnpj() {
		return {
			restrict : "A",
			require : 'ngModel',
			link : function(scope, elm, attrs, ctrl) {
				ctrl.$validators.cpf = function(modelValue, viewValue) {
					if (ctrl.$isEmpty(modelValue)) {
						return true
					}

					var tamanho = 0;
					var numeros = "";
					var digitos = "";
					var soma = 0;
					var pos = 0;
					var i = 0;
					var resultado;

					if (modelValue.length != 14 || modelValue == "00000000000000"
							|| modelValue == "11111111111111"
							|| modelValue == "22222222222222"
							|| modelValue == "33333333333333"
							|| modelValue == "44444444444444"
							|| modelValue == "55555555555555"
							|| modelValue == "66666666666666"
							|| modelValue == "77777777777777"
							|| modelValue == "88888888888888"
							|| modelValue == "99999999999999") {
						return false;
					}

					tamanho = modelValue.length - 2
					numeros = modelValue.substring(0, tamanho);
					digitos = modelValue.substring(tamanho);
					soma = 0;
					pos = tamanho - 7;
					for (i = tamanho; i >= 1; i--) {
						soma += numeros.charAt(tamanho - i) * pos--;
						if (pos < 2) {
							pos = 9;
						}
					}
					resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
					if (resultado != digitos.charAt(0)) {
						return false;
					}

					tamanho = tamanho + 1;
					numeros = modelValue.substring(0, tamanho);
					soma = 0;
					pos = tamanho - 7;
					for (i = tamanho; i >= 1; i--) {
						soma += numeros.charAt(tamanho - i) * pos--;
						if (pos < 2) {
							pos = 9;
						}
					}
					resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
					if (resultado != digitos.charAt(1)) {
						return false;
					}

					return true;

				}
			}
		}

	}

})();